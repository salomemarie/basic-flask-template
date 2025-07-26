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
                """
            },
        ]
    )
    return chat_response.choices[0].message.content