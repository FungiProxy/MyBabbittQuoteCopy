#!/usr/bin/env python3
"""
User Management Script for MyBabbittQuote
Administrative tool for managing user accounts.
"""

import sys
import os
import getpass

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.core.auth.user_manager import UserManager


def print_banner():
    """Print application banner."""
    print("=" * 60)
    print("           MyBabbittQuote User Management")
    print("=" * 60)
    print()


def print_menu():
    """Print the main menu."""
    print("Available actions:")
    print("1. List all users")
    print("2. Create new user")
    print("3. Change user password")
    print("4. Deactivate user")
    print("5. Activate user")
    print("6. Delete user")
    print("7. Exit")
    print()


def list_users(user_manager):
    """List all users."""
    print("\n📋 User List:")
    print("-" * 80)
    print(f"{'ID':<4} {'Username':<15} {'Full Name':<25} {'Email':<25} {'Role':<10} {'Status':<8}")
    print("-" * 80)
    
    try:
        with user_manager.user_manager.db_path.replace("users.db", "temp_users.db") as conn:
            cursor = conn.execute("""
                SELECT id, username, full_name, email, role, is_active 
                FROM users ORDER BY id
            """)
            
            for row in cursor.fetchall():
                user_id, username, full_name, email, role, is_active = row
                status = "Active" if is_active else "Inactive"
                print(f"{user_id:<4} {username:<15} {full_name:<25} {email:<25} {role:<10} {status:<8}")
    
    except Exception as e:
        print(f"❌ Error listing users: {e}")
    
    print()


def create_user(user_manager):
    """Create a new user."""
    print("\n👤 Create New User:")
    print("-" * 40)
    
    username = input("Username: ").strip()
    if not username:
        print("❌ Username is required")
        return
    
    email = input("Email: ").strip()
    if not email:
        print("❌ Email is required")
        return
    
    full_name = input("Full Name: ").strip()
    if not full_name:
        print("❌ Full name is required")
        return
    
    print("\nAvailable roles:")
    print("1. user - Basic user access")
    print("2. manager - Manager access with reports")
    print("3. admin - Full administrative access")
    
    role_choice = input("Role (1-3): ").strip()
    role_map = {"1": "user", "2": "manager", "3": "admin"}
    role = role_map.get(role_choice, "user")
    
    password = getpass.getpass("Password: ")
    if len(password) < 6:
        print("❌ Password must be at least 6 characters long")
        return
    
    confirm_password = getpass.getpass("Confirm Password: ")
    if password != confirm_password:
        print("❌ Passwords do not match")
        return
    
    success = user_manager.create_user(username, email, full_name, password, role)
    
    if success:
        print(f"✅ User '{username}' created successfully!")
    else:
        print("❌ Failed to create user. Username or email may already exist.")


def change_password(user_manager):
    """Change user password."""
    print("\n🔐 Change User Password:")
    print("-" * 40)
    
    username = input("Username: ").strip()
    if not username:
        print("❌ Username is required")
        return
    
    # Verify user exists
    try:
        with user_manager.user_manager.db_path.replace("users.db", "temp_users.db") as conn:
            cursor = conn.execute("SELECT id FROM users WHERE username = ?", (username,))
            if not cursor.fetchone():
                print("❌ User not found")
                return
    except Exception as e:
        print(f"❌ Error: {e}")
        return
    
    new_password = getpass.getpass("New Password: ")
    if len(new_password) < 6:
        print("❌ Password must be at least 6 characters long")
        return
    
    confirm_password = getpass.getpass("Confirm New Password: ")
    if new_password != confirm_password:
        print("❌ Passwords do not match")
        return
    
    # For admin password change, we'll need to implement this in UserManager
    print("⚠️  Password change functionality requires user to be logged in")
    print("   This feature will be implemented in the UI")


def deactivate_user(user_manager):
    """Deactivate a user."""
    print("\n🚫 Deactivate User:")
    print("-" * 40)
    
    username = input("Username: ").strip()
    if not username:
        print("❌ Username is required")
        return
    
    confirm = input(f"Are you sure you want to deactivate user '{username}'? (y/N): ").strip().lower()
    if confirm != 'y':
        print("❌ Operation cancelled")
        return
    
    try:
        with user_manager.user_manager.db_path.replace("users.db", "temp_users.db") as conn:
            conn.execute("UPDATE users SET is_active = 0 WHERE username = ?", (username,))
            conn.commit()
            print(f"✅ User '{username}' deactivated successfully")
    except Exception as e:
        print(f"❌ Error: {e}")


def activate_user(user_manager):
    """Activate a user."""
    print("\n✅ Activate User:")
    print("-" * 40)
    
    username = input("Username: ").strip()
    if not username:
        print("❌ Username is required")
        return
    
    try:
        with user_manager.user_manager.db_path.replace("users.db", "temp_users.db") as conn:
            conn.execute("UPDATE users SET is_active = 1 WHERE username = ?", (username,))
            conn.commit()
            print(f"✅ User '{username}' activated successfully")
    except Exception as e:
        print(f"❌ Error: {e}")


def delete_user(user_manager):
    """Delete a user."""
    print("\n🗑️  Delete User:")
    print("-" * 40)
    
    username = input("Username: ").strip()
    if not username:
        print("❌ Username is required")
        return
    
    confirm = input(f"Are you sure you want to DELETE user '{username}'? This cannot be undone! (y/N): ").strip().lower()
    if confirm != 'y':
        print("❌ Operation cancelled")
        return
    
    try:
        with user_manager.user_manager.db_path.replace("users.db", "temp_users.db") as conn:
            conn.execute("DELETE FROM users WHERE username = ?", (username,))
            conn.commit()
            print(f"✅ User '{username}' deleted successfully")
    except Exception as e:
        print(f"❌ Error: {e}")


def main():
    """Main function."""
    print_banner()
    
    # Initialize user manager
    try:
        user_manager = UserManager()
        print("✅ Connected to user database")
    except Exception as e:
        print(f"❌ Failed to connect to user database: {e}")
        return
    
    while True:
        print_menu()
        
        try:
            choice = input("Enter your choice (1-7): ").strip()
            
            if choice == '1':
                list_users(user_manager)
            elif choice == '2':
                create_user(user_manager)
            elif choice == '3':
                change_password(user_manager)
            elif choice == '4':
                deactivate_user(user_manager)
            elif choice == '5':
                activate_user(user_manager)
            elif choice == '6':
                delete_user(user_manager)
            elif choice == '7':
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please enter a number between 1 and 7.")
        
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


if __name__ == "__main__":
    main() 