#!/usr/bin/env python3
"""
Test script for the authentication system.
"""

import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_auth_system():
    """Test the authentication system components."""
    print("🧪 Testing Authentication System...")
    
    try:
        # Test imports
        print("📦 Testing imports...")
        from src.core.auth import AuthService
        from src.core.auth.user_manager import UserManager, User
        from src.core.auth.session_manager import SessionManager
        print("✅ All imports successful")
        
        # Test user manager
        print("\n👤 Testing User Manager...")
        user_manager = UserManager("data/test_users.db")
        
        # Test user creation
        success = user_manager.create_user(
            username="testuser",
            email="test@example.com",
            full_name="Test User",
            password="testpass123",
            role="user"
        )
        print(f"✅ User creation: {'Success' if success else 'Failed'}")
        
        # Test authentication
        user = user_manager.authenticate_user("testuser", "testpass123")
        if user:
            print(f"✅ Authentication successful: {user.username}")
        else:
            print("❌ Authentication failed")
        
        # Test session manager
        print("\n🔐 Testing Session Manager...")
        session_manager = SessionManager("data/test_session.json")
        
        if user:
            session_manager.login(user, remember_me=True)
            print("✅ Session created")
            
            if session_manager.is_logged_in():
                print("✅ Session verification successful")
            else:
                print("❌ Session verification failed")
        
        # Test auth service
        print("\n🔧 Testing Auth Service...")
        auth_service = AuthService()
        
        success, message = auth_service.login("testuser", "testpass123")
        print(f"✅ Auth service login: {message}")
        
        if auth_service.is_logged_in():
            current_user = auth_service.get_current_user()
            print(f"✅ Current user: {current_user.full_name}")
        
        # Cleanup
        print("\n🧹 Cleaning up test files...")
        try:
            os.remove("data/test_users.db")
            os.remove("data/test_session.json")
            print("✅ Test files cleaned up")
        except:
            print("⚠️  Could not clean up test files")
        
        print("\n🎉 Authentication system test completed successfully!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_auth_system() 