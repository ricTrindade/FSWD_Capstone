import json
from flask import request, _request_ctx_stack, abort, jsonify
from functools import wraps
from jose import jwt
from urllib.request import urlopen


AUTH0_DOMAIN = 'pragmatic-dev.uk.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'capstone'

## AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

## Auth Header
def get_token_auth_header():
    # Make sure that Authorization is sent in request
    if 'Authorization' not in request.headers:
        abort(401)

    # Get Authorization Info
    auth_header = request.headers['Authorization']
    header_parts = auth_header.split(' ')

    # Make Sure Authorization is a Bearer Token
    if len(header_parts) != 2:
        abort(401)
    elif header_parts[0].lower() != 'bearer':
        abort(401)

    return header_parts[1]

## Check JWT Permissions
def check_permissions(permission, payload):
    # Verify that Payload Contains the 'permission' key
    if 'permissions' not in payload:
        abort(400)

    # Check that Required permission is Present
    if permission not in payload['permissions']:
        abort(403)

    # Passed all checks
    return True

# !!NOTE urlopen has a common certificate error described here: https://stackoverflow.com/questions/50236117/scraping-ssl-certificate-verify-failed-error-for-http-en-wikipedia-org
def verify_decode_jwt(token):

    # Get Public Key from Auth0
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())

    # Get the data in the header
    unverified_header = jwt.get_unverified_header(token)

    # Choose the Key
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code' : 'invalid_header',
            'description' : 'Authorisation malformed'
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

            # USE THE KEY TO VALIDATE THE JWT
            return jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer=f'https://{AUTH0_DOMAIN}/'
            )

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
        'code': 'invalid_header',
        'description': 'Unable to find the appropriate key.'
    }, 400)

# Requires Permission Decorator
def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            jwt_token = get_token_auth_header()
            try:
                payload = verify_decode_jwt(jwt_token)
                check_permissions(permission, payload)
            except AuthError as e:
                return jsonify({
                    'success': False,
                    'error': 403,
                    'message': e.error
                }), 403
            return f(payload, *args, **kwargs)
        return wrapper
    return requires_auth_decorator