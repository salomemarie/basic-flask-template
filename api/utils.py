import json, re
from data.shared_data import findDestData, places
import config
from mistralai import Mistral

model = "mistral-large-latest"

client = Mistral(api_key=config.API_KEY)

def getPlaces(findDestData):
    chat_response = client.chat.complete(
        model= model,
        messages = [
            {
                "role": "user",
                "content": f"""
                       I want you to return a list of 3 vacation destinations that I would enjoy, as structured `Place` objects in JSON format without including the word json.

                        Each `Place` should include:
                        - `city` (string): the name of the city
                        - `country` (string): the country it’s located in
                        - `liked` (boolean): default to false
                        - `goodThing` (string): one reason I would like this destination
                        - `watchOut` (string): one thing I should watch out for
                        - `isShown` (boolean): default to true

                        Return the list as a JSON array without any explanations or extra text.

                        Here’s my travel profile:
                        - Distance preference from home: {findDestData.get('distanceFromHome')}
                        - Type of trip I want: {findDestData.get('tripType')}
                        - Past trips I’ve taken: {findDestData.get('pastVacations')}
                        - Favorite past trip: {findDestData.get('favoriteVacation')}
                        - Other considerations (cost, crowd, etc.): {findDestData.get('extraInformation')}
                        - Places you have aleady recommended that I liked : {findDestData.get('likedPropositions')}
                        - Places that you have already recommened so try different ones :  {findDestData.get('previousPropositions')}
                """
            },
        ]
    )
    return chat_response.choices[0].message.content

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
    rawPlacesData = getPlaces(findDestData=findDestData)
    jsonPlacesData = clean_and_parse_json(rawPlacesData)
    places.extend(jsonPlacesData)

