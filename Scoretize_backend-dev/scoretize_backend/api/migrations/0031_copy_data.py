from django.db import migrations, models


def copy_data(apps, schema_editor):
    Website = apps.get_model('api', 'Website')
    NewWebsite = apps.get_model('api', 'Website_model')

    for obj in Website.objects.all():
        new_website = NewWebsite(website_id=obj.website_id, company=obj.company, initial_date=obj.initial_date, mobile_page_speed=obj.mobile_page_speed, desktop_page_speed=obj.desktop_page_speed, bounce_rate=obj.bounce_rate, monthly_traffic=obj.monthly_traffic, pages_visit=obj.pages_visit, avg_TimeOnSite=obj.avg_TimeOnSite)
        new_website.save()


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0030_website_model'),
    ]

    operations = [
        migrations.RunPython(copy_data)
    ]
