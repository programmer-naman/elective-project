import json
import bcrypt
import os

USER_FILE = "users.json"

def load_users():
    """Load existing users from JSON file."""
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    """Save users to JSON file."""
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=4)


def register_user():
    users = load_users()
    print("\n--- User Registration ---")
    email = input("Enter email: ").strip()

    if email in users:
        print("User already exists!")
        return

    password = input("Enter password: ").strip()
    role = input("Enter role (student/institution/employer): ").strip().lower()

    if role not in ["student", "institution", "employer"]:
        print("Invalid role! Must be student/institution/employer.")
        return

    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    users[email] = {
        "password": hashed_pw,
        "role": role
    }

    save_users(users)
    print("Registration successful!")


def login_user():
    users = load_users()
    print("\n--- User Login ---")
    email = input("Enter email: ").strip()
    password = input("Enter password: ").strip()

    if email not in users:
        print("User not found!")
        return None

    stored_hash = users[email]["password"].encode()
    if bcrypt.checkpw(password.encode(), stored_hash):
        print(f"Login successful! Welcome, {users[email]['role'].capitalize()}.")
        return users[email]["role"]
    else:
        print("Incorrect password!")
        return None


def list_all_users():
    """Display all registered users (for testing/admin purpose)."""
    users = load_users()
    print("\nRegistered Users:")
    for email, data in users.items():
        print(f" {email} - Role: {data['role']}")