import jwt
from datetime import datetime, timedelta, timezone
from flask import current_app

def encode_auth_token(user_id):
    try:
        payload = {
            'exp': datetime.now(timezone.utc) + timedelta(hours=1),  # Expira en 1 hr,minutes, days
            'iat': datetime.now(timezone.utc),
            'sub': user_id
        }
        return jwt.encode(payload, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')
    except Exception as e:
        return str(e)

#obtiene el id del usuario
def decode_auth_token(auth_token):
    try:
        payload = jwt.decode(auth_token, current_app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
        return payload['sub']  # ID del usuario
    except jwt.ExpiredSignatureError:
        return "Signature expired. Please log in again."
    except jwt.InvalidTokenError:
        return "Invalid token. Please log in again."
