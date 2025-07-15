#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Peter Simeth's basic flask pretty youtube downloader (v1.3)
https://github.com/petersimeth/basic-flask-template
© MIT licensed, 2018-2023
"""

import config
import api
import markdown
from flask import Flask, render_template, request, url_for, flash, redirect

DEVELOPMENT_ENV = True

app = Flask(__name__)
app.config['SECRET_KEY'] = config.SECRET_KEY

findDestData = {}
places = {}


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
        places["places"] = api.getPlaces(findDestData=findDestData)
        return redirect(url_for('contact'))
    return render_template("find.html")


@app.route("/contact")
def contact():
    response_markdown = places.get("places", "")
    response_html = markdown.markdown(response_markdown)
    return render_template("contact.html", app_data=places, recommendation_html=response_html)


if __name__ == "__main__":
    app.run(debug=DEVELOPMENT_ENV)
