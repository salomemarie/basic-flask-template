#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Peter Simeth's basic flask pretty youtube downloader (v1.3)
https://github.com/petersimeth/basic-flask-template
© MIT licensed, 2018-2023
"""

import config
from flask import Flask, render_template
from api.find_routes import find_bp
from api.build_routes import build_bp

DEVELOPMENT_ENV = True

app = Flask(__name__)
app.config['SECRET_KEY'] = config.SECRET_KEY


app.register_blueprint(find_bp)
app.register_blueprint(build_bp)
@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=DEVELOPMENT_ENV)
