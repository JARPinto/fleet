from flask import session, redirect
from functools import wraps
import calendar

def login_required(f):
    """
    Decorate routes to require login.
    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


# This function passes a str to int and them to month name
def str_to_month(x):
    """
    STR to INT
    INT to month name
    Good to populate array
    """
    i = int(x)
    return calendar.month_name[i]