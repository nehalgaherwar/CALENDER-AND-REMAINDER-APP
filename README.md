# 📅 Calendar and Reminder App

A modern, feature-rich Python application for managing calendar events and reminders with an elegant dark mode GUI.

## Features

✨ **Core Features:**
- 📆 Monthly calendar view with easy navigation
- ➕ Add, edit, and delete reminders
- 🔔 Notification/reminder alerts with popup notifications
- 💾 SQLite database for persistent reminder storage
- 🎨 Dark mode modern UI using CustomTkinter
- 🔍 Search reminders by title or description
- 📂 Organize reminders by category (Work, Personal, Health, etc.)
- 🎯 Priority levels (Low, Normal, High)
- ⏰ Date and time picker interface
- 🔗 Filter reminders by category

## Requirements

- Python 3.8 or higher
- All dependencies listed in `requirements.txt`

## Installation

### 1. Clone/Download the Project

```bash
cd "calendar and remender app"
```

### 2. Create a Virtual Environment (Recommended)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**Note:** If you encounter issues with `pyaudio`, you can skip it:
```bash
pip install customtkinter pillow tkcalendar playsound
```

## Usage

### Starting the Application

```bash
python main.py
```

### How to Use

#### 1. **View Calendar**
- Navigate months using ◀ Prev and Next ▶ buttons
- Dates with reminders are highlighted in green
- Click any date to view its reminders

#### 2. **Add a Reminder**
- Click the ➕ **Add Reminder** button in the top bar
- Fill in the reminder details:
  - **Title:** Brief reminder title
  - **Description:** Detailed information
  - **Date:** Select in YYYY-MM-DD format
  - **Time:** Set in HH:MM format (24-hour)
  - **Category:** Choose from predefined categories
  - **Priority:** Low, Normal, or High
- Click **Save** to create the reminder

#### 3. **Edit a Reminder**
- Select a reminder from the list
- Click ✏️ **Edit**
- Modify the details
- Click **Save**

#### 4. **Delete a Reminder**
- Select a reminder from the list
- Click 🗑️ **Delete**
- Confirm deletion

#### 5. **Mark Reminder as Complete**
- Select a reminder from the list
- Click ✓ **Mark Done**

#### 6. **Search Reminders**
- Use the search bar at the top
- Type keywords to find reminders
- Press Enter or click 🔍 **Search**

#### 7. **Filter by Category**
- Use the category filter buttons below the reminder list
- Select: All, Work, Personal, Health, or Other

#### 8. **Receive Notifications**
- Notifications are checked every 60 seconds
- When a reminder's time arrives, a popup notification appears
- The app plays a notification sound (if audio is available)

## Project Structure

```
calendar and remender app/
├── main.py                 # Application entry point
├── ui.py                   # GUI implementation (CustomTkinter)
├── database.py             # SQLite database operations
├── notifications.py        # Notification and alert system
├── utils.py                # Utility functions and helpers
├── requirements.txt        # Python package dependencies
├── reminders.db            # SQLite database (created on first run)
└── README.md              # This file
```

## Database Schema

### Reminders Table

```sql
CREATE TABLE reminders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    date TEXT NOT NULL,           -- YYYY-MM-DD format
    time TEXT NOT NULL,           -- HH:MM format
    category TEXT DEFAULT 'General',
    priority TEXT DEFAULT 'Normal',
    is_completed INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Categories

Default categories available:
- Work
- Personal
- Health
- Shopping
- Finance
- Education
- Entertainment
- General

## Priority Levels

- **High** - Red color, urgent reminders
- **Normal** - Orange color, standard reminders
- **Low** - Green color, low-priority reminders

## Color Theme

The app uses a professional dark theme:
- Background: Dark gray (#1a1a1a)
- Accent: Blue (#2196F3)
- Success: Green (#4CAF50)
- Warning: Red (#FF6B6B)
- Calendar dates with reminders: Green highlight

## Features Explanation

### Calendar View
- Left panel displays a monthly calendar
- Green highlighted dates indicate days with reminders
- Click any date to view all reminders for that day
- Navigate between months using Previous/Next buttons

### Reminder Management
- Right panel displays reminders for selected date
- Add new reminders with customizable details
- Edit existing reminders with all fields modifiable
- Delete reminders with confirmation
- Mark reminders as complete without deletion

### Search Function
- Real-time search as you type
- Searches in reminder titles and descriptions
- Shows all matching results

### Notifications
- Automatic background checking every 60 seconds
- Popup notifications when reminder time arrives
- Shows reminder title, time, and description
- Sound alert (Windows systems)
- Options to mark as done or snooze

## Troubleshooting

### Issue: Application won't start
**Solution:** Ensure Python 3.8+ is installed and all packages from requirements.txt are installed

### Issue: CustomTkinter not working
**Solution:** 
```bash
pip uninstall customtkinter
pip install --upgrade customtkinter
```

### Issue: No notifications appearing
**Solution:** Ensure the reminder time is set correctly in HH:MM format and the date is today or later

### Issue: Database errors
**Solution:** The database file (reminders.db) is created automatically. If corrupted, delete it and restart the app

## Development

### Dependencies Used

- **customtkinter** - Modern GUI framework (replaces tkinter)
- **pillow** - Image processing
- **tkcalendar** - Calendar widget support
- **playsound** - Audio notifications
- **sqlite3** - Built-in database (no installation needed)

### Module Descriptions

1. **main.py** - Entry point, minimal setup
2. **ui.py** - Complete GUI implementation with all windows and dialogs
3. **database.py** - SQLite ORM-like wrapper for database operations
4. **notifications.py** - Notification management and alert system
5. **utils.py** - Date utilities, color mappings, priority/category helpers

## Tips and Tricks

1. **Quick Add:** Use the ➕ button to quickly add reminders
2. **Keyboard Shortcuts:** Tab between fields in dialogs
3. **Date Navigation:** Click dates to see all reminders for that day
4. **Bulk Operations:** Filter by category to manage similar reminders
5. **Past Reminders:** Completed reminders can be marked done to track history

## Known Limitations

- Recurring reminders are not yet implemented
- Sound notifications require audio output device
- Maximum reminder description is limited by UI display
- No email or push notifications (local popups only)

## Future Enhancements

- [ ] Recurring reminders (daily, weekly, monthly)
- [ ] Email notifications
- [ ] Import/export to iCalendar format
- [ ] Multiple reminder times per day
- [ ] Customizable notification sounds
- [ ] Reminder templates
- [ ] Multi-user support
- [ ] Cloud sync capability
- [ ] Mobile app version

## License

This project is provided as-is for personal and educational use.

## Support

For issues or questions, ensure:
1. All dependencies are properly installed
2. Python version is 3.8 or higher
3. Database file has proper permissions
4. System time is correctly set

## Author

Created as a comprehensive Python application demonstrating:
- GUI development with CustomTkinter
- SQLite database management
- Threading for background tasks
- Event handling and notifications
- Modern dark mode UI design

---

**Enjoy organizing your reminders! 📝✨**
