import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "homedashboard_django.settings")

import django

django.setup()


import random
from faker import Faker
from catalog.models import Item, Category, Room, Condition
from account.models import User
from maintenance.models import Maintenance, Vehicle
from maintenance.models import Category as Maint_Category
from PIL import Image
from datetime import datetime

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

def FakeMaintRecord():
    allvehicles = list(Vehicle.objects.all())
    allcategories = list(Maint_Category.objects.all())
    allpeople = list(User.objects.all())

    rand_vehicle = (random.randrange(len(allvehicles)),)
    rand_category = (random.randrange(len(allcategories)),)
    rand_entered_by = (random.randrange(len(allpeople)),)

    maint = Maintenance.objects.get_or_create(
        vehicle = allvehicles[rand_vehicle[0]],
        mileage = random.randint(1, 250000),
        category = allcategories[rand_category[0]],
        short_description = "Rand Desc",
        maintenance_performed = fakegen.company(),
        cost = random.randint(1, 10000),
        entered_by=allpeople[rand_entered_by[0]],

    )

def populate_data(n=300):
    for entry in range(n):
        # FakeItem()
        FakeMaintRecord()


if __name__ == "__main__":
    main()
