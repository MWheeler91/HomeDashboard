import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "homedashboard_django.settings")

import django

django.setup()


import random
from faker import Faker
from catalog.models import Item, Category, Room, Condition
from account.models import User

from PIL import Image

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "homedashboard_django.settings")


# fake pop script
fakegen = Faker()


def main():
    print("Populating the script!")
    populate_data()
    print("Complete!")


def FakeItem():
    allrooms = list(Room.objects.all())
    allcatagories = list(Category.objects.all())
    allconditions = list(Condition.objects.all())
    allpeople = list(User.objects.all())

    rand_item_category = (random.randrange(len(allcatagories)),)
    rand_condition = (random.randrange(len(allconditions)),)
    rand_room = (random.randrange(len(allrooms)),)
    rand_entered_by = random.randrange(len(allpeople))

    item = Item.objects.get_or_create(
        item_name=fakegen.company(),
        item_description="Random Desc",
        item_category=allcatagories[rand_item_category[0]],
        condition=allconditions[rand_condition[0]],
        room=allrooms[rand_room[0]],
        value=random.randint(1, 10000),
        model_number=fakegen.ssn(),
        serial_number=fakegen.ssn(),
        entered_by=allpeople[rand_entered_by],
    )


def populate_data(n=300):
    for entry in range(n):
        FakeItem()


if __name__ == "__main__":
    main()
