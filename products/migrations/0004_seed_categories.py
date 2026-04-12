from django.db import migrations

def seed_categories(apps, schema_editor):
    Category = apps.get_model("products", "Category")

    default_categories = [
        "Car","Bike","Scooter","Bicycle","Electric Car","Electric Bike",
        "Auto Rickshaw","Bus","Truck","Van","SUV","Pickup",
        "Tractor","Ambulance","Luxury Car","Sports Bike"
    ]

    for cat in default_categories:
        Category.objects.get_or_create(name=cat)


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_rename_vehicledetails_product'),
    ]

    operations = [
        migrations.RunPython(seed_categories),
    ]