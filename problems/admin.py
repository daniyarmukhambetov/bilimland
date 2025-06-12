from django.contrib import admin
from .models import Problem, Choice, Attempt

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4

@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ('title', 'problem_type', 'difficulty', 'created_at')
    list_filter = ('problem_type', 'difficulty', 'created_at')
    search_fields = ('title', 'description')
    inlines = [ChoiceInline]
    
    def get_readonly_fields(self, request, obj=None):
        # Make problem_type readonly if the problem already exists
        # This prevents changing a problem type after choices have been added
        if obj:
            return ('problem_type',)
        return ()

@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'problem', 'is_correct', 'created_at')
    list_filter = ('is_correct', 'created_at')
    search_fields = ('user__username', 'problem__title')
    readonly_fields = ('user', 'problem', 'selected_choices', 'answer_text', 'created_at')
    
    def has_add_permission(self, request):
        # Prevent adding attempts directly through admin
        return False
