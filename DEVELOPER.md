# Developer Documentation

## Architecture Overview

The Calendar and Reminder App is built using a modular architecture with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────┐
│                    main.py (Entry Point)                │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│                  ui.py (GUI Layer)                      │
│  ├── CalendarAndReminderApp (Main Window)              │
│  ├── ReminderDialog (Add/Edit Dialog)                  │
│  └── UI Components                                      │
└──┬──────────────────────────────┬──────────────────────┘
   │                              │
   ▼                              ▼
┌──────────────────┐    ┌─────────────────────┐
│ database.py      │    │ notifications.py    │
│ (Data Layer)     │    │ (Alert Layer)       │
└──────────────────┘    └─────────────────────┘
   │                              │
   ▼                              ▼
┌──────────────────┐    ┌─────────────────────┐
│   SQLite DB      │    │ Background Thread   │
│ (reminders.db)   │    │ (Notification Loop) │
└──────────────────┘    └─────────────────────┘
         
              utils.py (Utilities)
         ├── DateUtils
         ├── PriorityColors
         └── CategoryColors
```

## Module Descriptions

### 1. main.py
**Purpose:** Application entry point
**Responsibilities:**
- Import UI module
- Initialize application
- Handle startup

**Key Functions:**
```python
def main():
    """Run the application."""
```

### 2. ui.py
**Purpose:** All GUI components and user interface logic
**Key Classes:**

#### CalendarAndReminderApp (ctk.CTk)
Main application window inheriting from CustomTkinter root widget.

**Key Methods:**
- `__init__()` - Initialize app, database, and notifications
- `create_ui()` - Create main UI layout
- `create_calendar_panel()` - Left panel with calendar
- `create_reminders_panel()` - Right panel with reminders list
- `update_calendar()` - Refresh calendar display
- `load_reminders()` - Load reminders from database
- `open_add_reminder_dialog()` - Show add reminder dialog
- `edit_reminder()` - Show edit dialog
- `delete_reminder()` - Remove reminder
- `search_reminders()` - Search by keyword
- `filter_reminders()` - Filter by category

**Key Attributes:**
- `db` - ReminderDatabase instance
- `notification_manager` - NotificationManager instance
- `current_month`, `current_year` - Current calendar view
- `selected_date` - Currently selected date
- `reminders_data` - Cached reminders list

#### ReminderDialog (ctk.CTkToplevel)
Modal dialog for adding/editing reminders.

**Key Methods:**
- `__init__()` - Initialize dialog
- `create_dialog_ui()` - Create form fields
- `save_reminder()` - Validate and save
- `cancel()` - Close without saving

### 3. database.py
**Purpose:** SQLite database operations and reminder management
**Key Class:** ReminderDatabase

**Methods:**
- `add_reminder()` - Insert new reminder
- `get_all_reminders()` - Retrieve all reminders
- `get_reminders_by_date()` - Get reminders for specific date
- `get_reminders_by_category()` - Filter by category
- `search_reminders()` - Full-text search
- `update_reminder()` - Modify existing reminder
- `delete_reminder()` - Remove reminder
- `get_reminder_by_id()` - Retrieve single reminder
- `get_upcoming_reminders()` - Get next N days
- `get_categories()` - List unique categories

**Database Schema:**
```
reminders
├── id (INTEGER PRIMARY KEY)
├── title (TEXT) - Reminder title
├── description (TEXT) - Detailed description
├── date (TEXT) - YYYY-MM-DD format
├── time (TEXT) - HH:MM format
├── category (TEXT) - Category name
├── priority (TEXT) - Low/Normal/High
├── is_completed (INTEGER) - 0/1 flag
├── created_at (TIMESTAMP)
└── updated_at (TIMESTAMP)
```

### 4. notifications.py
**Purpose:** Handle reminder notifications and alerts
**Key Classes:**

#### NotificationManager
Manages background reminder checking and notifications.

**Methods:**
- `start()` - Begin monitoring (threaded)
- `stop()` - Stop monitoring
- `set_reminders()` - Update reminder list
- `add_notification_callback()` - Register callback
- `show_notification_popup()` - Display popup alert
- `play_notification_sound()` - Play system sound

**Threading:**
- Runs background check loop every 60 seconds
- Triggers callbacks when reminders are due
- Non-blocking with daemon thread

#### ReminderAlert
Static methods for displaying alert windows.

**Methods:**
- `show_alert()` - Display styled alert popup

### 5. utils.py
**Purpose:** Utility functions and helpers
**Key Classes:**

#### DateUtils
Static methods for date operations.

**Methods:**
- `get_current_date()` - Current date YYYY-MM-DD
- `get_current_time()` - Current time HH:MM
- `format_date()` - Convert to readable format
- `format_datetime()` - Format date and time
- `is_past_due()` - Check if reminder past due
- `get_day_name()` - Get weekday name
- `get_month_calendar()` - Get month data
- `add_days()` - Add/subtract days

#### PriorityColors
Color scheme for priority levels.

**Attributes:**
```python
COLORS = {
    "High": "#FF6B6B",      # Red
    "Normal": "#FFA500",    # Orange
    "Low": "#4CAF50"        # Green
}
```

#### CategoryColors
Color scheme for categories.

**Attributes:**
```python
COLORS = {
    "Work": "#2196F3",
    "Personal": "#9C27B0",
    "Health": "#4CAF50",
    # ... more categories
}
```

## Data Flow

### Adding a Reminder
```
User clicks "Add Reminder"
    ↓
