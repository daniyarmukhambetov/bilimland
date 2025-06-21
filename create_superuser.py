"""
Script to create a superuser for the Uzdikland application.
This script uses environment variables to set the username, password, and email.
"""

import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uzdikland.settings')
django.setup()

from django.contrib.auth.models import User
from django.db import IntegrityError

def create_superuser():
    """Create a superuser using environment variables"""
    
    # Get superuser credentials from environment variables
    username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'uzdikland_admin')
    password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'Uzd1kL@nd2025!')
    email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@uzdikland.kz')
    
    try:
        # Check if the user already exists
        if User.objects.filter(username=username).exists():
            print(f"Superuser '{username}' already exists.")
            return
        
        # Create the superuser
        User.objects.create_superuser(username=username, email=email, password=password)
        print(f"Superuser '{username}' created successfully.")
    
    except IntegrityError:
        print(f"Error: Could not create superuser '{username}'. Username may already exist.")
    except Exception as e:
        print(f"Error creating superuser: {str(e)}")

if __name__ == "__main__":
    create_superuser()