from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from app import app


def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])


def confirm_token(token, expiration=15): # 15 # 3600
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration
        )
    except SignatureExpired:
        raise Exception('Token has expired')
    except BadSignature:
        raise Exception('Invalid token')  # Raise exception when token is invalid
    return email