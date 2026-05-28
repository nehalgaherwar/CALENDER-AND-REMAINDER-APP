"""
Database module for handling SQLite operations.
Manages reminders, their storage, retrieval, and updates.
"""

import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Optional, Tuple


class ReminderDatabase:
    """SQLite database handler for reminders."""
    
    def __init__(self, db_path: str = "reminders.db"):
        """Initialize database connection and create tables if needed."""
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self.init_database()
    
    def init_database(self):
        """Initialize database connection and create tables."""
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self._create_tables()
    
    def _create_tables(self):
        """Create necessary tables if they don't exist."""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS reminders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                date TEXT NOT NULL,
                time TEXT NOT NULL,
                category TEXT DEFAULT 'General',
                priority TEXT DEFAULT 'Normal',
                is_completed INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()
    
    def add_reminder(self, title: str, description: str, date: str, 
                     time: str, category: str = "General", 
                     priority: str = "Normal") -> int:
        """
        Add a new reminder to the database.
        
        Args:
            title: Reminder title
            description: Reminder description
            date: Reminder date (YYYY-MM-DD format)
            time: Reminder time (HH:MM format)
            category: Reminder category
            priority: Reminder priority (Low, Normal, High)
        
        Returns:
            ID of the inserted reminder
        """
        try:
            self.cursor.execute('''
                INSERT INTO reminders 
                (title, description, date, time, category, priority)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (title, description, date, time, category, priority))
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return -1
    
    def get_all_reminders(self) -> List[Dict]:
        """Get all reminders from the database."""
        try:
            self.cursor.execute('SELECT * FROM reminders ORDER BY date, time')
            rows = self.cursor.fetchall()
            return self._convert_to_dict(rows)
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []
    
    def get_reminders_by_date(self, date: str) -> List[Dict]:
        """Get reminders for a specific date."""
        try:
            self.cursor.execute(
                'SELECT * FROM reminders WHERE date = ? ORDER BY time',
                (date,)
            )
            rows = self.cursor.fetchall()
            return self._convert_to_dict(rows)
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []
    
    def get_reminders_by_category(self, category: str) -> List[Dict]:
        """Get reminders by category."""
        try:
            self.cursor.execute(
                'SELECT * FROM reminders WHERE category = ? ORDER BY date, time',
                (category,)
            )
            rows = self.cursor.fetchall()
            return self._convert_to_dict(rows)
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []
    
    def search_reminders(self, query: str) -> List[Dict]:
        """Search reminders by title or description."""
        try:
            search_term = f"%{query}%"
            self.cursor.execute('''
                SELECT * FROM reminders 
                WHERE title LIKE ? OR description LIKE ?
                ORDER BY date, time
            ''', (search_term, search_term))
            rows = self.cursor.fetchall()
            return self._convert_to_dict(rows)
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []
    
    def update_reminder(self, reminder_id: int, **kwargs) -> bool:
        """
        Update a reminder.
        
        Args:
            reminder_id: ID of the reminder to update
            **kwargs: Fields to update (title, description, date, time, etc.)
        
        Returns:
            True if successful, False otherwise
        """
        try:
            allowed_fields = {'title', 'description', 'date', 'time', 
                            'category', 'priority', 'is_completed'}
            fields_to_update = {k: v for k, v in kwargs.items() 
                               if k in allowed_fields}
            
            if not fields_to_update:
                return False
            
            set_clause = ', '.join([f"{k} = ?" for k in fields_to_update.keys()])
            set_clause += ', updated_at = CURRENT_TIMESTAMP'
            
            values = list(fields_to_update.values()) + [reminder_id]
            
            self.cursor.execute(
                f'UPDATE reminders SET {set_clause} WHERE id = ?',
                values
            )
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False
    
    def delete_reminder(self, reminder_id: int) -> bool:
        """Delete a reminder by ID."""
        try:
            self.cursor.execute('DELETE FROM reminders WHERE id = ?', (reminder_id,))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False
    
    def get_reminder_by_id(self, reminder_id: int) -> Optional[Dict]:
        """Get a specific reminder by ID."""
        try:
            self.cursor.execute('SELECT * FROM reminders WHERE id = ?', (reminder_id,))
            row = self.cursor.fetchone()
            if row:
                return self._row_to_dict(row)
            return None
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None
    
    def get_upcoming_reminders(self, days: int = 7) -> List[Dict]:
        """Get reminders for the next N days."""
        try:
            self.cursor.execute('''
                SELECT * FROM reminders 
                WHERE date >= date('now') AND date <= date('now', ? || ' days')
                ORDER BY date, time
            ''', (days,))
            rows = self.cursor.fetchall()
            return self._convert_to_dict(rows)
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []
    
    def get_categories(self) -> List[str]:
        """Get all unique categories."""
        try:
            self.cursor.execute('SELECT DISTINCT category FROM reminders')
            categories = [row[0] for row in self.cursor.fetchall()]
            return sorted(categories)
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []
    
    def _row_to_dict(self, row: Tuple) -> Dict:
        """Convert a database row to a dictionary."""
        return {
            'id': row[0],
            'title': row[1],
            'description': row[2],
            'date': row[3],
            'time': row[4],
            'category': row[5],
            'priority': row[6],
            'is_completed': row[7],
            'created_at': row[8],
            'updated_at': row[9]
        }
    
    def _convert_to_dict(self, rows: List[Tuple]) -> List[Dict]:
        """Convert multiple rows to dictionaries."""
        return [self._row_to_dict(row) for row in rows]
    
    def close(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()
    
    def __del__(self):
        """Destructor to ensure database is closed."""
        self.close()
