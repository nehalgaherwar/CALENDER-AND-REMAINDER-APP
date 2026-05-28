"""
Utility functions for the Calendar and Reminder App.
"""

from datetime import datetime, timedelta
import calendar as cal


class DateUtils:
    """Utilities for date handling."""
    
    @staticmethod
    def get_current_date() -> str:
        """Get current date in YYYY-MM-DD format."""
        return datetime.now().strftime("%Y-%m-%d")
    
    @staticmethod
    def get_current_time() -> str:
        """Get current time in HH:MM format."""
        return datetime.now().strftime("%H:%M")
    
    @staticmethod
    def format_date(date_str: str) -> str:
        """
        Format date string to human-readable format.
        
        Args:
            date_str: Date in YYYY-MM-DD format
        
        Returns:
            Formatted date string (e.g., "January 15, 2024")
        """
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            return date_obj.strftime("%B %d, %Y")
        except (ValueError, TypeError):
            return date_str
    
    @staticmethod
    def format_datetime(date_str: str, time_str: str) -> str:
        """
        Format date and time for display.
        
        Args:
            date_str: Date in YYYY-MM-DD format
            time_str: Time in HH:MM format
        
        Returns:
            Formatted datetime string
        """
        date_formatted = DateUtils.format_date(date_str)
        return f"{date_formatted} at {time_str}"
    
    @staticmethod
    def is_past_due(date_str: str, time_str: str) -> bool:
        """
        Check if a reminder is past due.
        
        Args:
            date_str: Date in YYYY-MM-DD format
            time_str: Time in HH:MM format
        
        Returns:
            True if past due, False otherwise
        """
        try:
            reminder_datetime = datetime.strptime(
                f"{date_str} {time_str}", 
                "%Y-%m-%d %H:%M"
            )
            return reminder_datetime < datetime.now()
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def get_day_name(date_str: str) -> str:
        """
        Get day name from date string.
        
        Args:
            date_str: Date in YYYY-MM-DD format
        
        Returns:
            Day name (e.g., "Monday")
        """
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            return date_obj.strftime("%A")
        except (ValueError, TypeError):
            return ""
    
    @staticmethod
    def get_month_calendar(year: int, month: int) -> list:
        """
        Get calendar data for a specific month.
        
        Args:
            year: Year
            month: Month (1-12)
        
        Returns:
            List of weeks, each containing day numbers
        """
        return cal.monthcalendar(year, month)
    
    @staticmethod
    def get_month_name(month: int) -> str:
        """Get month name from month number."""
        months = [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ]
        return months[month - 1] if 1 <= month <= 12 else ""
    
    @staticmethod
    def add_days(date_str: str, days: int) -> str:
        """
        Add days to a date.
        
        Args:
            date_str: Date in YYYY-MM-DD format
            days: Number of days to add
        
        Returns:
            New date in YYYY-MM-DD format
        """
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            new_date = date_obj + timedelta(days=days)
            return new_date.strftime("%Y-%m-%d")
        except (ValueError, TypeError):
            return date_str


class PriorityColors:
    """Color mappings for priority levels."""
    
    COLORS = {
        "High": "#FF6B6B",      # Red
        "Normal": "#FFA500",    # Orange
        "Low": "#4CAF50"        # Green
    }
    
    @staticmethod
    def get_color(priority: str) -> str:
        """Get color for priority level."""
        return PriorityColors.COLORS.get(priority, "#FFA500")
    
    @staticmethod
    def get_priority_list() -> list:
        """Get list of priority options."""
        return list(PriorityColors.COLORS.keys())


class CategoryColors:
    """Color mappings for categories."""
    
    COLORS = {
        "Work": "#2196F3",
        "Personal": "#9C27B0",
        "Health": "#4CAF50",
        "Shopping": "#FF9800",
        "Finance": "#3F51B5",
        "Education": "#00BCD4",
        "Entertainment": "#E91E63",
        "General": "#757575"
    }
    
    @staticmethod
    def get_color(category: str) -> str:
        """Get color for category."""
        return CategoryColors.COLORS.get(category, "#757575")
    
    @staticmethod
    def get_default_categories() -> list:
        """Get default category list."""
        return list(CategoryColors.COLORS.keys())
    
    @staticmethod
    def add_category_color(category: str, color: str):
        """Add custom category color."""
        CategoryColors.COLORS[category] = color
