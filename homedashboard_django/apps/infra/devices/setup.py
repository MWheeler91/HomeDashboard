import os, tempfile, paramiko, environ
from pathlib import Path
from django.conf import settings
from .models import SshKeys, DeviceAuth
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token


def setup_server(obj):
    env = environ.Env()
    ssh = None

    ssh_keys = SshKeys.objects.filter(key_type='YubiKey') if obj.is_public_facing else SshKeys.objects.all()
    public_keys = [k.public_key for k in ssh_keys]

    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(
            hostname=obj.ip_address,
            username=env("SETUP_USERNAME"),
            password=env("SETUP_PASSWORD")
        )

        sftp = ssh.open_sftp()

        # Step 1: Add public SSH keys
        ssh.exec_command("mkdir -p ~/.ssh && chmod 700 ~/.ssh")
        for key in public_keys:
            ssh.exec_command(f'echo "{key.strip()}" >> ~/.ssh/authorized_keys')
        ssh.exec_command("chmod 600 ~/.ssh/authorized_keys")

        # Step 2: Inject credentials into FastAPI template
        main_path = Path(settings.BASE_DIR) / 'agent_template' / 'main.py'
        with open(main_path, 'r') as f:
            code = f.read()

        token = get_token(obj)
        code = code.replace('your-token-here', token).replace('your-managed-device-id', obj.hostname)

        with tempfile.NamedTemporaryFile('w', delete=False) as tmp:
            tmp.write(code)
            tmp.flush()
            temp_path = tmp.name

        remote_app_path = "/opt/fastapi_agent"
        ssh.exec_command(f"mkdir -p {remote_app_path}")
        sftp.put(temp_path, f"{remote_app_path}/main.py")
        os.unlink(temp_path)

        # Step 3: Create systemd service
        service_content = f"""[Unit]
Description=FastAPI Agent
After=network.target

[Service]
ExecStart=/usr/bin/python3 {remote_app_path}/main.py
Restart=always
User={env('SETUP_USERNAME')}
WorkingDirectory={remote_app_path}

[Install]
WantedBy=multi-user.target
"""

        with tempfile.NamedTemporaryFile('w', delete=False) as svc:
            svc.write(service_content)
            svc.flush()
            service_file = svc.name

        sftp.put(service_file, "/etc/systemd/system/fastapi_agent.service")
        os.unlink(service_file)

        ssh.exec_command("sudo systemctl daemon-reexec && sudo systemctl daemon-reload && sudo systemctl enable --now fastapi_agent")

        # Step 4: Lock down FastAPI (optional)
        stdin, stdout, _ = ssh.exec_command("which ufw")
        if stdout.read().strip():
            ssh.exec_command("sudo ufw deny 8000")
            ssh.exec_command("sudo ufw allow from 192.168.0.0/16 to any port 8000")

        # Step 5: Disable agent account
        ssh.exec_command("sudo usermod -L agent_account")

        # Step 6: Update device state
        obj.is_processed = True
        obj.has_keys = True
        obj.save()
        
    finally:
        if ssh:
            ssh.close()


def get_token(obj):
    device_auth, _ = DeviceAuth.objects.get_or_create(device=obj)

    User = get_user_model()
    user = User.objects.get(username='agent_user')
    token_obj, _ = Token.objects.get_or_create(user=user)

    device_auth.token = token_obj.key
    device_auth.save()
    return token_obj.key
