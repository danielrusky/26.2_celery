from django.contrib import admin

from materials.models import Course, Lesson, Subscription


@admin.register(Course)
class AdminCourse(admin.ModelAdmin):
    list_display = ('title', 'image', 'description', 'owner',)


@admin.register(Lesson)
class AdminLesson(admin.ModelAdmin):
    list_display = ('course', 'title', 'description', 'image', 'url_video', 'owner',)


@admin.register(Subscription)
class AdminSubscription(admin.ModelAdmin):
    list_display = ('user', 'course',)