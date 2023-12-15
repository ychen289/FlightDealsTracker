from config import TEQUILA_KIWI_API_KEY
import requests
from flight_data import FlightData

headers = {"apikey": TEQUILA_KIWI_API_KEY}

TEQUILA_KIWI_ENDPOINT = "https://api.tequila.kiwi.com/locations/query"


class FlightSearch:
    # This class is responsible for talking to the Flight Search API.
    def get_destination_code(self, cityName):
        searchQuery = {"term": cityName, "location_types": "city"}
        response = requests.get(
            TEQUILA_KIWI_ENDPOINT, headers=headers, params=searchQuery
        )
        results = response.json()["locations"]
        code = results[0]["code"]
        return code

    def checkFlights(self, originCityCode, destinationCityCode, dateFrom, dateTo):
        searchQuery = {
            "fly_from": originCityCode,
            "fly_to": destinationCityCode,
            "date_from": dateFrom,
            "date_to": dateTo,
            # below are just selected queries (round trip, direct flight, etc)
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "one_for_city": 1,
            "max_stopovers": 0,
            "curr": "USD",
        }
        response = requests.get(
            f"{TEQUILA_KIWI_ENDPOINT}/search", params=searchQuery, headers=headers
        )
        try:
            results = response.json()["data"][0]
            results.raise_for_status()
        except IndexError:
            print("There weren't any flights to be found. ")
            return None

        flight_data = FlightData(
            price=results["price"],
            origin_city=results["route"][0]["cityFrom"],
            origin_airport=results["route"][0]["flyFrom"],
            destination_city=results["route"][0]["cityTo"],
            destination_airport=results["route"][0]["flyTo"],
            out_date=results["route"][0]["local_departure"].split("T")[0],
            return_date=results["route"][1]["local_departure"].split("T")[0],
        )
        
        print(f"{flight_data.destination_city}: USD{flight_data.price}")
        return flight_data