ReminderDialog opens
    ↓
User fills form and clicks Save
    ↓
Dialog validates input
    ↓
database.add_reminder() called
    ↓
SQLite INSERT executed
    ↓
notification_manager.set_reminders() updated
    ↓
UI refreshed (calendar and list)
```

### Notification Flow
```
Background thread checks every 60 seconds
    ↓
Compares reminder date/time with current
    ↓
Match found - reminder is due
    ↓
Callbacks triggered
    ↓
ReminderAlert.show_alert() displayed
    ↓
Sound plays (if available)
    ↓
User marks as done or snoozes
```

## Extending the Application

### Adding a New Category

Edit `utils.py`:
```python
class CategoryColors:
    COLORS = {
        "NewCategory": "#HEXCOLOR",  # Add this line
        # ... existing categories
    }
```

### Adding a New Priority Level

Edit `utils.py` and `ui.py`:
```python
# In utils.py
PriorityColors.COLORS["Custom"] = "#HEXCOLOR"

# In database.py - update schema if needed
# In ui.py - update dialog options
```

### Adding a New Feature

1. **Database Feature:**
   ```python
   # In database.py, add to ReminderDatabase class
   def new_method(self, params):
       # SQLite operations
       pass
   ```

2. **UI Feature:**
   ```python
   # In ui.py, add to CalendarAndReminderApp class
   def new_feature(self):
       # UI logic
       pass
   ```

3. **Utility Support:**
   ```python
   # In utils.py, create helper class/methods
   class NewUtils:
       @staticmethod
       def helper_method(params):
           pass
   ```

### Custom Notification Sounds

Edit `notifications.py`:
```python
def play_notification_sound(self):
    """Play a notification sound."""
    try:
        from playsound import playsound
        playsound('path/to/sound.wav')
    except Exception as e:
        print(f"Could not play sound: {e}")
```

### Recurring Reminders

Example extension to database schema:
```python
# Add to reminders table:
# - recurrence_pattern TEXT (daily/weekly/monthly)
# - recurrence_end_date TEXT
# - original_reminder_id INTEGER (for instances)

def get_recurring_instances(self, reminder_id):
    """Generate recurring reminder instances."""
    pass
```

## Error Handling

### Database Errors
```python
try:
    self.cursor.execute(...)
except sqlite3.Error as e:
    print(f"Database error: {e}")
    return None  # or default value
```

### UI Errors
```python
try:
    # UI operation
except Exception as e:
    messagebox.showerror("Error", str(e))
```

### Threading Errors
```python
while self.active:
    try:
        self._check_due_reminders()
    except Exception as e:
        print(f"Error in loop: {e}")
```

## Performance Considerations

1. **Database Queries:**
   - Use indexes on frequently queried columns (date, category)
   - Batch operations when possible
   - Close database connections properly

2. **GUI Updates:**
   - Use `after()` for thread-safe GUI updates
   - Avoid blocking UI thread during database operations
   - Cache frequently accessed data

3. **Notifications:**
   - Background thread with 60-second interval balances responsiveness and CPU usage
   - Consider adjusting interval based on use case

4. **Memory:**
   - Store database connections at class level
   - Properly close connections in destructors
   - Clear large data structures when no longer needed

## Testing

### Unit Test Example
```python
import unittest
from database import ReminderDatabase

class TestReminderDatabase(unittest.TestCase):
    def setUp(self):
        self.db = ReminderDatabase(":memory:")
    
    def test_add_reminder(self):
        reminder_id = self.db.add_reminder(
            "Test", "Description", "2024-01-01", "10:00"
        )
        self.assertGreater(reminder_id, 0)
    
    def tearDown(self):
        self.db.close()

if __name__ == '__main__':
    unittest.main()
```

## Deployment

### Creating Executable (Windows)

Using PyInstaller:
```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "Calendar Reminder" main.py
```

### Distribution
- Include README.md
- Include requirements.txt
- Include database schema documentation
- Create installer script

## Version Control

Recommended `.gitignore`:
```
reminders.db
*.pyc
__pycache__/
venv/
*.egg-info/
dist/
build/
.DS_Store
```

## Documentation Best Practices

1. **Docstrings:** Use Google-style docstrings
```python
def method_name(self, param):
    """
    Brief description.
    
    Args:
        param: Parameter description
    
    Returns:
        Return value description
    """
```

2. **Comments:** Explain WHY, not WHAT
```python
# Bad: Set count to 0
count = 0

# Good: Initialize counter before loop
count = 0
```

3. **Type Hints:** Use for clarity
```python
def method(self, param: str) -> bool:
    pass
```

## Future Roadmap

- [ ] Recurring reminders
- [ ] Email notifications
- [ ] iCalendar import/export
- [ ] Multiple reminder times
- [ ] Custom notification sounds
- [ ] Multi-user support
- [ ] Cloud synchronization
- [ ] Dark/Light theme toggle
- [ ] Timezone support
- [ ] Reminder templates

---

**Last Updated:** 2024
**Version:** 1.0
