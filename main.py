import uuid

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from swiftcrypt import swiftcrypt

from database_functions import set_account_data, get_account_data, accounts_db, set_auth_token, auth_token_db, \
    delete_auth_token, set_booking_data, bookings_db

# Create FastAPI object
app = FastAPI()

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# User class
class User(BaseModel):
    first_name: str
    surname: str
    email: str
    password: str

# Booking class
class Booking(BaseModel):
    email: str
    date: str
    topic: str
    phoneNumber: str


# Hashing function
def hash_password(password, salt):
    return swiftcrypt.Hash().hash_password(password, salt, "sha256")

# Generate and save an authentication token
def create_auth_token(user):
    uuid_str = str(uuid.uuid4())
    print(user)
    if isinstance(user, User):
        auth_token_user = { "email": user.email }
    else:
        auth_token_user = { "email": user['email'] }

    set_auth_token(uuid_str, auth_token_user)

    return uuid_str

# Registration endpoint
@app.post("/register")
async def register(user: User):
    if user.email in accounts_db:
        return False

    salt = swiftcrypt.Salts().generate_salt(4)
    hashed_password = hash_password(user.password, salt)

    set_account_data(user.email, {
        "first_name": user.first_name,
        "surname": user.surname,
        "email": user.email,
        "password": hashed_password,
        "salt": salt,
    })
    return create_auth_token(user)


# Login endpoint
@app.get("/login")
def login(email, password):
    print("sent")
    if email not in accounts_db:
        return {"result": False, "message": "Account not found"}

    user = get_account_data(email)
    print(user)
    hashed_password = hash_password(password, user["salt"])
    if hashed_password == user['password']:
        return {"result": True, "auth_token": create_auth_token(user)}

    return {"result": False, "message": "Incorrect password"}

# Authentication token validation
@app.get("/validate_auth_token")
async def login(auth_token):
    if auth_token not in auth_token_db:
        return False
    else:
        return get_account_data(auth_token_db[auth_token]["email"])

# Logout
@app.get("/logout")
async def logout(auth_token):
    if auth_token in auth_token_db:
        delete_auth_token(auth_token)
        return {"result": "success"}

    return {"result": "unknown error"}

# Registration endpoint
@app.post("/book/")
async def book(booking: Booking):
    print("Book")
    for (key, value) in bookings_db.items():
        if value["email"] == booking.email:
            print("return false")
            return False

    print("set booking data")
    set_booking_data(booking.date, {'email': booking.email, 'topic': booking.topic, 'phoneNumber': booking.phoneNumber})
    return True