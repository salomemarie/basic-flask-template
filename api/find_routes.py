from flask import Blueprint, render_template, request, redirect, url_for
from api.utils import clean_and_parse_json, fetch_and_add_new_places
from data.shared_data import places, likedPlaces, findDestData, previousPrepositions


find_bp = Blueprint('find_bp', __name__)

@find_bp.route("/find", methods=["GET", "POST"])
def find():
    if request.method == 'POST':
        findDestData['distanceFromHome'] = request.form.get('distanceFromHome', 'No distance preference provided')
        findDestData['tripType'] = request.form.get('tripType', 'No trip type specified')
        findDestData['pastVacations'] = request.form.get('pastVacations', 'No past vacations listed')
        findDestData['extraInformation'] = request.form.get('extraInformation', 'No extra information given')
        findDestData["likedPropositions"] = likedPlaces
        findDestData["previousPropositions"] = previousPrepositions

        fetch_and_add_new_places()
        return redirect(url_for('find_bp.destinations'))
    return render_template("find.html")

@find_bp.route('/like', methods=['POST'])
def toggle_like():
    city = request.form.get('city')
    country = request.form.get('country')

    for place in places:
        if place['city'] == city and place['country'] == country:
            place['liked'] = not place.get('liked', False)
            place_dict = {"city": city, "country": country}

            if place['liked']:
                if place_dict not in likedPlaces:
                    likedPlaces.append(place_dict)
            else:
                likedPlaces[:] = [p for p in likedPlaces if p != place_dict]
            break

    return redirect(url_for('find_bp.destinations'))

@find_bp.route('/more-info', methods=['POST'])
def more_info():
    city = request.form.get('city')
    country = request.form.get('country')
    
    # Logic to fetch extra info, maybe set place['extraInfo'] or redirect to a detail page
    return f"More info coming soon for {city}, {country}."

@find_bp.route('/refresh', methods=['POST'])
def refresh_places():

    for place in places:
        if place.get("isShown", True):
            previousPrepositions.append({"city": place["city"], "country": place["country"]})
            place['isShown'] = False

    findDestData["likedPropositions"] = likedPlaces
    findDestData["previousPropositions"] = previousPrepositions

    fetch_and_add_new_places()

    return redirect(url_for('find_bp.destinations'))


@find_bp.route('/destinations', methods=['GET'])
def destinations():
    return render_template('destinations.html', places=places)