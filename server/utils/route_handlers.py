from datetime import datetime, timezone

from flask import current_app
from flask_jwt_extended import get_jwt, create_access_token, current_user, set_access_cookies


def handle_refresh_expiring_jwts(response, remember: bool):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + current_app.config.get('JWT_ACCESS_TOKEN_EXPIRES') / 2)
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=current_user)
            set_access_cookies(
                response,
                access_token,
                max_age=current_app.config['JWT_ACCESS_TOKEN_EXPIRES'] if remember else None
            )
        return response
    except (RuntimeError, KeyError):
        return response
