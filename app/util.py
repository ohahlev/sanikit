import uuid

env = "ENVIRONMENT"
dev = "dev"
test = "test"
prod = "prod"

timeout = 60

recent_days = 30

about = {
    "type": "ABOUT",
    "text": "this is about"
}

contact = {
    "type": "CONTACT",
    "text": "this is contact"
}

# form
email_required = "email is required"
email_invalid = "invalid email"
password_required = "password is required"

# flash
wrong_email_or_password = "wrong email or password"
something_wrong = "something went wrong, please contact admin"
success = "success"
undefined = "undefined"

# max per page
PER_PAGE = 10

# default sorted by field
DEFAULT_SORT = "last_updated"

# empty value
EMPTY = "3MPT2"

def get_empty():
    return uuid.uuid4().hex


