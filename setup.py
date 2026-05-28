#!/usr/bin/env python3
"""
Setup script for Calendar and Reminder App
Handles environment setup and dependency installation
"""

import subprocess
import sys
import os
import platform


def print_header(text):
    """Print formatted header."""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60 + "\n")


def check_python_version():
    """Check if Python version is compatible."""
    print_header("Checking Python Version")
    
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required!")
        print(f"   Current version: {sys.version}")
        sys.exit(1)
    
    print(f"✓ Python {sys.version.split()[0]} detected")


def install_requirements():
    """Install project requirements."""
    print_header("Installing Dependencies")
    
    requirements_file = os.path.join(
        os.path.dirname(__file__), 
        "requirements.txt"
    )
    
    if not os.path.exists(requirements_file):
        print("❌ requirements.txt not found!")
        sys.exit(1)
    
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-r", requirements_file],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        print("✓ Dependencies installed successfully")
    except subprocess.CalledProcessError:
        print("⚠ Installation encountered some issues")
        print("Attempting alternative installation...")
        
        # Install without pyaudio if there are issues
        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", 
                 "install", "customtkinter", "pillow", 
                 "tkcalendar", "playsound"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            print("✓ Core dependencies installed (without audio)")
        except Exception as e:
            print(f"❌ Failed to install dependencies: {e}")
            sys.exit(1)


def check_database_setup():
    """Check if database can be created."""
    print_header("Database Setup")
    
    db_path = os.path.join(os.path.dirname(__file__), "reminders.db")
    
    try:
        import sqlite3
        conn = sqlite3.connect(db_path)
        conn.close()
        print("✓ Database setup verified")
    except Exception as e:
        print(f"❌ Database setup failed: {e}")
        sys.exit(1)


def launch_application():
    """Launch the main application."""
    print_header("Launching Application")
    
    main_file = os.path.join(os.path.dirname(__file__), "main.py")
    
    try:
        subprocess.call([sys.executable, main_file])
    except Exception as e:
        print(f"❌ Failed to launch application: {e}")
        sys.exit(1)


def main():
    """Run setup procedure."""
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "  📅 Calendar & Reminder App - Setup Wizard".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "═" * 58 + "╝")
    
    check_python_version()
    install_requirements()
    check_database_setup()
    
    print_header("Setup Complete!")
    print("✓ All requirements satisfied")
    print("✓ Ready to launch application\n")
    
    response = input("Do you want to launch the application now? (yes/no): ").strip().lower()
    
    if response in ('yes', 'y', '1', 'true'):
        launch_application()
    else:
        print("\nTo launch later, run: python main.py")
        print("Thank you for using Calendar & Reminder App! 📝")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n✗ Setup cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
