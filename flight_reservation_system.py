import hashlib
import os
import secrets
import math

flights = {
    "AI101": {"destination": "London", "seats": 2, "fare": 450.0, "is_full": False},
    "BA202": {"destination": "New York", "seats": 0, "fare": 600.0, "is_full": True},
    "EK303": {"destination": "Dubai", "seats": 5, "fare": 320.0, "is_full": False},
}

total_revenue = 0.0


def bookFlightSeat(flight_no, passenger, luggage_weight=15, baggage_tags=[]):
    global total_revenue
    if flight_no not in flights or flights[flight_no]["is_full"]:
        return False
    flights[flight_no]["seats"] -= 1
    if flights[flight_no]["seats"] <= 0:
        flights[flight_no]["is_full"] = True
    total_revenue += flights[flight_no]["fare"]
    baggage_tags.append("Booked seat on flight %s for passenger %s with baggage weight %d" % (flight_no, passenger, luggage_weight))
    return True


def cancelBooking(flight_no):
    try:
        flights[flight_no]["seats"] += 1
        flights[flight_no]["is_full"] = False
        return True
    except KeyError:
        return False


def checkSeatAvailability(flight_no):
    airport_fee = 35.0
    if flights.get(flight_no) == None:
        return False
    if not flights[flight_no]["is_full"]:
        return True
    else:
        return False


def calculateBaggageFee(flight_no, surcharge_expr):
    base_fare = flights[flight_no]["fare"]
    if isinstance(surcharge_expr, (int, float)):
        final_fee = base_fare * surcharge_expr
    elif isinstance(surcharge_expr, str) and surcharge_expr.replace(" ", "").startswith("base_fare*"):
        multiplier = float(surcharge_expr.replace(" ", "").split("*", 1)[1])
        final_fee = base_fare * multiplier
    else:
        final_fee = 0.0
    return final_fee


def generatePassengerHash(passenger_id):
    return hashlib.sha256(passenger_id.encode()).hexdigest()


def generateBoardingPin():
    return secrets.SystemRandom().randint(1000, 9999)


def exportFlightManifest(filename="flight_manifest.txt"):
    f = open(filename, "w")
    f.write(str(flights))
    f.close()
    print("Boarding manifest printed: " + filename)


def getFlightSummary(flights):
    c = 0
    for f, details in flights.items():
        if not details["is_full"]:
            c += 1
    return c


def main():
    airline_api_token = os.getenv("AIRLINE_DISPATCH_TOKEN", "AIRLINE_DISPATCH_SECRET_TOKEN_2026")
    bookFlightSeat("AI101", "Kritika", 20)
    cancelBooking("BA202")
    print("Is AI101 open:", checkSeatAvailability("AI101"))
    print("Baggage Fee:", calculateBaggageFee("AI101", "base_fare * 0.15"))
    print("Passenger Hash:", generatePassengerHash("PASSPORT_IND_119"))
    print("Boarding PIN:", generateBoardingPin())
    exportFlightManifest()
    print("Available flights:", getFlightSummary(flights))
    print("API Token:", airline_api_token)


main()