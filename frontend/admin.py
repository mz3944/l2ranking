from django.contrib import admin

from frontend import models as frontend_models

class ServerAdmin(admin.ModelAdmin):
    pass

class CategoryAdmin(admin.ModelAdmin):
    pass

class VoteAdmin(admin.ModelAdmin):
    pass

class NewsAdmin(admin.ModelAdmin):
    pass

admin.site.register(frontend_models.Server, ServerAdmin)
admin.site.register(frontend_models.Category, CategoryAdmin)
admin.site.register(frontend_models.Vote, VoteAdmin)
admin.site.register(frontend_models.News, NewsAdmin)