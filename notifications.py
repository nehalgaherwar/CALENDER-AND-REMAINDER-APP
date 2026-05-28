"""
Notifications module for handling reminder alerts.
"""

import threading
import time
from datetime import datetime
from typing import Callable, Optional
import tkinter as tk
from tkinter import messagebox


class NotificationManager:
    """Manages reminder notifications."""
    
    def __init__(self):
        """Initialize the notification manager."""
        self.active = False
        self.thread = None
        self.reminders_to_check = []
        self.notification_callbacks = []
    
    def start(self, check_interval: int = 60):
        """
        Start monitoring reminders for notifications.
        
        Args:
            check_interval: Interval in seconds to check for due reminders
        """
        if not self.active:
            self.active = True
            self.thread = threading.Thread(
                target=self._check_reminders_loop,
                args=(check_interval,),
                daemon=True
            )
            self.thread.start()
    
    def stop(self):
        """Stop monitoring reminders."""
        self.active = False
    
    def set_reminders(self, reminders: list):
        """Set the list of reminders to monitor."""
        self.reminders_to_check = reminders
    
    def add_notification_callback(self, callback: Callable):
        """
        Add a callback function for notifications.
        
        Args:
            callback: Function to call when a reminder is due
                     Should accept reminder dict as parameter
        """
        self.notification_callbacks.append(callback)
    
    def _check_reminders_loop(self, check_interval: int):
        """Background loop to check for due reminders."""
        while self.active:
            try:
                self._check_due_reminders()
                time.sleep(check_interval)
            except Exception as e:
                print(f"Error in reminder check loop: {e}")
    
    def _check_due_reminders(self):
        """Check if any reminders are due and trigger notifications."""
        now = datetime.now()
        current_date = now.strftime("%Y-%m-%d")
        current_time = now.strftime("%H:%M")
        
        for reminder in self.reminders_to_check:
            if not reminder['is_completed']:
                reminder_date = reminder['date']
                reminder_time = reminder['time']
                
                # Check if reminder is due (within same minute)
                if (reminder_date == current_date and 
                    reminder_time <= current_time):
                    
                    # Trigger all registered callbacks
                    for callback in self.notification_callbacks:
                        try:
                            callback(reminder)
                        except Exception as e:
                            print(f"Error in notification callback: {e}")
    
    def show_notification_popup(self, reminder: dict):
        """
        Show a popup notification for a reminder.
        
        Args:
            reminder: Reminder dictionary
        """
        try:
            root = tk.Tk()
            root.withdraw()  # Hide main window
            
            title = reminder.get('title', 'Reminder')
            description = reminder.get('description', '')
            time_str = reminder.get('time', '')
            
            message = f"Time: {time_str}\n\n{description}" if description else f"Time: {time_str}"
            
            messagebox.showinfo(
                f"Reminder: {title}",
                message
            )
            root.destroy()
        except Exception as e:
            print(f"Error showing notification: {e}")
    
    def play_notification_sound(self):
        """Play a notification sound (optional)."""
        try:
            # Using system beep
            import winsound
            winsound.Beep(1000, 500)  # 1000 Hz for 500ms
        except Exception as e:
            print(f"Could not play sound: {e}")


class ReminderAlert:
    """Creates and displays reminder alerts."""
    
    @staticmethod
    def show_alert(parent, reminder: dict):
        """
        Show an alert for a reminder.
        
        Args:
            parent: Parent Tkinter widget
            reminder: Reminder dictionary
        """
        title = reminder.get('title', 'Reminder')
        description = reminder.get('description', '')
        time_str = reminder.get('time', '')
        priority = reminder.get('priority', 'Normal')
        
        alert_window = tk.Toplevel(parent)
        alert_window.title(f"Reminder Alert - {priority}")
        alert_window.geometry("400x250")
        alert_window.resizable(False, False)
        
        # Make alert stay on top
        alert_window.attributes('-topmost', True)
        
        # Title
        title_label = tk.Label(
            alert_window,
            text=title,
            font=("Arial", 16, "bold"),
            fg="#FF6B6B" if priority == "High" else "#FFA500" if priority == "Normal" else "#4CAF50"
        )
        title_label.pack(pady=10)
        
        # Time
        time_label = tk.Label(
            alert_window,
            text=f"Time: {time_str}",
            font=("Arial", 12)
        )
        time_label.pack(pady=5)
        
        # Description
        if description:
            desc_label = tk.Label(
                alert_window,
                text=description,
                font=("Arial", 11),
                wraplength=350,
                justify=tk.LEFT
            )
            desc_label.pack(pady=10, padx=10)
        
        # Buttons frame
        button_frame = tk.Frame(alert_window)
        button_frame.pack(pady=20)
        
        def mark_done():
            alert_window.destroy()
            return True
        
        ok_button = tk.Button(
            button_frame,
            text="Mark as Done",
            command=mark_done,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10),
            padx=10
        )
        ok_button.pack(side=tk.LEFT, padx=5)
        
        snooze_button = tk.Button(
            button_frame,
            text="Snooze (5 min)",
            bg="#2196F3",
            fg="white",
            font=("Arial", 10),
            padx=10
        )
        snooze_button.pack(side=tk.LEFT, padx=5)
        
        alert_window.after(0, alert_window.lift)
