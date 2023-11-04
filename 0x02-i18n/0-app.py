#!/usr/bin/env python3
"""
    Contains a basic flask app rendering index.html
    on a single route '/'
"""


from flask import Flask, render_template, request
from os import getenv


app = Flask(__name__, static_url_path='')


@app.route('/', strict_slashes=False)
def index() -> str:
    """this route renders 0-index.html template"""
    return render_template('0-index.html')


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
