"""
Database manager for DoroLexus flashcard application
Handles SQLite database operations for decks, cards, and study sessions
"""

import sqlite3
import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple

class DatabaseManager:
    """Manages SQLite database operations for the flashcard app"""
    
    def __init__(self, db_path: str = None):
        """Initialize database connection and create tables if needed"""
        # Default DB path inside data/database directory
        if db_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            data_dir = os.path.join(base_dir, 'data', 'database')
            os.makedirs(data_dir, exist_ok=True)
            db_path = os.path.join(data_dir, 'dorolexus.db')

        self.db_path = db_path
        self.connection = sqlite3.connect(db_path)
        self.connection.row_factory = sqlite3.Row
        self.create_tables()
        
    def create_tables(self):
        """Create database tables if they don't exist"""
        cursor = self.connection.cursor()
        
        # Decks table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS decks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Cards table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cards (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                deck_id INTEGER NOT NULL,
                front TEXT NOT NULL,
                back TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (deck_id) REFERENCES decks (id) ON DELETE CASCADE
            )
        """)
        
        # Study sessions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS study_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                card_id INTEGER NOT NULL,
                deck_id INTEGER NOT NULL,
                review_date TIMESTAMP NOT NULL,
                ease_factor REAL DEFAULT 2.5,
                interval_days INTEGER DEFAULT 1,
                repetitions INTEGER DEFAULT 0,
                quality INTEGER, -- 0-5 rating
                FOREIGN KEY (card_id) REFERENCES cards (id) ON DELETE CASCADE,
                FOREIGN KEY (deck_id) REFERENCES decks (id) ON DELETE CASCADE
            )
        """)
        
        # Statistics table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS statistics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                deck_id INTEGER,
                date TEXT NOT NULL,
                cards_studied INTEGER DEFAULT 0,
                correct_answers INTEGER DEFAULT 0,
                study_time_seconds INTEGER DEFAULT 0,
                FOREIGN KEY (deck_id) REFERENCES decks (id) ON DELETE CASCADE
            )
        """)
        
        self.connection.commit()
        
    def create_deck(self, name: str, description: str = "") -> int:
        """Create a new deck and return its ID"""
        cursor = self.connection.cursor()
        try:
            cursor.execute("""
                INSERT INTO decks (name, description)
                VALUES (?, ?)
            """, (name, description))
            self.connection.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            raise ValueError(f"Deck with name '{name}' already exists")
            
    def get_all_decks(self) -> List[Dict]:
        """Get all decks with card counts"""
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT d.*, COUNT(c.id) as card_count
            FROM decks d
            LEFT JOIN cards c ON d.id = c.deck_id
            GROUP BY d.id
            ORDER BY d.created_at DESC
        """)
        return [dict(row) for row in cursor.fetchall()]
        
    def get_deck(self, deck_id: int) -> Optional[Dict]:
        """Get a specific deck by ID"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM decks WHERE id = ?", (deck_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
        
    def update_deck(self, deck_id: int, name: str, description: str = ""):
        """Update deck information"""
        cursor = self.connection.cursor()
        cursor.execute("""
            UPDATE decks 
            SET name = ?, description = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (name, description, deck_id))
        self.connection.commit()
        
    def delete_deck(self, deck_id: int):
        """Delete a deck and all its cards"""
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM decks WHERE id = ?", (deck_id,))
        self.connection.commit()
        
    def create_card(self, deck_id: int, front: str, back: str) -> int:
        """Create a new card in a deck"""
        cursor = self.connection.cursor()
        cursor.execute("""
            INSERT INTO cards (deck_id, front, back)
            VALUES (?, ?, ?)
        """, (deck_id, front, back))
        self.connection.commit()
        return cursor.lastrowid
        
    def get_cards_in_deck(self, deck_id: int) -> List[Dict]:
        """Get all cards in a specific deck"""
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT * FROM cards 
            WHERE deck_id = ? 
            ORDER BY created_at DESC
        """, (deck_id,))
        return [dict(row) for row in cursor.fetchall()]
        
    def update_card(self, card_id: int, front: str, back: str):
        """Update card content"""
        cursor = self.connection.cursor()
        cursor.execute("""
            UPDATE cards 
            SET front = ?, back = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (front, back, card_id))
        self.connection.commit()
        
    def delete_card(self, card_id: int):
        """Delete a card"""
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM cards WHERE id = ?", (card_id,))
        self.connection.commit()
        
    def get_cards_due_for_review(self, deck_id: int = None) -> List[Dict]:
        """Get cards that are due for review using spaced repetition"""
        cursor = self.connection.cursor()
        
        if deck_id:
            # Get cards for specific deck
            cursor.execute("""
                SELECT c.*, 
                       COALESCE(ss.ease_factor, 2.5) as ease_factor,
                       COALESCE(ss.interval_days, 1) as interval_days,
                       COALESCE(ss.repetitions, 0) as repetitions,
                       COALESCE(ss.review_date, '1900-01-01') as last_review
                FROM cards c
                LEFT JOIN study_sessions ss ON c.id = ss.card_id
                WHERE c.deck_id = ?
                AND (ss.review_date IS NULL 
                     OR datetime(ss.review_date, '+' || COALESCE(ss.interval_days, 1) || ' days') <= datetime('now'))
                ORDER BY COALESCE(ss.review_date, '1900-01-01')
            """, (deck_id,))
        else:
            # Get cards for all decks
            cursor.execute("""
                SELECT c.*, 
                       COALESCE(ss.ease_factor, 2.5) as ease_factor,
                       COALESCE(ss.interval_days, 1) as interval_days,
                       COALESCE(ss.repetitions, 0) as repetitions,
                       COALESCE(ss.review_date, '1900-01-01') as last_review
                FROM cards c
                LEFT JOIN study_sessions ss ON c.id = ss.card_id
                WHERE (ss.review_date IS NULL 
                       OR datetime(ss.review_date, '+' || COALESCE(ss.interval_days, 1) || ' days') <= datetime('now'))
                ORDER BY COALESCE(ss.review_date, '1900-01-01')
            """)
            
        return [dict(row) for row in cursor.fetchall()]
        
    def record_study_session(self, card_id: int, deck_id: int, quality: int):
        """Record a study session with spaced repetition algorithm"""
        cursor = self.connection.cursor()
        
        # Get current session data
        cursor.execute("""
            SELECT * FROM study_sessions 
            WHERE card_id = ? 
            ORDER BY review_date DESC 
            LIMIT 1
        """, (card_id,))
        
        current_session = cursor.fetchone()
        
        if current_session:
            # Update existing session
            ease_factor = current_session['ease_factor']
            interval_days = current_session['interval_days']
            repetitions = current_session['repetitions']
        else:
            # Create new session
            ease_factor = 2.5
            interval_days = 1
            repetitions = 0
            
        # Apply spaced repetition algorithm (simplified SM-2)
        if quality >= 3:  # Correct answer
            if repetitions == 0:
                interval_days = 1
            elif repetitions == 1:
                interval_days = 6
            else:
                interval_days = int(interval_days * ease_factor)
            repetitions += 1
        else:  # Incorrect answer
            repetitions = 0
            interval_days = 1
            
        # Update ease factor
        ease_factor = max(1.3, ease_factor + 0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
        
        # Insert or update session
        cursor.execute("""
            INSERT OR REPLACE INTO study_sessions 
            (card_id, deck_id, review_date, ease_factor, interval_days, repetitions, quality)
            VALUES (?, ?, datetime('now'), ?, ?, ?, ?)
        """, (card_id, deck_id, ease_factor, interval_days, repetitions, quality))
        
        self.connection.commit()
        
    def get_study_statistics(self, deck_id: int = None, days: int = 30) -> Dict:
        """Get study statistics for the specified period"""
        cursor = self.connection.cursor()
        
        date_filter = f"AND date >= date('now', '-{days} days')"
        deck_filter = f"AND deck_id = {deck_id}" if deck_id else ""
        
        cursor.execute(f"""
            SELECT 
                COUNT(*) as total_sessions,
                SUM(cards_studied) as total_cards_studied,
                SUM(correct_answers) as total_correct,
                SUM(study_time_seconds) as total_study_time,
                AVG(CAST(correct_answers AS FLOAT) / cards_studied) as accuracy_rate
            FROM statistics 
            WHERE 1=1 {date_filter} {deck_filter}
        """)
        
        stats = cursor.fetchone()
        
        # Get daily statistics
        cursor.execute(f"""
            SELECT date, cards_studied, correct_answers, study_time_seconds
            FROM statistics 
            WHERE 1=1 {date_filter} {deck_filter}
            ORDER BY date DESC
        """)
        
        daily_stats = [dict(row) for row in cursor.fetchall()]
        
        return {
            'total_sessions': stats['total_sessions'] or 0,
            'total_cards_studied': stats['total_cards_studied'] or 0,
            'total_correct': stats['total_correct'] or 0,
            'total_study_time': stats['total_study_time'] or 0,
            'accuracy_rate': stats['accuracy_rate'] or 0.0,
            'daily_stats': daily_stats
        }
        
    def record_daily_stats(self, deck_id: int, cards_studied: int, correct_answers: int, study_time_seconds: int):
        """Record daily study statistics"""
        cursor = self.connection.cursor()
        today = datetime.now().strftime('%Y-%m-%d')
        
        cursor.execute("""
            INSERT OR REPLACE INTO statistics 
            (deck_id, date, cards_studied, correct_answers, study_time_seconds)
            VALUES (?, ?, ?, ?, ?)
        """, (deck_id, today, cards_studied, correct_answers, study_time_seconds))
        
        self.connection.commit()
        
    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
