"""
Main GUI module using CustomTkinter for modern dark mode interface.
Enhanced with improved UX/UI and modern design patterns.
"""

import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
import calendar as cal
from database import ReminderDatabase
from notifications import NotificationManager, ReminderAlert
from utils import DateUtils, PriorityColors, CategoryColors
import tkinter as tk


class CalendarAndReminderApp(ctk.CTk):
    """Main application class."""
    
    # Color Palette
    COLOR_PRIMARY = "#0D47A1"
    COLOR_SECONDARY = "#1565C0"
    COLOR_ACCENT = "#00BCD4"
    COLOR_SUCCESS = "#4CAF50"
    COLOR_WARNING = "#FFC107"
    COLOR_DANGER = "#F44336"
    COLOR_BG_DARK = "#121212"
    COLOR_SURFACE = "#1E1E1E"
    COLOR_SURFACE_VARIANT = "#2D2D2D"
    COLOR_TEXT_PRIMARY = "#FFFFFF"
    COLOR_TEXT_SECONDARY = "#B0B0B0"
    
    def __init__(self):
        """Initialize the application."""
        super().__init__()
        
        # Configure appearance
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Window configuration
        self.title("📅 Calendar & Reminder Manager")
        self.geometry("1600x900")
        self.minsize(1400, 800)
        
        # Initialize database and notifications
        self.db = ReminderDatabase("reminders.db")
        self.notification_manager = NotificationManager()
        self.notification_manager.add_notification_callback(self.on_reminder_due)
        self.notification_manager.start()
        
        # Variables
        self.current_month = datetime.now().month
        self.current_year = datetime.now().year
        self.selected_date = None
        self.reminders_data = []
        
        # Setup UI
        self.configure(fg_color=self.COLOR_BG_DARK)
        self.create_ui()
        self.load_reminders()
        
        # Handle app close
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def create_ui(self):
        """Create the user interface."""
        # Main container
        main_container = ctk.CTkFrame(self, fg_color=self.COLOR_BG_DARK)
        main_container.pack(fill="both", expand=True, padx=0, pady=0)
        
        # Top bar
        self.create_top_bar(main_container)
        
        # Main content area with gradient effect
        content_frame = ctk.CTkFrame(main_container, fg_color=self.COLOR_BG_DARK)
        content_frame.pack(fill="both", expand=True, padx=12, pady=12)
        content_frame.grid_columnconfigure(0, weight=45)
        content_frame.grid_columnconfigure(1, weight=55)
        content_frame.grid_rowconfigure(0, weight=1)
        
        # Left panel - Calendar (slightly narrower)
        self.create_calendar_panel(content_frame)
        
        # Right panel - Reminders (wider for better visibility)
        self.create_reminders_panel(content_frame)
    
    def create_top_bar(self, parent):
        """Create top navigation bar with modern styling."""
        top_bar = ctk.CTkFrame(parent, fg_color=self.COLOR_SURFACE, height=70, corner_radius=12)
        top_bar.pack(fill="x", padx=0, pady=(0, 12))
        top_bar.grid_columnconfigure(1, weight=1)
        
        # App title with icon
        title_frame = ctk.CTkFrame(top_bar, fg_color="transparent")
        title_frame.grid(row=0, column=0, padx=20, pady=15, sticky="w")
        
        title_label = ctk.CTkLabel(
            title_frame,
            text="📅 Calendar & Reminder Manager",
            font=("Segoe UI", 22, "bold"),
            text_color=self.COLOR_TEXT_PRIMARY
        )
        title_label.pack()
        
        # Right side controls
        control_frame = ctk.CTkFrame(top_bar, fg_color="transparent")
        control_frame.grid(row=0, column=1, padx=20, pady=15, sticky="e")
        
        # Search frame with modern styling
        search_frame = ctk.CTkFrame(control_frame, fg_color=self.COLOR_SURFACE_VARIANT, corner_radius=8)
        search_frame.pack(side="left", padx=10)
        
        self.search_var = ctk.StringVar()
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="🔍 Search reminders...",
            textvariable=self.search_var,
            width=250,
            font=("Segoe UI", 11),
            fg_color=self.COLOR_SURFACE_VARIANT,
            border_width=0
        )
        self.search_entry.pack(padx=12, pady=8)
        self.search_entry.bind("<KeyRelease>", lambda e: self.search_reminders())
        
        # Add reminder button
        add_btn = ctk.CTkButton(
            control_frame,
            text="➕ Add Reminder",
            command=self.open_add_reminder_dialog,
            width=140,
            font=("Segoe UI", 11, "bold"),
            fg_color=self.COLOR_SUCCESS,
            hover_color="#45a049",
            corner_radius=8,
            height=38
        )
        add_btn.pack(side="left", padx=10)
    
    def create_calendar_panel(self, parent):
        """Create calendar panel on the left with modern styling."""
        # Main calendar container with card style
        calendar_frame = ctk.CTkFrame(parent, fg_color=self.COLOR_SURFACE, corner_radius=12)
        calendar_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 12))
        calendar_frame.grid_rowconfigure(1, weight=1)
        calendar_frame.grid_columnconfigure(0, weight=1)
        
        # Calendar header with better styling
        header_frame = ctk.CTkFrame(calendar_frame, fg_color=self.COLOR_SURFACE_VARIANT, corner_radius=8)
        header_frame.pack(fill="x", padx=12, pady=12)
        header_frame.grid_columnconfigure(1, weight=1)
        
        # Previous month button
        prev_btn = ctk.CTkButton(
            header_frame,
            text="◀ Prev",
            command=self.previous_month,
            width=70,
            font=("Segoe UI", 10, "bold"),
            fg_color=self.COLOR_PRIMARY,
            hover_color=self.COLOR_SECONDARY,
            corner_radius=6,
            height=32
        )
        prev_btn.grid(row=0, column=0, padx=5, pady=8)
        
        # Month and year label
        self.month_year_label = ctk.CTkLabel(
            header_frame,
            text="",
            font=("Segoe UI", 16, "bold"),
            text_color=self.COLOR_TEXT_PRIMARY
        )
        self.month_year_label.grid(row=0, column=1, padx=20, pady=8)
        
        # Next month button
        next_btn = ctk.CTkButton(
            header_frame,
            text="Next ▶",
            command=self.next_month,
            width=70,
            font=("Segoe UI", 10, "bold"),
            fg_color=self.COLOR_PRIMARY,
            hover_color=self.COLOR_SECONDARY,
            corner_radius=6,
            height=32
        )
        next_btn.grid(row=0, column=2, padx=5, pady=8)
        
        # Calendar grid with padding
        calendar_grid_frame = ctk.CTkFrame(calendar_frame, fg_color="transparent")
        calendar_grid_frame.pack(fill="both", expand=True, padx=12, pady=12)
        
        self.calendar_frame = ctk.CTkFrame(calendar_grid_frame, fg_color="transparent")
        self.calendar_frame.pack(fill="both", expand=True)
        
        self.update_calendar()
    
    def create_reminders_panel(self, parent):
        """Create reminders panel on the right with modern card design."""
        reminders_frame = ctk.CTkFrame(parent, fg_color=self.COLOR_SURFACE, corner_radius=12)
        reminders_frame.grid(row=0, column=1, sticky="nsew")
        reminders_frame.grid_rowconfigure(2, weight=1)
        reminders_frame.grid_columnconfigure(0, weight=1)
        
        # Header with icon
        header_container = ctk.CTkFrame(reminders_frame, fg_color="transparent")
        header_container.pack(fill="x", padx=12, pady=12)
        
        header = ctk.CTkLabel(
            header_container,
            text="📝 My Reminders",
            font=("Segoe UI", 18, "bold"),
            text_color=self.COLOR_TEXT_PRIMARY
        )
        header.pack(anchor="w")
        
        # Filter buttons with better styling
        filter_frame = ctk.CTkFrame(reminders_frame, fg_color="transparent")
        filter_frame.pack(fill="x", padx=12, pady=(0, 12))
        
        filter_label = ctk.CTkLabel(
            filter_frame,
            text="Filter by Category:",
            font=("Segoe UI", 10, "bold"),
            text_color=self.COLOR_TEXT_SECONDARY
        )
        filter_label.pack(anchor="w", pady=(0, 6))
        
        categories_frame = ctk.CTkFrame(filter_frame, fg_color="transparent")
        categories_frame.pack(fill="x")
        
        self.filter_var = ctk.StringVar(value="All")
        
        filter_options = ["All", "Work", "Personal", "Health", "Shopping", "Finance", "Education", "Entertainment"]
        for idx, option in enumerate(filter_options):
            radio_btn = ctk.CTkRadioButton(
                categories_frame,
                text=option,
                variable=self.filter_var,
                value=option,
                command=self.filter_reminders,
                font=("Segoe UI", 10),
                fg_color=self.COLOR_PRIMARY,
                hover_color=self.COLOR_SECONDARY
            )
            radio_btn.grid(row=idx // 4, column=idx % 4, padx=5, pady=3, sticky="w")
        
        categories_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        # Reminders list with scrollbar - using custom scrollable frame
        list_frame = ctk.CTkFrame(reminders_frame, fg_color="transparent")
        list_frame.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        list_frame.grid_rowconfigure(0, weight=1)
        list_frame.grid_columnconfigure(0, weight=1)
        
        # Create a canvas-based scrollable frame for better styling
        self.reminders_container = ctk.CTkFrame(list_frame, fg_color=self.COLOR_SURFACE_VARIANT, corner_radius=8)
        self.reminders_container.grid(row=0, column=0, sticky="nsew")
        self.reminders_container.grid_columnconfigure(0, weight=1)
        
        self.reminders_listbox = tk.Listbox(
            self.reminders_container,
            yscrollcommand=self._on_scroll,
            bg=self.COLOR_SURFACE_VARIANT,
            fg=self.COLOR_TEXT_PRIMARY,
            font=("Segoe UI", 10),
            border=0,
            highlightthickness=0,
            relief="flat",
            activestyle="none",
            selectmode="SINGLE"
        )
        self.reminders_listbox.pack(fill="both", expand=True, padx=8, pady=8)
        self.reminders_listbox.bind("<<ListboxSelect>>", self.on_reminder_select)
        self.reminders_listbox.bind("<Button-1>", self._on_listbox_click)
        
        # Buttons frame with modern styling
        button_frame = ctk.CTkFrame(reminders_frame, fg_color="transparent")
        button_frame.pack(fill="x", padx=12, pady=12)
        button_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        edit_btn = ctk.CTkButton(
            button_frame,
            text="✏️ Edit",
            command=self.edit_reminder,
            font=("Segoe UI", 11, "bold"),
            fg_color=self.COLOR_PRIMARY,
            hover_color=self.COLOR_SECONDARY,
            corner_radius=8,
            height=36
        )
        edit_btn.grid(row=0, column=0, padx=4, sticky="ew")
        
        complete_btn = ctk.CTkButton(
            button_frame,
            text="✓ Mark Done",
            command=self.mark_reminder_complete,
            font=("Segoe UI", 11, "bold"),
            fg_color=self.COLOR_SUCCESS,
            hover_color="#45a049",
            corner_radius=8,
            height=36
        )
        complete_btn.grid(row=0, column=1, padx=4, sticky="ew")
        
        delete_btn = ctk.CTkButton(
            button_frame,
            text="🗑️ Delete",
            command=self.delete_reminder,
            font=("Segoe UI", 11, "bold"),
            fg_color=self.COLOR_DANGER,
            hover_color="#da190b",
            corner_radius=8,
            height=36
        )
        delete_btn.grid(row=0, column=2, padx=4, sticky="ew")
    
    def _on_scroll(self, *args):
        """Handle scrollbar movement."""
        pass
    
    def _on_listbox_click(self, event):
        """Handle listbox click for better interaction."""
        pass
    
    def update_calendar(self):
        """Update calendar display with enhanced styling."""
        # Clear previous calendar
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()
        
        # Update header
        month_name = DateUtils.get_month_name(self.current_month)
        self.month_year_label.configure(text=f"{month_name} {self.current_year}")
        
        # Create day headers with better styling
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for i, day in enumerate(days):
            day_label = ctk.CTkLabel(
                self.calendar_frame,
                text=day,
                font=("Segoe UI", 10, "bold"),
                text_color=self.COLOR_TEXT_SECONDARY
            )
            day_label.grid(row=0, column=i, padx=3, pady=6, sticky="nsew")
        
        # Get calendar data
        weeks = cal.monthcalendar(self.current_year, self.current_month)
        
        for week_num, week in enumerate(weeks, start=1):
            for day_num, day in enumerate(week):
                if day == 0:
                    empty_label = ctk.CTkLabel(
                        self.calendar_frame,
                        text="",
                        fg_color="transparent"
                    )
                    empty_label.grid(row=week_num, column=day_num, padx=3, pady=6, sticky="nsew")
                    continue
                
                # Create date string
                date_str = f"{self.current_year}-{self.current_month:02d}-{day:02d}"
                
                # Check if date has reminders
                date_reminders = self.db.get_reminders_by_date(date_str)
                has_reminders = len(date_reminders) > 0
                is_today = date_str == DateUtils.get_current_date()
                is_selected = date_str == self.selected_date
                
                # Determine button color based on state
                if is_selected:
                    btn_color = self.COLOR_ACCENT
                    hover_color = "#00ACC1"
                elif is_today:
                    btn_color = self.COLOR_PRIMARY
                    hover_color = self.COLOR_SECONDARY
                elif has_reminders:
                    btn_color = self.COLOR_SUCCESS
                    hover_color = "#45a049"
                else:
                    btn_color = self.COLOR_SURFACE_VARIANT
                    hover_color = "#3D3D3D"
                
                # Add visual indicator for reminders
                display_text = str(day)
                if has_reminders:
                    display_text = f"{day} •"  # Dot indicator
                
                # Create date button with corner radius
                date_btn = ctk.CTkButton(
                    self.calendar_frame,
                    text=display_text,
                    fg_color=btn_color,
                    hover_color=hover_color,
                    text_color=self.COLOR_TEXT_PRIMARY,
                    command=lambda d=day, date=date_str: self.select_date(date),
                    font=("Segoe UI", 10, "bold"),
                    corner_radius=6,
                    height=40
                )
                date_btn.grid(row=week_num, column=day_num, padx=3, pady=6, sticky="nsew")
        
        # Configure grid weights
        for i in range(len(days)):
            self.calendar_frame.grid_columnconfigure(i, weight=1)
        for i in range(len(weeks) + 1):
            self.calendar_frame.grid_rowconfigure(i, weight=1)
    
    def select_date(self, date: str):
        """Select a date and show its reminders."""
        self.selected_date = date
        self.update_calendar()
        self.show_date_reminders(date)
    
    def show_date_reminders(self, date: str):
        """Show reminders for a specific date with enhanced formatting."""
        reminders = self.db.get_reminders_by_date(date)
        self.reminders_listbox.delete(0, tk.END)
        
        date_formatted = DateUtils.format_date(date)
        day_name = DateUtils.get_day_name(date)
        
        # Header with better styling
        header_text = f"  📅 {day_name}, {date_formatted}"
        self.reminders_listbox.insert(tk.END, header_text)
        self.reminders_listbox.itemconfig(0, {'bg': self.COLOR_PRIMARY, 'fg': self.COLOR_TEXT_PRIMARY})
        
        if reminders:
            for reminder in reminders:
                # Priority emoji
                priority_icon = "🔴" if reminder['priority'] == "High" else "🟡" if reminder['priority'] == "Normal" else "🟢"
                # Completion indicator
                completion_status = "✓" if reminder.get('is_completed') else "○"
                
                reminder_text = f"  {completion_status} {priority_icon} [{reminder['time']}] {reminder['title']}"
                self.reminders_listbox.insert(tk.END, reminder_text)
                
                # Color code by priority
                if reminder['priority'] == "High":
                    bg_color = "#3d1a1a"
                elif reminder['priority'] == "Normal":
                    bg_color = "#3d2a1a"
                else:
                    bg_color = "#1a3d1a"
                
                self.reminders_listbox.itemconfig(tk.END, {'bg': bg_color, 'fg': self.COLOR_TEXT_PRIMARY})
        else:
            self.reminders_listbox.insert(tk.END, "  ✨ No reminders for this date")
            self.reminders_listbox.itemconfig(tk.END, {'bg': self.COLOR_SURFACE_VARIANT, 'fg': self.COLOR_TEXT_SECONDARY})
    
    def load_reminders(self):
        """Load all reminders from database."""
        self.reminders_data = self.db.get_all_reminders()
        self.notification_manager.set_reminders(self.reminders_data)
        self.update_reminders_display()
    
    def update_reminders_display(self):
        """Update reminders display."""
        if self.selected_date:
            self.show_date_reminders(self.selected_date)
        else:
            self.show_all_reminders()
    
    def show_all_reminders(self):
        """Show all reminders with enhanced formatting."""
        self.reminders_listbox.delete(0, tk.END)
        reminders = self.db.get_all_reminders()
        
        if reminders:
            self.reminders_listbox.insert(tk.END, f"  📋 All Reminders ({len(reminders)} total)")
            self.reminders_listbox.itemconfig(0, {'bg': self.COLOR_PRIMARY, 'fg': self.COLOR_TEXT_PRIMARY})
            
            for reminder in reminders:
                # Priority emoji and color
                if reminder['priority'] == "High":
                    priority_icon = "🔴"
                    color = "#3d1a1a"
                elif reminder['priority'] == "Normal":
                    priority_icon = "🟡"
                    color = "#3d2a1a"
                else:
                    priority_icon = "🟢"
                    color = "#1a3d1a"
                
                # Completion indicator
                completion_status = "✓" if reminder.get('is_completed') else "○"
                
                # Category emoji mapping
                category_emoji = {
                    "Work": "💼",
                    "Personal": "👤",
                    "Health": "🏥",
                    "Shopping": "🛒",
                    "Finance": "💰",
                    "Education": "📚",
                    "Entertainment": "🎭",
                    "General": "📌"
                }
                cat_emoji = category_emoji.get(reminder['category'], "📌")
                
                reminder_text = (
                    f"  {completion_status} {priority_icon} {cat_emoji} [{reminder['date']} {reminder['time']}] {reminder['title']}"
                )
                self.reminders_listbox.insert(tk.END, reminder_text)
                self.reminders_listbox.itemconfig(tk.END, {'bg': color, 'fg': self.COLOR_TEXT_PRIMARY})
        else:
            self.reminders_listbox.insert(tk.END, "  📭 No reminders yet")
            self.reminders_listbox.itemconfig(tk.END, {'bg': self.COLOR_SURFACE_VARIANT, 'fg': self.COLOR_TEXT_SECONDARY})
    
    def open_add_reminder_dialog(self):
        """Open dialog to add new reminder."""
        dialog = ReminderDialog(self, "Add Reminder")
        if dialog.result:
            title, description, date, time, category, priority = dialog.result
            reminder_id = self.db.add_reminder(
                title, description, date, time, category, priority
            )
            if reminder_id > 0:
                messagebox.showinfo("Success", "Reminder added successfully!")
                self.load_reminders()
                if date == self.selected_date or self.selected_date is None:
                    self.update_calendar()
            else:
                messagebox.showerror("Error", "Failed to add reminder")
    
    def edit_reminder(self):
        """Edit selected reminder."""
        selection = self.reminders_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a reminder to edit")
            return
        
        index = selection[0]
        if index == 0:
            messagebox.showwarning("Warning", "Please select a valid reminder")
            return
        
        reminders = self.db.get_reminders_by_date(self.selected_date)
        if index - 1 < len(reminders):
            reminder = reminders[index - 1]
            dialog = ReminderDialog(self, "Edit Reminder", reminder)
            if dialog.result:
                title, description, date, time, category, priority = dialog.result
                self.db.update_reminder(
                    reminder['id'],
                    title=title,
                    description=description,
                    date=date,
                    time=time,
                    category=category,
                    priority=priority
                )
                messagebox.showinfo("Success", "Reminder updated successfully!")
                self.load_reminders()
                self.update_calendar()
    
    def delete_reminder(self):
        """Delete selected reminder."""
        selection = self.reminders_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a reminder to delete")
            return
        
        index = selection[0]
        if index == 0:
            messagebox.showwarning("Warning", "Please select a valid reminder")
            return
        
        if messagebox.askyesno("Confirm", "Delete this reminder?"):
            reminders = self.db.get_reminders_by_date(self.selected_date)
            if index - 1 < len(reminders):
                reminder_id = reminders[index - 1]['id']
                self.db.delete_reminder(reminder_id)
                messagebox.showinfo("Success", "Reminder deleted!")
                self.load_reminders()
                self.update_calendar()
    
    def mark_reminder_complete(self):
        """Mark selected reminder as complete."""
        selection = self.reminders_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a reminder")
            return
        
        index = selection[0]
        if index == 0:
            return
        
        reminders = self.db.get_reminders_by_date(self.selected_date)
        if index - 1 < len(reminders):
            reminder = reminders[index - 1]
            self.db.update_reminder(reminder['id'], is_completed=1)
            messagebox.showinfo("Success", "Reminder marked as complete!")
            self.load_reminders()
    
    def on_reminder_select(self, event):
        """Handle reminder selection."""
        pass
    
    def search_reminders(self):
        """Search reminders by keyword."""
        query = self.search_var.get().strip()
        self.reminders_listbox.delete(0, tk.END)
        
        if query:
            results = self.db.search_reminders(query)
            if results:
                self.reminders_listbox.insert(tk.END, f"Search Results for: '{query}'")
                self.reminders_listbox.itemconfig(0, {'bg': '#2196F3'})
                for reminder in results:
                    reminder_text = (
                        f"[{reminder['date']} {reminder['time']}] "
                        f"{reminder['title']}"
                    )
                    self.reminders_listbox.insert(tk.END, reminder_text)
            else:
                self.reminders_listbox.insert(tk.END, "No results found")
        else:
            self.update_reminders_display()
    
    def filter_reminders(self):
        """Filter reminders by category."""
        filter_val = self.filter_var.get()
        self.reminders_listbox.delete(0, tk.END)
        
        if filter_val == "All":
            self.show_all_reminders()
        else:
            reminders = self.db.get_reminders_by_category(filter_val)
            if reminders:
                for reminder in reminders:
                    reminder_text = (
                        f"[{reminder['time']}] {reminder['title']} "
                        f"({reminder['date']})"
                    )
                    self.reminders_listbox.insert(tk.END, reminder_text)
            else:
                self.reminders_listbox.insert(tk.END, f"No reminders in {filter_val}")
    
    def previous_month(self):
        """Navigate to previous month."""
        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1
        self.update_calendar()
    
    def next_month(self):
        """Navigate to next month."""
        if self.current_month == 12:
            self.current_month = 1
            self.current_year += 1
        else:
            self.current_month += 1
        self.update_calendar()
    
    def on_reminder_due(self, reminder: dict):
        """Handle reminder due notification."""
        try:
            def show_alert():
                ReminderAlert.show_alert(self, reminder)
            
            self.after(0, show_alert)
        except Exception as e:
            print(f"Error showing alert: {e}")
    
    def on_closing(self):
        """Handle application closing."""
        self.notification_manager.stop()
        self.db.close()
        self.destroy()


class ReminderDialog(ctk.CTkToplevel):
    """Dialog for adding/editing reminders."""
    
    def __init__(self, parent, title: str, reminder: dict = None):
        """Initialize reminder dialog."""
        super().__init__(parent)
        self.title(title)
        self.geometry("500x600")
        self.resizable(False, False)
        
        self.result = None
        self.reminder = reminder
        
        # Make dialog modal
        self.transient(parent)
        self.grab_set()
        
        self.create_dialog_ui()
        self.wait_window()
    
    def create_dialog_ui(self):
        """Create dialog UI."""
        frame = ctk.CTkFrame(self)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        frame.grid_columnconfigure(0, weight=1)
        
        # Title
        title_label = ctk.CTkLabel(frame, text="Title:", font=("Arial", 12, "bold"))
        title_label.grid(row=0, column=0, sticky="w", pady=(0, 5))
        
        self.title_entry = ctk.CTkEntry(frame, placeholder_text="Enter reminder title")
        self.title_entry.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        
        # Description
        desc_label = ctk.CTkLabel(frame, text="Description:", font=("Arial", 12, "bold"))
        desc_label.grid(row=2, column=0, sticky="w", pady=(0, 5))
        
        self.desc_entry = ctk.CTkTextbox(frame, height=100)
        self.desc_entry.grid(row=3, column=0, sticky="ew", pady=(0, 10))
        
        # Date
        date_label = ctk.CTkLabel(frame, text="Date:", font=("Arial", 12, "bold"))
        date_label.grid(row=4, column=0, sticky="w", pady=(0, 5))
        
        self.date_entry = ctk.CTkEntry(frame, placeholder_text="YYYY-MM-DD")
        self.date_entry.grid(row=5, column=0, sticky="ew", pady=(0, 10))
        
        # Time
        time_label = ctk.CTkLabel(frame, text="Time:", font=("Arial", 12, "bold"))
        time_label.grid(row=6, column=0, sticky="w", pady=(0, 5))
        
        self.time_entry = ctk.CTkEntry(frame, placeholder_text="HH:MM")
        self.time_entry.grid(row=7, column=0, sticky="ew", pady=(0, 10))
        
        # Category
        cat_label = ctk.CTkLabel(frame, text="Category:", font=("Arial", 12, "bold"))
        cat_label.grid(row=8, column=0, sticky="w", pady=(0, 5))
        
        categories = CategoryColors.get_default_categories()
        self.category_var = ctk.StringVar(value="General")
        category_menu = ctk.CTkOptionMenu(
            frame,
            variable=self.category_var,
            values=categories
        )
        category_menu.grid(row=9, column=0, sticky="ew", pady=(0, 10))
        
        # Priority
        priority_label = ctk.CTkLabel(frame, text="Priority:", font=("Arial", 12, "bold"))
        priority_label.grid(row=10, column=0, sticky="w", pady=(0, 5))
        
        priorities = PriorityColors.get_priority_list()
        self.priority_var = ctk.StringVar(value="Normal")
        priority_menu = ctk.CTkOptionMenu(
            frame,
            variable=self.priority_var,
            values=priorities
        )
        priority_menu.grid(row=11, column=0, sticky="ew", pady=(0, 20))
        
        # Buttons
        button_frame = ctk.CTkFrame(frame)
        button_frame.grid(row=12, column=0, sticky="ew", columnspan=2)
        button_frame.grid_columnconfigure((0, 1), weight=1)
        
        save_btn = ctk.CTkButton(
            button_frame,
            text="Save",
            command=self.save_reminder,
            fg_color="#4CAF50"
        )
        save_btn.grid(row=0, column=0, padx=5, sticky="ew")
        
        cancel_btn = ctk.CTkButton(
            button_frame,
            text="Cancel",
            command=self.cancel,
            fg_color="#FF6B6B"
        )
        cancel_btn.grid(row=0, column=1, padx=5, sticky="ew")
        
        # Load existing reminder data if editing
        if self.reminder:
            self.title_entry.insert(0, self.reminder['title'])
            self.desc_entry.insert("1.0", self.reminder['description'])
            self.date_entry.insert(0, self.reminder['date'])
            self.time_entry.insert(0, self.reminder['time'])
            self.category_var.set(self.reminder['category'])
            self.priority_var.set(self.reminder['priority'])
        else:
            self.date_entry.insert(0, DateUtils.get_current_date())
            self.time_entry.insert(0, DateUtils.get_current_time())
    
    def save_reminder(self):
        """Save reminder and close dialog."""
        title = self.title_entry.get().strip()
        description = self.desc_entry.get("1.0", "end-1c").strip()
        date = self.date_entry.get().strip()
        time = self.time_entry.get().strip()
        category = self.category_var.get()
        priority = self.priority_var.get()
        
        # Validation
        if not title:
            messagebox.showwarning("Warning", "Please enter a title")
            return
        
        if not date or not time:
            messagebox.showwarning("Warning", "Please enter date and time")
            return
        
        try:
            datetime.strptime(date, "%Y-%m-%d")
            datetime.strptime(time, "%H:%M")
        except ValueError:
            messagebox.showerror("Error", "Invalid date/time format")
            return
        
        self.result = (title, description, date, time, category, priority)
        self.destroy()
    
    def cancel(self):
        """Cancel and close dialog."""
        self.result = None
        self.destroy()


def main():
    """Run the application."""
    app = CalendarAndReminderApp()
    app.mainloop()


if __name__ == "__main__":
    main()
