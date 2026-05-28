"""
Examples and Configuration for Calendar and Reminder App

This file demonstrates various ways to use the Calendar and Reminder App,
both through the GUI and programmatically.
"""

# ============================================================================
# EXAMPLE 1: Using the Application Programmatically
# ============================================================================

"""
from database import ReminderDatabase
from utils import DateUtils

# Initialize database
db = ReminderDatabase("reminders.db")

# Add a reminder programmatically
reminder_id = db.add_reminder(
    title="Project Deadline",
    description="Submit quarterly report",
    date="2024-03-15",
    time="17:00",
    category="Work",
    priority="High"
)

# Get all reminders
all_reminders = db.get_all_reminders()
for reminder in all_reminders:
    print(f"{reminder['date']} {reminder['time']}: {reminder['title']}")

# Get reminders for specific date
today_reminders = db.get_reminders_by_date(DateUtils.get_current_date())
print(f"Today's reminders: {len(today_reminders)}")

# Search reminders
results = db.search_reminders("project")
print(f"Search results: {results}")

# Update a reminder
db.update_reminder(
    reminder_id=1,
    title="Updated Title",
    priority="Normal"
)

# Get upcoming reminders
upcoming = db.get_upcoming_reminders(days=7)
print(f"Reminders for next 7 days: {len(upcoming)}")

# Close database
db.close()
"""

# ============================================================================
# EXAMPLE 2: Custom Notification Handler
# ============================================================================

"""
from notifications import NotificationManager
from database import ReminderDatabase

def custom_notification_handler(reminder):
    '''Custom handler for reminders'''
    title = reminder['title']
    print(f"ALERT: {title} is due!")
    # Add custom logic here (email, SMS, webhook, etc.)

# Initialize
notification_manager = NotificationManager()
reminder_db = ReminderDatabase()

# Set custom callback
notification_manager.add_notification_callback(custom_notification_handler)

# Start monitoring
notification_manager.start(check_interval=30)  # Check every 30 seconds

# Set reminders to monitor
reminders = reminder_db.get_all_reminders()
notification_manager.set_reminders(reminders)

# Run until stopped
import time
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    notification_manager.stop()
"""

# ============================================================================
# EXAMPLE 3: Bulk Import Reminders
# ============================================================================

"""
from database import ReminderDatabase
import csv

def import_reminders_from_csv(csv_file):
    '''Import reminders from CSV file'''
    db = ReminderDatabase()
    
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            db.add_reminder(
                title=row['title'],
                description=row.get('description', ''),
                date=row['date'],
                time=row['time'],
                category=row.get('category', 'General'),
                priority=row.get('priority', 'Normal')
            )
    
    db.close()

# Usage:
# import_reminders_from_csv('reminders.csv')

# CSV format:
# title,description,date,time,category,priority
# Team Meeting,Weekly sync,2024-03-20,10:00,Work,Normal
# Birthday,Jane's birthday,2024-03-22,00:00,Personal,High
"""

# ============================================================================
# EXAMPLE 4: Export Reminders to CSV
# ============================================================================

"""
from database import ReminderDatabase
import csv

def export_reminders_to_csv(output_file, category=None):
    '''Export reminders to CSV file'''
    db = ReminderDatabase()
    
    if category:
        reminders = db.get_reminders_by_category(category)
    else:
        reminders = db.get_all_reminders()
    
    with open(output_file, 'w', newline='') as f:
        writer = csv.DictWriter(
            f, 
            fieldnames=['id', 'title', 'description', 'date', 'time', 
                       'category', 'priority', 'is_completed']
        )
        writer.writeheader()
        writer.writerows(reminders)
    
    db.close()

# Usage:
# export_reminders_to_csv('all_reminders.csv')
# export_reminders_to_csv('work_reminders.csv', category='Work')
"""

# ============================================================================
# EXAMPLE 5: Generate Reminder Statistics
# ============================================================================

"""
from database import ReminderDatabase
from collections import Counter

def generate_statistics():
    '''Generate statistics about reminders'''
    db = ReminderDatabase()
    reminders = db.get_all_reminders()
    
    if not reminders:
        print("No reminders found")
        return
    
    # Count by category
    categories = Counter(r['category'] for r in reminders)
    print("Reminders by category:")
    for cat, count in categories.most_common():
        print(f"  {cat}: {count}")
    
    # Count by priority
    priorities = Counter(r['priority'] for r in reminders)
    print("\nReminders by priority:")
    for pri, count in priorities.most_common():
        print(f"  {pri}: {count}")
    
    # Count completed vs pending
    completed = sum(1 for r in reminders if r['is_completed'])
    pending = len(reminders) - completed
    print(f"\nCompletion status:")
    print(f"  Completed: {completed}")
    print(f"  Pending: {pending}")
    
    # Average reminders per day
    dates = set(r['date'] for r in reminders)
    print(f"\nTotal unique dates: {len(dates)}")
    print(f"Average reminders per day: {len(reminders) / len(dates):.2f}")
    
    db.close()

# Usage:
# generate_statistics()
"""

# ============================================================================
# EXAMPLE 6: Data Cleanup and Maintenance
# ============================================================================

"""
from database import ReminderDatabase
from utils import DateUtils
from datetime import datetime, timedelta

def cleanup_old_reminders(days_ago=30):
    '''Delete completed reminders older than specified days'''
    db = ReminderDatabase()
    reminders = db.get_all_reminders()
    
    cutoff_date = datetime.now() - timedelta(days=days_ago)
    count = 0
    
    for reminder in reminders:
        if reminder['is_completed']:
            reminder_date = datetime.strptime(reminder['date'], '%Y-%m-%d')
            if reminder_date < cutoff_date:
                db.delete_reminder(reminder['id'])
                count += 1
    
    print(f"Deleted {count} old completed reminders")
    db.close()

# Usage:
# cleanup_old_reminders(days_ago=30)
"""

