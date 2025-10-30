from django.contrib import admin
from .models import Choice, Question

# Register your models here.

#if you don't want to customize stuff just do this
# admin.site.register(Choice)

#class lets you change the default options in admin form
#inline ones let you add this to another form, so when you fill out the form for Question, it has default 3 fields for Choices
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    #change order of fields
    # fields= ["pub_date", "question_text"]
    #split fields into different sections, first arg is section heading
    fieldsets = [
        (None, {"fields": ["question_text"]}),
        ("Date information", {"fields": ["pub_date"], "classes": ["collapse"]}),
    ]
    inlines=[ChoiceInline]
    #which fields to show in the list of existing questions (default is tostring)
    list_display = ["question_text", "pub_date", "was_published_recently"]
    list_filter = ["pub_date"] #allows you to filter questions by date in the admin dashboard
    search_fields = ["question_text"] #allows you to search any number of fields but limit to a reasonable amount

admin.site.register(Question, QuestionAdmin)