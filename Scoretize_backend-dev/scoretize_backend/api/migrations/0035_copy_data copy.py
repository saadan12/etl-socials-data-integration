from django.db import migrations, models


def copy_seo_data(apps, schema_editor):
    Seo = apps.get_model('api', 'Seo')
    NewSeo = apps.get_model('api', 'Seo_data')

    for obj in Seo.objects.all():
        new_seo = NewSeo(seo_id=obj.seo_id, initial_date=obj.initial_date, organic_traffic=obj.organic_traffic, web_authority=obj.web_authority, total_keywords=obj.total_keywords, avg_keywords_search=obj.avg_keywords_search, traffic_value=obj.traffic_value, paid_traffic=obj.paid_traffic, estimatedCPC=obj.estimatedCPC, paid_keywords=obj.paid_keywords, estm_ppc_budget=obj.estm_ppc_budget, backlinks=obj.backlinks, referring_domains=obj.referring_domains, avg_organic_rank=obj.avg_organic_rank, company=obj.company)
        new_seo.save()

def copy_sm_data(apps, schema_editor):
    SocialMedia = apps.get_model('api', 'Social_media')
    NewSocialMedia = apps.get_model('api', 'Social_media_data')

    for obj in SocialMedia.objects.all():
        new_sm = NewSocialMedia(social_id=obj.social_id, initial_date=obj.initial_date, global_engagement_rate=obj.global_engagement_rate, total_followers=obj.total_followers, total_average_interactions=obj.total_average_interactions, total_clicks=obj.total_clicks, project_id=obj.project_id, company=obj.company)
        new_sm.save()

class Migration(migrations.Migration):

    dependencies = [
        ('api', '0034_social_media_data_seo_data'),
    ]

    operations = [
        migrations.RunPython(copy_seo_data),
        migrations.RunPython(copy_sm_data)
    ]
