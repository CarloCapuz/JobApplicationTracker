#!/usr/bin/env python3
"""
Setup script for Job Tracker with authentication
"""

import os
import secrets
import sys

def create_env_file():
    """Create .env file with default values"""
    if os.path.exists('.env'):
        print("✅ .env file already exists")
        return
    
    # Generate a random secret key
    secret_key = secrets.token_hex(32)
    
    env_content = f"""# Environment variables for Job Tracker
# Change these values for production!

# Authentication credentials
FLASK_USERNAME=your_username_here
FLASK_PASSWORD=your_password_here

# Flask configuration
FLASK_ENV=development
SECRET_KEY={secret_key}

# Database configuration
DATABASE_URL=sqlite:///job_tracker.db
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ Created .env file with default credentials")
    print("📝 Default login credentials:")
    print("   Username: your_username_here")
    print("   Password: your_password_here")
    print("⚠️  IMPORTANT: Change these credentials before deploying!")

def check_dependencies():
    """Check if required packages are installed"""
    try:
        import flask
        import flask_login
        import dotenv
        print("✅ All required packages are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing package: {e}")
        print("Run: pip install -r requirements.txt")
        return False

def main():
    print("🚀 Job Tracker Setup")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Create .env file
    create_env_file()
    
    print("\n🎉 Setup complete!")
    print("\nNext steps:")
    print("1. Edit .env file to set your own credentials")
    print("2. Run: python app.py")
    print("3. Visit: http://localhost:5000")
    print("4. Login with your credentials")
    
    print("\n📚 For deployment instructions, see DEPLOYMENT.md")

if __name__ == "__main__":
    main()
