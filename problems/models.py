from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from markdown import markdown
import re

# Problem difficulty levels
DIFFICULTY_CHOICES = [
    ('easy', 'Easy'),
    ('medium', 'Medium'),
    ('hard', 'Hard'),
]

# Problem types
PROBLEM_TYPE_CHOICES = [
    ('mcq', 'Multiple Choice Question'),
    ('scq', 'Single Choice Question'),
    ('open', 'Open-ended Question'),
]

class Problem(models.Model):
    """Model representing a math problem"""
    title = models.CharField(max_length=200)
    description = models.TextField(help_text="Problem description (supports LaTeX)")
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='medium')
    problem_type = models.CharField(max_length=10, choices=PROBLEM_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('problem-detail', args=[str(self.id)])
    
    def description_html(self):
        """Convert markdown to HTML and preserve LaTeX"""
        # Convert markdown to HTML
        html = markdown(self.description)
        return html
    
    @property
    def is_mcq(self):
        return self.problem_type == 'mcq'
    
    @property
    def is_scq(self):
        return self.problem_type == 'scq'
    
    @property
    def is_open(self):
        return self.problem_type == 'open'


class Choice(models.Model):
    """Model representing a choice for MCQ or SCQ problems"""
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='choices')
    text = models.TextField(help_text="Choice text (supports LaTeX)")
    is_correct = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.text[:50]}..."
    
    def text_html(self):
        """Convert markdown to HTML and preserve LaTeX"""
        return markdown(self.text)


class Attempt(models.Model):
    """Model representing a student's attempt to solve a problem"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attempts')
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='attempts')
    
    # For MCQ/SCQ problems
    selected_choices = models.ManyToManyField(Choice, blank=True, related_name='attempts')
    
    # For open-ended problems
    answer_text = models.TextField(blank=True, null=True)
    
    is_correct = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        # Ensure a user can only have one attempt per problem
        unique_together = ['user', 'problem']
    
    def __str__(self):
        return f"{self.user.username}'s attempt on {self.problem.title}"
    
    def check_answer(self):
        """Check if the attempt is correct based on problem type"""
        if self.problem.is_mcq:
            # For MCQ, all correct choices must be selected and no incorrect choices
            correct_choices = self.problem.choices.filter(is_correct=True)
            selected_correct = self.selected_choices.filter(is_correct=True).count()
            selected_incorrect = self.selected_choices.filter(is_correct=False).count()
            
            self.is_correct = (selected_correct == correct_choices.count() and selected_incorrect == 0)
        
        elif self.problem.is_scq:
            # For SCQ, exactly one choice must be selected and it must be correct
            self.is_correct = (self.selected_choices.count() == 1 and
                              self.selected_choices.first().is_correct)
        
        # For open-ended problems, is_correct must be set manually by an admin/teacher
        
        self.save()
        return self.is_correct
