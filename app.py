#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Peter Simeth's basic flask pretty youtube downloader (v1.3)
https://github.com/petersimeth/basic-flask-template
© MIT licensed, 2018-2023
"""

from flask import Flask, render_template, request, url_for, flash, redirect
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

DEVELOPMENT_ENV = True

app = Flask(__name__)
app.config['SECRET_KEY'] = 'H82xzioef9H22O8DH0h_eçhw<he_'
# Flask-WTF requires this line
csrf = CSRFProtect(app)

findDestData = {}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/build")
def build():
    return render_template("build.html")


@app.route("/find", methods=["GET", "POST"])
def find():
    if request.method == 'POST':
        findDestData['distanceFromHome'] = request.form['distanceFromHome']
        return redirect(url_for('contact'))
    return render_template("find.html")


@app.route("/contact")
def contact():
    return render_template("contact.html", app_data=findDestData)


if __name__ == "__main__":
    app.run(debug=DEVELOPMENT_ENV)
