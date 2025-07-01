# MyBabbittQuote Authentication System

## Overview

The MyBabbittQuote application now includes a comprehensive authentication system that provides secure user login, role-based access control, and session management. This system ensures that only authorized users can access the application and its features.

## Features

### 🔐 Secure Authentication
- **Password Hashing**: All passwords are securely hashed using SHA-256 with unique salts
- **Session Management**: Persistent sessions with remember-me functionality
- **Login Attempt Logging**: All login attempts are logged for security monitoring
- **Account Status**: Users can be activated/deactivated by administrators

### 👥 User Management
- **Role-Based Access Control**: Three user roles (user, manager, admin)
- **User Creation**: Administrators can create new user accounts
- **Password Management**: Secure password change functionality
- **Account Administration**: Activate, deactivate, and delete user accounts

### 🛡️ Security Features
- **Input Validation**: All user inputs are validated and sanitized
- **SQL Injection Protection**: Parameterized queries prevent SQL injection
- **Session Security**: Secure session storage and management
- **Permission System**: Fine-grained permission control based on user roles

## User Roles and Permissions

### User (Basic Access)
- View quotes
- Create quotes
- Basic application features

### Manager (Enhanced Access)
- All user permissions
- Edit quotes
- View reports
- Customer management

### Admin (Full Access)
- All manager permissions
- User management
- System administration
- Database management

## Default Login

When the application is first run, a default administrator account is automatically created:

- **Username**: `admin`
- **Password**: `admin123`
- **Role**: Administrator

⚠️ **Important**: Change the default password immediately after first login!

## Installation and Setup

### 1. Automatic Setup
The authentication system is automatically initialized when the application starts. No manual setup is required.

### 2. Database Files
The system creates the following files in the `data/` directory:
- `users.db` - User accounts and authentication data
- `session.json` - Current user session information

### 3. First Run
1. Start the application: `python main.py`
2. Login with the default admin credentials
3. Change the default password immediately
4. Create additional user accounts as needed

## Usage

### Application Login
1. Launch the application
2. Enter your username and password
3. Optionally check "Remember me" for persistent login
4. Click "Login" to access the application

### User Management (Administrators)

#### Command Line Tool
Use the provided user management script:
```bash
python manage_users.py
```

Available actions:
- List all users
- Create new user
- Change user password
- Activate/deactivate users
- Delete users

#### GUI Management
User management is also available through the application interface for administrators.

### Logout
- Click the "🚪 Logout" button in the top-right corner
- The application will return to the login screen

## Security Best Practices

### For Administrators
1. **Change Default Password**: Immediately change the default admin password
2. **Strong Passwords**: Enforce strong password policies
3. **Regular Audits**: Review user accounts and permissions regularly
4. **Monitor Logs**: Check login attempt logs for suspicious activity
5. **Principle of Least Privilege**: Assign minimum necessary permissions

### For Users
1. **Strong Passwords**: Use strong, unique passwords
2. **Secure Sessions**: Don't share your login session
3. **Regular Password Changes**: Change passwords periodically
4. **Logout**: Always logout when finished using the application

## Technical Details

### Database Schema

#### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    full_name TEXT NOT NULL,
    password_hash TEXT NOT NULL,
    salt TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'user',
    is_active BOOLEAN NOT NULL DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);
```

#### Login Attempts Table
```sql
CREATE TABLE login_attempts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    ip_address TEXT,
    success BOOLEAN NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Password Security
- **Algorithm**: SHA-256
- **Salt**: 32-character random hex string
- **Storage**: `hash = SHA256(password + salt)`
- **Minimum Length**: 6 characters

### Session Management
- **Storage**: JSON file in `data/session.json`
- **Persistence**: Remember-me functionality
- **Security**: Session data includes user ID, role, and login time

## Troubleshooting

### Common Issues

#### "Invalid username or password"
- Verify username and password are correct
- Check if account is active
- Ensure caps lock is off

#### "Account is deactivated"
- Contact administrator to reactivate account
- Check if account was disabled for security reasons

#### "Database connection error"
- Ensure write permissions to `data/` directory
- Check if database files are corrupted
- Restart the application

#### "Permission denied"
- Verify user has required role/permissions
- Contact administrator for access

### Reset Admin Password
If the admin password is lost:

1. Stop the application
2. Delete `data/users.db` and `data/session.json`
3. Restart the application
4. Default admin account will be recreated

⚠️ **Warning**: This will delete all user accounts!

## API Reference

### AuthService
Main authentication service class.

```python
from src.core.auth import AuthService

auth_service = AuthService()

# Login
success, message = auth_service.login(username, password, remember_me)

# Check authentication
if auth_service.is_logged_in():
    user = auth_service.get_current_user()

# Check permissions
if auth_service.has_permission('create_quotes'):
    # User can create quotes
    pass

# Logout
auth_service.logout()
```

### UserManager
User account management.

```python
from src.core.auth.user_manager import UserManager

user_manager = UserManager()

# Create user
success = user_manager.create_user(username, email, full_name, password, role)

# Authenticate user
user = user_manager.authenticate_user(username, password)

# Change password
success = user_manager.change_password(user_id, current_password, new_password)
```

### SessionManager
Session management.

```python
from src.core.auth.session_manager import SessionManager

session_manager = SessionManager()

# Login user
session_manager.login(user, remember_me=True)

# Check session
if session_manager.is_logged_in():
    user = session_manager.get_current_user()

# Logout
session_manager.logout()
```

## Development

### Adding New Permissions
1. Update the permission mapping in `SessionManager.has_permission()`
2. Add permission checks to relevant functions
3. Update UI to show/hide features based on permissions

### Customizing User Roles
1. Modify role definitions in `SessionManager.has_permission()`
2. Update user creation forms
3. Adjust UI based on role requirements

### Extending Authentication
The authentication system is designed to be extensible. Key extension points:
- `UserManager` - Add custom user fields and validation
- `SessionManager` - Customize session behavior
- `AuthService` - Add custom authentication logic

## Support

For issues or questions about the authentication system:
1. Check this documentation
2. Review the troubleshooting section
3. Check application logs for error details
4. Contact system administrator

---

**Version**: 1.0  
**Last Updated**: 2024  
**Security Level**: Production Ready 