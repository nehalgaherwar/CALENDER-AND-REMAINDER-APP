# Quick Start Guide 🚀

Get your Calendar and Reminder App up and running in minutes!

## Windows Users 🪟

### Option 1: Automatic Setup (Easiest)
1. Download all files to a folder
2. Double-click **`run.bat`**
3. The app will automatically:
   - Install all dependencies
   - Create the database
   - Launch the application

### Option 2: Manual Setup
```bash
# 1. Open Command Prompt in the app folder
# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
python main.py
```

---

## macOS / Linux Users 🍎🐧

### Option 1: Automatic Setup (Easiest)
```bash
# 1. Open Terminal in the app folder
# 2. Make script executable
chmod +x run.sh

# 3. Run setup script
./run.sh
```

### Option 2: Manual Setup
```bash
# 1. Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux

# 2. Install dependencies
pip3 install -r requirements.txt

# 3. Run the app
python3 main.py
```

---

## First-Time Use

### 1. Launch the App
Run using one of the methods above.

### 2. Add Your First Reminder
- Click **➕ Add Reminder** button
- Fill in the details:
  - **Title:** What is the reminder about?
  - **Description:** Any additional details
  - **Date:** When (YYYY-MM-DD format)
  - **Time:** What time (HH:MM format, 24-hour)
  - **Category:** Type of reminder
  - **Priority:** Urgency level
- Click **Save**

### 3. View Calendar
- Left side shows monthly calendar
- Green dates have reminders
- Click a date to see its reminders

### 4. Get Notifications
- Notifications check every minute
- When time arrives, popup appears
- Click "Mark as Done" when handled

---

## Common Tasks

### Adding a Reminder
```
1. Click ➕ Add Reminder
2. Fill form
3. Click Save
```

### Editing a Reminder
```
1. Select reminder from list
2. Click ✏️ Edit
3. Modify details
4. Click Save
```

### Deleting a Reminder
```
1. Select reminder from list
2. Click 🗑️ Delete
3. Confirm deletion
```

### Marking as Complete
```
1. Select reminder from list
2. Click ✓ Mark Done
3. Reminder marked complete
```

### Searching Reminders
```
1. Type in search box at top
2. Results appear instantly
3. Click reminder to view details
```

### Filtering by Category
```
1. Select category buttons below reminders
2. List filters automatically
3. Select "All" to show everything
```

---

## Date & Time Format

### Date Format: `YYYY-MM-DD`
- **2024-03-20** = March 20, 2024
- **2024-12-31** = December 31, 2024

### Time Format: `HH:MM` (24-hour)
- **09:00** = 9:00 AM
- **14:30** = 2:30 PM
- **23:59** = 11:59 PM

---

## Tips & Tricks

### 💡 Pro Tips

1. **Quick Add:** Press ➕ to add reminder from anywhere
2. **Color Codes:**
   - 🟩 Green reminders = Today or upcoming
   - 🟨 Yellow = Edited recently
   - 🟥 Red = High priority
3. **Keyboard:** Tab through dialog fields, Enter to save
4. **Search:** Searches both title and description
5. **Filter:** Use categories to organize reminders

### ⚡ Shortcuts

| Action | Method |
|--------|--------|
| Add Reminder | Click ➕ button |
| Search | Type in search box |
| Change Month | Click ◀ / ▶ |
| Select Date | Click date in calendar |
| Mark Done | Select & click ✓ |
| Delete | Select & click 🗑️ |

---

## Troubleshooting

### ❌ App Won't Start
**Solution:**
```bash
# Update CustomTkinter
pip install --upgrade customtkinter

# Try again
python main.py
```

### ❌ Dependencies Won't Install
**Solution:**
```bash
# Try minimal install
pip install customtkinter pillow tkcalendar

# If still fails, check Python version
python --version  # Should be 3.8+
```

### ❌ No Notifications
**Possible causes:**
- Time format incorrect (use HH:MM)
- Date is in the past
- App is minimized (bring to foreground)

**Solution:**
- Set reminder for a minute from now to test
- Check time format in dialog

### ❌ Database Error
**Solution:**
1. Close the app
2. Delete `reminders.db` file
3. Restart app (it will recreate database)

---

## Categories

### Pre-defined Categories
- 🏢 **Work** - Work-related tasks
- 👤 **Personal** - Personal tasks
- 💪 **Health** - Health and fitness
- 🛒 **Shopping** - Shopping lists
- 💰 **Finance** - Financial matters
- 📚 **Education** - Learning tasks
- 🎮 **Entertainment** - Fun activities
- 📝 **General** - Other reminders

---

## Priority Levels

| Priority | Color | Use Case |
|----------|-------|----------|
| **High** | 🔴 Red | Urgent, must do today |
| **Normal** | 🟠 Orange | Regular, important |
| **Low** | 🟢 Green | Can wait, flexible |

---

## Data Storage

All your reminders are stored in `reminders.db`:
- Located in the app folder
- Automatically created on first run
- Persistent across sessions
- Never needs manual updates

### Backup Recommended
Copy `reminders.db` to a safe location regularly.

---

## Getting Help

### Check the Documentation
- **README.md** - Full feature documentation
- **DEVELOPER.md** - Technical details
- **examples.py** - Code examples
- **This file** - Quick reference

### Common Issues & Solutions

| Problem | Solution |
|---------|----------|
| Forgot date format | Use YYYY-MM-DD |
| Forgot time format | Use HH:MM (24-hour) |
| Notification didn't show | Check system time |
| Database corrupted | Delete reminders.db |
| Slow performance | Close other apps |

---

## Next Steps

1. ✅ Install and launch app
2. ✅ Add a test reminder
3. ✅ Try editing it
4. ✅ Test search feature
5. ✅ Read README.md for advanced features

---

## Welcome! 👋

You're all set to start organizing your reminders!

**Questions?** Check README.md or DEVELOPER.md

**Ready to go?** Click that ➕ button and add your first reminder! 🎉

---

**Pro Tip:** Set your first reminder for a minute from now to test notifications! ⏰
