#!/usr/bin/env python3
"""
    Contains a basic flask app displaying 'Welcome to Holberton' on
    a single route '/'
"""


from flask import Flask, g, render_template, request
from flask_babel import Babel
from os import getenv

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


app = Flask(__name__, static_url_path='')
babel = Babel(app)


class Config(object):
    """configuration for babel"""
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app.config.from_object(Config)


@app.route('/', methods=['GET'], strict_slashes=False)
def index() -> str:
    """this route renders 0-index.html template"""
    return render_template('6-index.html')


@babel.localeselector
def get_locale() -> str:
    """this method checks the URL parameter for locale variable
    and force the Locale of the app"""
    if request.args.get('locale'):
        lang = request.args.get('locale')
        if lang in app.config['LANGUAGES']:
            return lang
    if g.user:
        lang = g.user.get('locale')
        if lang in app.config['LANGUAGES']:
            return lang
    lang = request.headers.get('locale', None)
    if lang:
        if lang in app.config['LANGUAGES']:
            return lang
    else:
        return request.accept_languages.best_match(app.config['LANGUAGES'])


def get_user():
    """this function returns a user dictionary or None if the ID
    cannot be found or if login_as was not passed"""
    userId = request.args.get('login_as', None)
    if userId:
        return users.get(int(userId))
    return None


@app.before_request
def before_request():
    """this function forces this method to be executed before any other"""
    g.user = get_user()


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
