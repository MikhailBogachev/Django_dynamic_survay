from django.contrib import admin
from .models import Survey, Question, Choice, NextQuestionLogic


class NextQuestionLogicInline(admin.StackedInline):
    model = NextQuestionLogic
    extra = 1


class ChoiceAdmin(admin.ModelAdmin):
    inlines = [NextQuestionLogicInline]
    list_display = ('text', 'question',)
    list_editable = ('question',)


class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 5


class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ('text', 'survey',)
    list_editable = ('survey',)
    list_display_links = ('text',)


admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(Survey)
admin.site.register(NextQuestionLogic)
