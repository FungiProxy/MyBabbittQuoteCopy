"""
User management system for authentication.
"""

import hashlib
import secrets
import sqlite3
import os
from typing import Optional, Dict, Any
from dataclasses import dataclass
from datetime import datetime, timedelta
import time


@dataclass
class User:
    """User data model."""
    id: int
    username: str
    email: str
    full_name: str
    role: str
    is_active: bool
    created_at: datetime
    last_login: Optional[datetime] = None
    work_phone: Optional[str] = None


class UserManager:
    """Manages user accounts and authentication."""
    
    def __init__(self, db_path: str = "data/users.db"):
        """Initialize user manager with database path."""
        self.db_path = db_path
        self._ensure_db_exists()
    
    def _ensure_db_exists(self):
        """Create database and tables if they don't exist."""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    full_name TEXT NOT NULL,
                    password_hash TEXT NOT NULL,
                    salt TEXT NOT NULL,
                    role TEXT NOT NULL DEFAULT 'user',
                    is_active BOOLEAN NOT NULL DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_login TIMESTAMP,
                    work_phone TEXT
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS login_attempts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    ip_address TEXT,
                    success BOOLEAN NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
    
    def _hash_password(self, password: str, salt: str) -> str:
        """Hash password with salt using SHA-256."""
        return hashlib.sha256((password + salt).encode()).hexdigest()
    
    def _generate_salt(self) -> str:
        """Generate a random salt for password hashing."""
        return secrets.token_hex(16)
    
    def _validate_password(self, password: str) -> tuple[bool, str]:
        """
        Validate password requirements.
        
        Returns:
            tuple[bool, str]: (is_valid, error_message)
        """
        # No validation rules - accept any password
        return True, ""
    
    def create_user(self, username: str, email: str, full_name: str, 
                   password: str, role: str = "user", work_phone: Optional[str] = None) -> tuple[bool, str]:
        """Create a new user account."""
        # Validate password
        is_valid, error_msg = self._validate_password(password)
        if not is_valid:
            return False, error_msg
        try:
            salt = self._generate_salt()
            password_hash = self._hash_password(password, salt)
            if work_phone is None:
                work_phone = ""
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT INTO users (username, email, full_name, password_hash, salt, role, work_phone)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (username, email, full_name, password_hash, salt, role, work_phone))
                conn.commit()
            return True, "User created successfully"
        except sqlite3.IntegrityError:
            return False, "Username or email already exists"
        except Exception as e:
            return False, f"Error creating user: {e}"
    
    def authenticate_user(self, username: str, password: str, 
                         ip_address: Optional[str] = None) -> Optional[User]:
        """Authenticate a user with username and password."""
        try:
            with sqlite3.connect(self.db_path, timeout=10.0) as conn:
                cursor = conn.execute("""
                    SELECT id, username, email, full_name, password_hash, salt, 
                           role, is_active, created_at, last_login
                    FROM users WHERE username = ? AND is_active = 1
                """, (username,))
                
                row = cursor.fetchone()
                if not row:
                    self._log_login_attempt(username, ip_address, False)
                    return None
                
                user_id, db_username, email, full_name, stored_hash, salt, \
                role, is_active, created_at, last_login = row
                
                # Verify password
                provided_hash = self._hash_password(password, salt)
                if provided_hash != stored_hash:
                    self._log_login_attempt(username, ip_address, False)
                    return None
                
                # Update last login
                conn.execute("""
                    UPDATE users SET last_login = CURRENT_TIMESTAMP 
                    WHERE id = ?
                """, (user_id,))
                
                # Log successful login
                self._log_login_attempt(username, ip_address, True)
                
                return User(
                    id=user_id,
                    username=db_username,
                    email=email,
                    full_name=full_name,
                    role=role,
                    is_active=bool(is_active),
                    created_at=datetime.fromisoformat(created_at),
                    last_login=datetime.fromisoformat(last_login) if last_login else None
                )
                
        except Exception as e:
            print(f"Authentication error: {e}")
            return None
    
    def _log_login_attempt(self, username: str, ip_address: Optional[str], success: bool):
        """Log login attempts for security monitoring."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT INTO login_attempts (username, ip_address, success)
                    VALUES (?, ?, ?)
                """, (username, ip_address, success))
                conn.commit()
        except Exception as e:
            print(f"Failed to log login attempt: {e}")
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute("""
                    SELECT id, username, email, full_name, role, is_active, 
                           created_at, last_login, work_phone
                    FROM users WHERE id = ?
                """, (user_id,))
                
                row = cursor.fetchone()
                if not row:
                    return None
                
                user_id, username, email, full_name, role, is_active, \
                created_at, last_login, work_phone = row
                
                return User(
                    id=user_id,
                    username=username,
                    email=email,
                    full_name=full_name,
                    role=role,
                    is_active=bool(is_active),
                    created_at=datetime.fromisoformat(created_at),
                    last_login=datetime.fromisoformat(last_login) if last_login else None,
                    work_phone=work_phone
                )
        except Exception as e:
            print(f"Error getting user: {e}")
            return None
    
    def change_password(self, user_id: int, current_password: str, 
                       new_password: str) -> tuple[bool, str]:
        """Change user password."""
        # Validate new password
        is_valid, error_msg = self._validate_password(new_password)
        if not is_valid:
            return False, error_msg
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                # Get current password hash
                cursor = conn.execute("""
                    SELECT password_hash, salt FROM users WHERE id = ?
                """, (user_id,))
                row = cursor.fetchone()
                
                if not row:
                    return False, "User not found"
                
                stored_hash, salt = row
                
                # Verify current password
                current_hash = self._hash_password(current_password, salt)
                if current_hash != stored_hash:
                    return False, "Current password is incorrect"
                
                # Generate new salt and hash
                new_salt = self._generate_salt()
                new_hash = self._hash_password(new_password, new_salt)
                
                # Update password
                conn.execute("""
                    UPDATE users SET password_hash = ?, salt = ? WHERE id = ?
                """, (new_hash, new_salt, user_id))
                conn.commit()
                
                return True, "Password changed successfully"
        except Exception as e:
            return False, f"Error changing password: {e}"
    
    def create_default_admin(self):
        """Create a default admin user if no users exist."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute("SELECT COUNT(*) FROM users")
                count = cursor.fetchone()[0]
                
                if count == 0:
                    # Create default admin user
                    self.create_user(
                        username="admin",
                        email="admin@babbitt.com",
                        full_name="System Administrator",
                        password="admin123",
                        role="admin"
                    )
                    print("Default admin user created: admin/admin123")
                    print("⚠️  Please change the default password immediately!")
        except Exception as e:
            print(f"Error creating default admin: {e}")

    def list_users(self) -> list[User]:
        """Return a list of all users."""
        users = []
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute("""
                    SELECT id, username, email, full_name, role, is_active, created_at, last_login, work_phone
                    FROM users ORDER BY id
                """)
                for row in cursor.fetchall():
                    user_id, username, email, full_name, role, is_active, created_at, last_login, work_phone = row
                    users.append(User(
                        id=user_id,
                        username=username,
                        email=email,
                        full_name=full_name,
                        role=role,
                        is_active=bool(is_active),
                        created_at=datetime.fromisoformat(created_at),
                        last_login=datetime.fromisoformat(last_login) if last_login else None,
                        work_phone=work_phone
                    ))
        except Exception as e:
            print(f"Error listing users: {e}")
        return users

    def update_user(self, user_id: int, email: str, full_name: str, role: str, is_active: bool, work_phone: Optional[str] = None) -> bool:
        """Update user details (except password and username)."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    UPDATE users SET email = ?, full_name = ?, role = ?, is_active = ?, work_phone = ? WHERE id = ?
                """, (email, full_name, role, int(is_active), work_phone, user_id))
                conn.commit()
            return True
        except Exception as e:
            print(f"Error updating user: {e}")
            return False

    def activate_user(self, user_id: int) -> bool:
        """Activate a user account."""
        user = self.get_user_by_id(user_id)
        if user is None:
            return False
        return self.update_user(user_id, user.email, user.full_name, user.role, True, user.work_phone)

    def deactivate_user(self, user_id: int) -> bool:
        """Deactivate a user account."""
        user = self.get_user_by_id(user_id)
        if user is None:
            return False
        return self.update_user(user_id, user.email, user.full_name, user.role, False, user.work_phone)

    def delete_user(self, user_id: int) -> bool:
        """Delete a user account."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
                conn.commit()
            return True
        except Exception as e:
            print(f"Error deleting user: {e}")
            return False

    def set_password_admin(self, user_id: int, new_password: str) -> tuple[bool, str]:
        """Set user password as admin (bypasses current password requirement)."""
        # Validate new password
        is_valid, error_msg = self._validate_password(new_password)
        if not is_valid:
            return False, error_msg
        
        try:
            # Generate new salt and hash
            new_salt = self._generate_salt()
            new_hash = self._hash_password(new_password, new_salt)
            
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    UPDATE users SET password_hash = ?, salt = ? WHERE id = ?
                """, (new_hash, new_salt, user_id))
                conn.commit()
            
            return True, "Password set successfully"
        except Exception as e:
            return False, f"Error setting password: {e}" 