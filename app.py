#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Peter Simeth's basic flask pretty youtube downloader (v1.3)
https://github.com/petersimeth/basic-flask-template
© MIT licensed, 2018-2023
"""

from flask import Flask, render_template, request, url_for, flash, redirect

DEVELOPMENT_ENV = True

app = Flask(__name__)
app.config['SECRET_KEY'] = 'd6e1db7bc1d7a23c4a3d0bf072bb09acc45802b00e58e543'

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
        findDestData['tripType'] = request.form['tripType']
        findDestData['pastVacations'] = request.form['pastVacations']
        findDestData['extraInformation'] = request.form['extraInformation']
        return redirect(url_for('contact'))
    return render_template("find.html")


@app.route("/contact")
def contact():
    return render_template("contact.html", app_data=findDestData)


if __name__ == "__main__":
    app.run(debug=DEVELOPMENT_ENV)
