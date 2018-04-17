from functools import partial, wraps
from flask import current_app, g, abort, redirect
from werkzeug.local import LocalProxy
from werkzeug.urls import Href
from flask_jwt_simple import JWTManager, create_jwt, get_jwt_identity, jwt_required
from authlib.flask.client import OAuth
from authlib.client.apps import register_apps, get_app
from word_noter.web.model import User

oauth = OAuth()
jwt = JWTManager()


def login(user_info):
    user = User.create_or_update(user_info)
    token = create_jwt(identity=user.id)
    redirect_url = current_app.config.get('AUTH_REDIRECT_URL', None)
    if redirect_url is None:
        return token
    return redirect(Href(redirect_url)(token=token))


def get_current_user():
    user = g.get('user', None)
    if user:
        return user
    identity = get_jwt_identity()
    if not identity:
        return None
    user = User.query.get(identity)
    g.user = user
    return user


current_user = LocalProxy(get_current_user)
google_oauth_service = LocalProxy(partial(get_app, 'google'))


def require_login(f):
    @wraps(f)
    @jwt_required
    def decorated(*args, **kargs):
        if not current_user:
            abort(401)
        return f(*args, **kargs)

    return decorated


def init_app(app):
    oauth.init_app(app)
    register_apps(oauth, ['google'])
    jwt.init_app(app)
