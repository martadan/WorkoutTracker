import json
from flask import request
from functools import wraps
from jose import jwt
from urllib.request import urlopen

DOMAIN = 'dev-l4529u72.auth0.com'
ALGORITHMS = ['RS256']
AUDIENCE = 'workout'


class CustomAuthError(Exception):
    """
    Custom Exception class to communicate details of authorization error back to app.py
    """
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def get_token_auth_header():
    """
    Splits out bearer token from authorization header
    """
    authorization = request.headers.get('Authorization', None)

    if authorization is None:
        raise CustomAuthError({
            'code': 'authorization_header_missing',
            'description': 'Authorization header is expected.'
        }, 401)

    auth_parts = authorization.split()

    if auth_parts[0].lower() != 'bearer':
        raise CustomAuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must start with "Bearer".'
        }, 401)

    elif len(auth_parts) < 2:
        raise CustomAuthError({
            'code': 'invalid_header',
            'description': 'Token not found.'
        }, 401)

    elif len(auth_parts) > 2:
        raise CustomAuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must be bearer token.'
        }, 401)

    token = auth_parts[1]
    return token


def check_permissions(permission, payload):
    """
    Checks if string permission is in payload jwt
    (Copied from BasicFlaskAuth)
    """
    if 'permissions' not in payload:
        raise CustomAuthError({
            'code': 'invalid_claims',
            'description': 'Permissions not included in JWT.'
        }, 400)

    if permission not in payload['permissions']:
        raise CustomAuthError({
            'code': 'unauthorized',
            'description': 'Permission not found.'
        }, 403)

    return True


def verify_decode_jwt(token):
    """
    Returns payload from jwt (and verifies jwt is correct)
    """
    jsonurl = urlopen(f'https://{DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}

    if 'kid' not in unverified_header:
        raise CustomAuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }

    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=AUDIENCE,
                issuer=f'https://{DOMAIN}/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise CustomAuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise CustomAuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)

        except Exception:
            raise CustomAuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)

    raise CustomAuthError({
        'code': 'invalid_header',
        'description': 'Unable to find the appropriate key.'
    }, 401)


def requires_auth(permission=''):
    """
    Wrapper function for authenticating request (check token, check for permissions)
    No payload in f() return - current functions don't take a payload
    """
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(*args, **kwargs)

        return wrapper
    return requires_auth_decorator
