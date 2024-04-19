from django.contrib import admin
from .models import Users, User_Type, Account, \
    Company, Company_wise_scores, \
    Industry_wise_scores, Seo, \
    Social_media, Website, Youtube, \
    Website_traffic, UserProject, \
    Twitter, Instagram, Facebook, \
    Sector, Project

# Register your models here.
admin.site.register(Users)
admin.site.register(User_Type)
admin.site.register(Account)
admin.site.register(Company)
admin.site.register(Company_wise_scores)
admin.site.register(Industry_wise_scores)
admin.site.register(Seo)
admin.site.register(Social_media)
admin.site.register(Website)
admin.site.register(Website_traffic)
admin.site.register(UserProject)
admin.site.register(Youtube)
admin.site.register(Twitter)
admin.site.register(Instagram)
admin.site.register(Facebook)
admin.site.register(Sector)
admin.site.register(Project)
