from flask import Blueprint, url_for, jsonify
from word_noter.web import auth

bp = Blueprint('auth', __name__)


@bp.route('/login')
def login():
    """Redirect url to OAuth login page

        :return:
        """
    callback_uri = url_for('.login_callback', _external=True)
    return auth.google_oauth_service.authorize_redirect(callback_uri)


@bp.route('/login_callback')
def login_callback():
    """OAuth login callback

        This method does:
            1. Exchange access token from code
            2. Obtain user profile using access token
            3. Create or update user data using the profile
            4. Generate login token
            5. Redirect to url that set from config with token as parameter
        :return:
        """
    auth.google_oauth_service.authorize_access_token()
    user_info = auth.google_oauth_service.profile()
    return auth.login(user_info)


# TODO maybe put this into user route later
@bp.route('/profile')
@auth.require_login
def profile():
    user = auth.current_user
    return jsonify(user.to_dict())


def init_app(app):
    app.register_blueprint(bp)
