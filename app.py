#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Peter Simeth's basic flask pretty youtube downloader (v1.3)
https://github.com/petersimeth/basic-flask-template
© MIT licensed, 2018-2023
"""

from flask import Flask, render_template

DEVELOPMENT_ENV = True

app = Flask(__name__)

app_data = {
    "name": "Start planning !",
    "description": "An app to help you plan your next trip",
    "author": "Salomé Marie",
    "html_title": "Start planning !",
    "project_name": "Trip Planning",
    "keywords": "flask, webapp, template, basic",
}


@app.route("/")
def index():
    return render_template("index.html", app_data=app_data)


@app.route("/build")
def build():
    return render_template("build.html", app_data=app_data)


@app.route("/find")
def find():
    return render_template("find.html", app_data=app_data)


@app.route("/contact")
def contact():
    return render_template("contact.html", app_data=app_data)


if __name__ == "__main__":
    app.run(debug=DEVELOPMENT_ENV)
