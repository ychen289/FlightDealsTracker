from data_manager import DataManager
from flight_search import FlightSearch
from datetime import datetime, timedelta
from notification_manager import NotificationManager

flightsData = DataManager()
sheet_data = flightsData.getData()
ORIGIN_CITY_IATA = "NYC"
flightSearch = FlightSearch()
notificationManager = NotificationManager()

for entry in sheet_data:
    if entry["iataCode"] == "":
        cityName = entry["city"]
        entry["iataCode"] = flightSearch.get_destination_code(cityName)

flightsData.updateData(sheet_data)

tommorow = datetime.now() + timedelta(1)
six_months_from_now = datetime.now() + timedelta(180)
#                                  6 months x 30 days

for entry in sheet_data:
    flight = flightSearch.checkFlights(
        originCityCode=ORIGIN_CITY_IATA,
        destinationCityCode=entry["city"],
        dateFrom=tommorow,
        dateTo=six_months_from_now,
    )
    if flight == None:
        print("nothing was returned")
    else:
        if flight.price < entry["lowestPrice"]:
            notificationManager.send_sms(
                message=f"Low price alert! Only ${flight.price} to fly from {flight.origin_city}-{flight.origin_airport} to {flight.destination_city}-{flight.destination_airport}, from {flight.out_date} to {flight.return_date}."
            )
