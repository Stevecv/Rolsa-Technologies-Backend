import json

# Database functions
# Load data
def load_accounts_db():
    with open('accounts_database.json') as f:
        d = json.load(f)
        return d
def load_auth_token_db():
    with open('auth_token_database.json') as f:
        d = json.load(f)
        return d
def load_bookings_db():
    with open('bookings.json') as f:
        d = json.load(f)
        return d

# Save data
def save_accounts_db():
    with open('accounts_database.json', 'w') as f:
        json.dump(accounts_db, f)
def save_auth_token_db():
    with open('auth_token_database.json', 'w') as f:
        json.dump(auth_token_db, f)
def save_bookings_db():
    with open('bookings.json', 'w') as f:
        json.dump(bookings_db, f)

# Set data
def set_account_data(key, data):
    accounts_db[key] = data
    save_accounts_db()
def set_auth_token(key, data):
    auth_token_db[key] = data
    save_auth_token_db()
def set_booking_data(key, data):
    bookings_db[key] = data
    save_bookings_db()

# Get data
def get_account_data(key):
    return accounts_db[key]
def get_auth_token_data(key):
    return auth_token_db[key]
def get_booking_data(key):
    return bookings_db[key]

# Delete data
def delete_account(email):
    del accounts_db[email]
    save_accounts_db()
def delete_auth_token(auth_token):
    del auth_token_db[auth_token]
    save_auth_token_db()
def delete_booking(auth_token):
    del bookings_db[auth_token]
    save_bookings_db()

accounts_db = load_accounts_db()
auth_token_db = load_auth_token_db()
bookings_db = load_bookings_db()