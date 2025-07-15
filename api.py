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
                        I want you to help me find 3 vacation destinations that I would enjoy.

                        Without introduction or conclusion, jump right into the destinations
                        For each destination:
                        - Give me one strong positive reason to go there
                        - And one thing I should watch out for

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