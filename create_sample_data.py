"""
Script to create sample data for the Math Problems platform.
Run this script after migrations to populate the database with sample problems.
"""

import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uzdikland.settings')
django.setup()

from django.contrib.auth.models import User
from problems.models import Problem, Choice

def create_sample_problems():
    """Create sample problems of different types"""
    
    # Create a Multiple Choice Question
    mcq = Problem.objects.create(
        title="Solving a Quadratic Equation",
        description="""
Find all solutions to the quadratic equation:

$$x^2 - 5x + 6 = 0$$

Select all correct answers.
        """,
        difficulty="easy",
        problem_type="mcq"
    )
    
    # Add choices for the MCQ
    Choice.objects.create(problem=mcq, text="$x = 2$", is_correct=True)
    Choice.objects.create(problem=mcq, text="$x = 3$", is_correct=True)
    Choice.objects.create(problem=mcq, text="$x = -2$", is_correct=False)
    Choice.objects.create(problem=mcq, text="$x = -3$", is_correct=False)
    
    # Create a Single Choice Question
    scq = Problem.objects.create(
        title="Derivative of a Function",
        description="""
Calculate the derivative of the function:

$$f(x) = e^{2x} \sin(x)$$

Choose the correct answer.
        """,
        difficulty="medium",
        problem_type="scq"
    )
    
    # Add choices for the SCQ
    Choice.objects.create(problem=scq, text="$f'(x) = 2e^{2x} \sin(x) + e^{2x} \cos(x)$", is_correct=True)
    Choice.objects.create(problem=scq, text="$f'(x) = 2e^{2x} \sin(x)$", is_correct=False)
    Choice.objects.create(problem=scq, text="$f'(x) = e^{2x} \cos(x)$", is_correct=False)
    Choice.objects.create(problem=scq, text="$f'(x) = 2e^{2x} \sin(x) - e^{2x} \cos(x)$", is_correct=False)
    
    # Create an Open-ended Question
    Problem.objects.create(
        title="Proving a Trigonometric Identity",
        description="""
Prove the following trigonometric identity:

$$\sin^2(x) + \cos^2(x) = 1$$

Provide a detailed proof with all steps clearly explained.
        """,
        difficulty="hard",
        problem_type="open"
    )
    
    print("Sample problems created successfully!")

if __name__ == "__main__":
    # Check if problems already exist
    if Problem.objects.count() == 0:
        create_sample_problems()
    else:
        print("Problems already exist in the database. No sample data created.")