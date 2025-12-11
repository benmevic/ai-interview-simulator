import hashlib
import secrets
from typing import Optional, Tuple
from database.db_manager import DatabaseManager

class AuthService:
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
    
    @staticmethod
    def hash_password(password: str, salt: Optional[str] = None) -> Tuple[str, str]:
        """Hash a password with a salt using SHA-256."""
        if salt is None:
            salt = secrets.token_hex(32)
        
        password_hash = hashlib.sha256((password + salt).encode()).hexdigest()
        # Store both hash and salt together
        combined = f"{salt}${password_hash}"
        return combined, salt
    
    @staticmethod
    def verify_password(password: str, stored_hash: str) -> bool:
        """Verify a password against a stored hash."""
        try:
            salt, password_hash = stored_hash.split('$')
            new_hash = hashlib.sha256((password + salt).encode()).hexdigest()
            return new_hash == password_hash
        except ValueError:
            return False
    
    def register_user(self, username: str, email: str, password: str) -> Tuple[bool, str]:
        """Register a new user.
        
        Returns:
            Tuple of (success: bool, message: str)
        """
        # Validate input
        if len(username) < 3:
            return False, "Username must be at least 3 characters long"
        
        if len(password) < 6:
            return False, "Password must be at least 6 characters long"
        
        if '@' not in email:
            return False, "Invalid email address"
        
        # Check if user already exists
        if self.db.get_user_by_username(username):
            return False, "Username already exists"
        
        if self.db.get_user_by_email(email):
            return False, "Email already registered"
        
        # Hash password and create user
        password_hash, _ = self.hash_password(password)
        user_id = self.db.create_user(username, email, password_hash)
        
        if user_id:
            return True, "Registration successful"
        else:
            return False, "Registration failed. Please try again."
    
    def login_user(self, username: str, password: str) -> Tuple[bool, Optional[dict], str]:
        """Authenticate a user.
        
        Returns:
            Tuple of (success: bool, user_data: dict or None, message: str)
        """
        user = self.db.get_user_by_username(username)
        
        if not user:
            return False, None, "Invalid username or password"
        
        if self.verify_password(password, user['password_hash']):
            # Don't return password hash to the caller
            user_data = {
                'id': user['id'],
                'username': user['username'],
                'email': user['email'],
                'created_at': user['created_at']
            }
            return True, user_data, "Login successful"
        else:
            return False, None, "Invalid username or password"
    
    def get_user_info(self, user_id: int) -> Optional[dict]:
        """Get user information by ID (without password hash)."""
        user = self.db.get_user_by_id(user_id)
        
        if user:
            return {
                'id': user['id'],
                'username': user['username'],
                'email': user['email'],
                'created_at': user['created_at']
            }
        return None