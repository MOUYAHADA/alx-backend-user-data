#!/usr/bin/env python3
"""
Basic flask app integration testing
"""
import requests


def register_user(email: str, password: str) -> None:
    """Register a new user
    """
    res = requests.post('http://0.0.0.0:5000/users', data={
        "email": email,
        "password": password
    })
    if res.ok:
        assert res.status_code == 200
        assert res.json() == {"email": email, "message": "user created"}
    else:
        assert res.status_code == 400
        assert res.json() == {"message": "email already registered"}


def log_in_wrong_password(email: str, password: str) -> None:
    """Log in with a wrong password
    """
    res = requests.post('http://0.0.0.0:5000/sessions', data={
        "email": email,
        "password": password
    })

    assert res.status_code == 401


def log_in(email: str, password: str) -> str:
    """Log in with correct password
    Returns:
        str: session id
    """
    res = requests.post('http://0.0.0.0:5000/sessions', data={
        "email": email,
        "password": password
    })

    assert res.ok
    assert res.json() == {"email": email, "message": "logged in"}

    return res.cookies.get('session_id')


def profile_unlogged() -> None:
    """Request user's profile without being logged in
    """
    res = requests.get('http://0.0.0.0:5000/profile')
    assert res.status_code == 403


def profile_logged(session_id: str) -> None:
    """Request user profile while logged in
    """
    res = requests.get('http://0.0.0.0:5000/profile',
                       cookies={"session_id": f"{session_id}"})

    assert res.status_code == 200 and res.json().get('email')


def log_out(session_id: str) -> None:
    """Log out and destroy user session
    """
    res = requests.delete('http://0.0.0.0:5000/sessions',
                          cookies={"session_id": f"{session_id}"})
    assert res.ok


def reset_password_token(email: str) -> str:
    """get password reset token
    Returns:
        str: reset token
    """
    res = requests.post('http://0.0.0.0:5000/reset_password',
                        data={"email": email})
    data = res.json()

    assert res.ok and data.get('email') and data.get('reset_token')

    return data.reset_token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Update user password using reset token
    """
    res = requests.put('http://0.0.0.0:5000/reset_password',
                       data={
                           "email": email,
                           "reset_token": reset_token,
                           "new_password": new_password
                       })
    data = res.json()

    assert res.ok
    assert data == {"email": email, "message": "Password updated"}


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
