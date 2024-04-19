# Generated by Django 4.0.8 on 2023-02-07 11:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0020_remove_social_links_id_alter_social_links_company_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Performance',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('initial_date', models.DateTimeField(auto_now=True)),
                ('performance_date', models.DateTimeField()),
                ('web_mobile_page_speed', models.FloatField(blank=True, max_length=255)),
                ('web_desktop_page_speed', models.FloatField(blank=True, max_length=255)),
                ('web_bounce_rate', models.FloatField(blank=True, max_length=255)),
                ('web_monthly_traffic', models.FloatField(blank=True, max_length=255)),
                ('web_pages_visit', models.FloatField(blank=True, max_length=255)),
                ('web_avg_time', models.FloatField(blank=True, max_length=255)),
                ('web_mail_traffic', models.FloatField(blank=True, max_length=255)),
                ('web_referred_traffic', models.FloatField(blank=True, max_length=255)),
                ('web_social_traffic', models.FloatField(blank=True, max_length=255)),
                ('web_organic_traffic', models.FloatField(blank=True, max_length=255)),
                ('web_paid_traffic', models.FloatField(blank=True, max_length=255)),
                ('web_direct_traffic', models.FloatField(blank=True, max_length=255)),
                ('web_social_sources', models.FloatField(blank=True, max_length=255)),
                ('seo_organic_traffic', models.FloatField(blank=True, max_length=255)),
                ('seo_w_authority', models.FloatField(blank=True, max_length=255)),
                ('seo_total_keywords', models.FloatField(blank=True, max_length=255)),
                ('seo_avg_organic_rank', models.FloatField(blank=True, max_length=255)),
                ('seo_referring_domains', models.FloatField(blank=True, max_length=255)),
                ('seo_backlinks', models.FloatField(blank=True, max_length=255)),
                ('seo_avg_keywords', models.FloatField(blank=True, max_length=255)),
                ('seo_traffic_value', models.FloatField(blank=True, max_length=255)),
                ('paid_paid_traffic', models.FloatField(blank=True, max_length=255)),
                ('paid_est_cpc_links', models.FloatField(blank=True, max_length=255)),
                ('paid_paid_keywords', models.FloatField(blank=True, max_length=255)),
                ('paid_est_cpc_budget', models.FloatField(blank=True, max_length=255)),
                ('social_engagement_rate', models.FloatField(blank=True, max_length=255)),
                ('social_total_followers', models.FloatField(blank=True, max_length=255)),
                ('social_total_interactions', models.FloatField(blank=True, max_length=255)),
                ('social_total_clicks', models.FloatField(blank=True, max_length=255)),
                ('facebook_total_followers', models.FloatField(blank=True, max_length=255)),
                ('facebook_total_page_likes', models.FloatField(blank=True, max_length=255)),
                ('facebook_avg_post_likes', models.FloatField(blank=True, max_length=255)),
                ('facebook_avg_post_shares', models.FloatField(blank=True, max_length=255)),
                ('facebook_avg_post_comments', models.FloatField(blank=True, max_length=255)),
                ('instagram_total_followers', models.FloatField(blank=True, max_length=255)),
                ('instagram_total_posts', models.FloatField(blank=True, max_length=255)),
                ('instagram_avg_likes', models.FloatField(blank=True, max_length=255)),
                ('instagram_avg_comments', models.FloatField(blank=True, max_length=255)),
                ('twitter_total_followers', models.FloatField(blank=True, max_length=255)),
                ('twitter_total_following', models.FloatField(blank=True, max_length=255)),
                ('twitter_avg_retweets', models.FloatField(blank=True, max_length=255)),
                ('twitter_avg_replies', models.FloatField(blank=True, max_length=255)),
                ('twitter_avg_likes', models.FloatField(blank=True, max_length=255)),
                ('youtube_total_videos', models.FloatField(blank=True, max_length=255)),
                ('youtube_total_views', models.FloatField(blank=True, max_length=255)),
                ('youtube_total_likes', models.FloatField(blank=True, max_length=255)),
                ('youtube_total_comments', models.FloatField(blank=True, max_length=255)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.project')),
            ],
        ),
    ]