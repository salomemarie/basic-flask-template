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
import json, re
from flask import Flask, render_template, request, url_for, flash, redirect

DEVELOPMENT_ENV = True

app = Flask(__name__)
app.config['SECRET_KEY'] = config.SECRET_KEY

findDestData = {}
places = []
likedPlaces = []
previousPrepositions = []


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/build")
def build():
    return render_template("build.html")


@app.route("/find", methods=["GET", "POST"])
def find():
    if request.method == 'POST':
        findDestData['distanceFromHome'] = request.form.get('distanceFromHome', 'No distance preference provided')
        findDestData['tripType'] = request.form.get('tripType', 'No trip type specified')
        findDestData['pastVacations'] = request.form.get('pastVacations', 'No past vacations listed')
        findDestData['extraInformation'] = request.form.get('extraInformation', 'No extra information given')
        findDestData["likedPropositions"] = likedPlaces
        findDestData["previousPropositions"] = previousPrepositions

        fetch_and_add_new_places()
        return redirect(url_for('destinations'))
    return render_template("find.html")


@app.route('/destinations', methods=['GET'])
def destinations():
    return render_template('destinations.html', places=places)


@app.route('/like', methods=['POST'])
def toggle_like():
    city = request.form.get('city')
    country = request.form.get('country')

    for place in places:
        if place['city'] == city and place['country'] == country:
            place['liked'] = not place['liked']
            if place['liked'] == True :
                likedPlaces.append({"city": place["city"], "country": place["country"]})
            else:
                likedPlaces.remove({"city": place["city"], "country": place["country"]})
            break

    return redirect(url_for('destinations'))

@app.route('/more-info', methods=['POST'])
def more_info():
    city = request.form.get('city')
    country = request.form.get('country')
    
    # Logic to fetch extra info, maybe set place['extraInfo'] or redirect to a detail page
    return f"More info coming soon for {city}, {country}."

@app.route('/refresh', methods=['POST'])
def refresh_places():

    for place in places:
        if place.get("isShown", True):
            previousPrepositions.append({"city": place["city"], "country": place["country"]})
            place['isShown'] = False

    findDestData["likedPropositions"] = likedPlaces
    findDestData["previousPropositions"] = previousPrepositions

    fetch_and_add_new_places()

    return redirect(url_for('destinations'))



def clean_and_parse_json(raw):
    if isinstance(raw, list):  # Already parsed
        return raw

    if not isinstance(raw, str):
        raise ValueError("Input must be a string or list")

    # Extract just the JSON array
    match = re.search(r'\[\s*{.*?}\s*\]', raw, re.DOTALL)
    if not match:
        raise ValueError("Could not find JSON array in the response")

    json_str = match.group(0)
    return json.loads(json_str)

def fetch_and_add_new_places():
    rawPlacesData = api.getPlaces(findDestData=findDestData)
    jsonPlacesData = clean_and_parse_json(rawPlacesData)
    places.extend(jsonPlacesData)

if __name__ == "__main__":
    app.run(debug=DEVELOPMENT_ENV)