# ============================================================================
# EXAMPLE 7: Scheduled Backup
# ============================================================================

"""
import shutil
import os
from datetime import datetime

def backup_database(source_db='reminders.db'):
    '''Create a backup of the database'''
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = f'reminders_backup_{timestamp}.db'
    
    if os.path.exists(source_db):
        shutil.copy2(source_db, backup_file)
        print(f"Backup created: {backup_file}")
        return backup_file
    else:
        print(f"Database file not found: {source_db}")
        return None

# Usage:
# backup_database()

# Scheduled backup (using APScheduler):
# from apscheduler.schedulers.background import BackgroundScheduler
# 
# scheduler = BackgroundScheduler()
# scheduler.add_job(backup_database, 'cron', hour=0)  # Daily at midnight
# scheduler.start()
"""

# ============================================================================
# EXAMPLE 8: Custom Categories and Colors
# ============================================================================

"""
from utils import CategoryColors

# Add custom category
CategoryColors.add_category_color('Emergency', '#D32F2F')

# Get category color
color = CategoryColors.get_color('Emergency')
print(f"Emergency color: {color}")

# Update default categories list
custom_categories = CategoryColors.get_default_categories()
custom_categories.append('Emergency')
"""

# ============================================================================
# EXAMPLE 9: Reminder Templates
# ============================================================================

"""
from database import ReminderDatabase
from utils import DateUtils

# Define reminder templates
TEMPLATES = {
    'daily_standup': {
        'title': 'Daily Standup',
        'description': 'Participate in team standup',
        'time': '09:00',
        'category': 'Work',
        'priority': 'Normal'
    },
    'gym': {
        'title': 'Gym Session',
        'description': '1 hour workout',
        'time': '18:00',
        'category': 'Health',
        'priority': 'Normal'
    }
}

def create_from_template(template_name, date):
    '''Create a reminder from a template'''
    db = ReminderDatabase()
    template = TEMPLATES.get(template_name)
    
    if not template:
        print(f"Template '{template_name}' not found")
        return
    
    reminder_id = db.add_reminder(
        date=date,
        **template
    )
    
    db.close()
    return reminder_id

# Usage:
# create_from_template('daily_standup', '2024-03-20')
# create_from_template('gym', DateUtils.get_current_date())
"""

# ============================================================================
# EXAMPLE 10: Integration with External Services
# ============================================================================

"""
from database import ReminderDatabase
from notifications import NotificationManager

# Example: Send reminder to email
def send_reminder_email(reminder):
    '''Send reminder notification via email'''
    import smtplib
    from email.mime.text import MIMEText
    
    sender = 'your-email@gmail.com'
    password = 'your-app-password'
    recipient = 'recipient@example.com'
    
    msg = MIMEText(
        f"Title: {reminder['title']}\\n"
        f"Time: {reminder['time']}\\n"
        f"Description: {reminder['description']}"
    )
    msg['Subject'] = f"Reminder: {reminder['title']}"
    msg['From'] = sender
    msg['To'] = recipient
    
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender, password)
            server.send_message(msg)
    except Exception as e:
        print(f"Failed to send email: {e}")

# Example: Send to Slack
def send_to_slack(reminder):
    '''Send reminder to Slack channel'''
    import requests
    
    webhook_url = 'YOUR_SLACK_WEBHOOK_URL'
    message = {
        'text': f"*{reminder['title']}*\\n_{reminder['description']}_\\nTime: {reminder['time']}"
    }
    
    try:
        requests.post(webhook_url, json=message)
    except Exception as e:
        print(f"Failed to send to Slack: {e}")

# Setup
def setup_integrations():
    notification_manager = NotificationManager()
    notification_manager.add_notification_callback(send_reminder_email)
    notification_manager.add_notification_callback(send_to_slack)
    notification_manager.start()
    
    return notification_manager

# Usage:
# notif_manager = setup_integrations()
"""

# ============================================================================
# CONFIGURATION
# ============================================================================

# Default settings
CONFIG = {
    # Database
    'DATABASE': 'reminders.db',
    'AUTO_BACKUP': True,
    'BACKUP_INTERVAL': 7,  # days
    
    # Notifications
    'CHECK_INTERVAL': 60,  # seconds
    'NOTIFICATION_SOUND': True,
    'SOUND_FILE': None,  # None = system beep
    
    # UI
    'THEME': 'dark',
    'COLOR_THEME': 'blue',
    'WINDOW_GEOMETRY': '1400x850',
    'FONT_FAMILY': 'Arial',
    
    # Reminders
    'AUTO_COMPLETE_PAST': False,
    'SHOW_COMPLETED': True,
    'CLEANUP_DAYS': 30,
}

# Default categories
DEFAULT_CATEGORIES = [
    'Work',
    'Personal',
    'Health',
    'Shopping',
    'Finance',
    'Education',
    'Entertainment',
    'General'
]

# Priority levels
PRIORITY_LEVELS = ['Low', 'Normal', 'High']

# Time formats
TIME_FORMAT = '%H:%M'
DATE_FORMAT = '%Y-%m-%d'
DATETIME_FORMAT = '%Y-%m-%d %H:%M'

print(__doc__)
