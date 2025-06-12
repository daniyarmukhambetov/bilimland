from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.urls import reverse

from .models import Problem, Attempt, Choice

class HomeView(TemplateView):
    template_name = 'home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if self.request.user.is_authenticated:
            # Get recent successful attempts for the user
            context['recent_attempts'] = Attempt.objects.filter(
                user=self.request.user,
                is_correct=True
            ).order_by('-created_at')[:5]
            
        return context

class ProblemListView(ListView):
    model = Problem
    template_name = 'problems/problem_list.html'
    context_object_name = 'problems'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = Problem.objects.all()
        
        # Apply search filter
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query)
            )
        
        # Apply difficulty filter
        difficulty = self.request.GET.get('difficulty', '')
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)
        
        # Apply problem type filter
        problem_type = self.request.GET.get('problem_type', '')
        if problem_type:
            queryset = queryset.filter(problem_type=problem_type)
        
        # Apply solved/unsolved filters if user is authenticated
        if self.request.user.is_authenticated:
            solved = self.request.GET.get('solved', '')
            unsolved = self.request.GET.get('unsolved', '')
            
            if solved == 'true' and unsolved != 'true':
                # Get IDs of problems the user has solved correctly
                solved_problem_ids = Attempt.objects.filter(
                    user=self.request.user,
                    is_correct=True
                ).values_list('problem_id', flat=True)
                
                queryset = queryset.filter(id__in=solved_problem_ids)
                
            elif unsolved == 'true' and solved != 'true':
                # Get IDs of all problems the user has attempted
                attempted_problem_ids = Attempt.objects.filter(
                    user=self.request.user
                ).values_list('problem_id', flat=True)
                
                # Get IDs of problems the user has solved correctly
                solved_problem_ids = Attempt.objects.filter(
                    user=self.request.user,
                    is_correct=True
                ).values_list('problem_id', flat=True)
                
                # Filter for problems that either haven't been attempted or were attempted but not solved
                queryset = queryset.exclude(id__in=solved_problem_ids)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Check if any filter is applied
        context['filter_applied'] = any([
            self.request.GET.get('search', ''),
            self.request.GET.get('difficulty', ''),
            self.request.GET.get('problem_type', ''),
            self.request.GET.get('solved', ''),
            self.request.GET.get('unsolved', '')
        ])
        
        # If user is authenticated, add solved problems to context
        if self.request.user.is_authenticated:
            solved_problem_ids = Attempt.objects.filter(
                user=self.request.user,
                is_correct=True
            ).values_list('problem_id', flat=True)
            
            context['solved_problems'] = set(solved_problem_ids)
        
        return context

class ProblemDetailView(DetailView):
    model = Problem
    template_name = 'problems/problem_detail.html'
    context_object_name = 'problem'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # If user is authenticated, check if they've attempted this problem
        if self.request.user.is_authenticated:
            try:
                context['user_attempt'] = Attempt.objects.get(
                    user=self.request.user,
                    problem=self.object
                )
            except Attempt.DoesNotExist:
                context['user_attempt'] = None
        
        return context
    
    def post(self, request, *args, **kwargs):
        """Handle form submission for problem solving"""
        self.object = self.get_object()
        
        if request.user.is_authenticated:
            return submit_answer(request, self.object.pk)
        
        return self.get(request, *args, **kwargs)

@login_required
def submit_answer(request, pk):
    problem = get_object_or_404(Problem, pk=pk)
    
    if request.method == 'POST':
        # Get or create an attempt for this user and problem
        attempt, created = Attempt.objects.get_or_create(
            user=request.user,
            problem=problem,
            defaults={'is_correct': False}
        )
        
        if problem.is_mcq or problem.is_scq:
            # Clear previous selected choices
            attempt.selected_choices.clear()
            
            # Get selected choice IDs
            selected_choice_ids = request.POST.getlist('choices')
            
            if selected_choice_ids:
                # Add selected choices to the attempt
                selected_choices = Choice.objects.filter(id__in=selected_choice_ids)
                attempt.selected_choices.add(*selected_choices)
                
                # Check if the answer is correct
                attempt.check_answer()
                
                if attempt.is_correct:
                    messages.success(request, 'Correct answer!')
                else:
                    messages.error(request, 'Incorrect answer. Try again!')
            else:
                messages.error(request, 'Please select at least one choice.')
        
        elif problem.is_open:
            # Save the answer text
            attempt.answer_text = request.POST.get('answer_text', '')
            attempt.save()
            
            messages.info(request, 'Your answer has been submitted and will be reviewed.')
        
        return redirect('problem-detail', pk=problem.id)
    
    return redirect('problem-detail', pk=problem.id)
