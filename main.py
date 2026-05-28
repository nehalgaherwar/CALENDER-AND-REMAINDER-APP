"""
Calendar and Reminder App - Main Entry Point

A comprehensive Python application for managing calendar events and reminders
with a modern dark mode GUI using CustomTkinter and SQLite database.

Features:
- Monthly calendar view with date navigation
- Add, edit, and delete reminders
- Search functionality for reminders
- SQLite database for persistent storage
- Notification/reminder alerts
- Priority levels and categories
- Dark mode modern UI
- Time and date picker
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui import main

if __name__ == "__main__":
    main()
