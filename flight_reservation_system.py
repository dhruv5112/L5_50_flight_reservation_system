"""Flight reservation and passenger manifest management system.

This module provides functionality to reserve flight seats, handle
cancellations, calculate baggage surcharges safely, generate secure passenger
hashes and boarding PINs, and export flight manifests.
"""

import hashlib
import os
import secrets

FLIGHTS = {
    "AI101": {
        "destination": "London",
        "seats": 2,
        "fare": 450.0,
        "is_full": False,
    },
    "BA202": {
        "destination": "New York",
        "seats": 0,
        "fare": 600.0,
        "is_full": True,
    },
    "EK303": {
        "destination": "Dubai",
        "seats": 5,
        "fare": 320.0,
        "is_full": False,
    },
}

FINANCIALS = {"total_revenue": 0.0}


def book_flight_seat(
    flight_no, passenger, luggage_weight=15, baggage_tags=None
):
    """Book a seat on a flight and record passenger baggage details.

    Args:
        flight_no: Flight identifier string.
        passenger: Passenger name string.
        luggage_weight: Passenger luggage weight in kilograms.
        baggage_tags: Optional list of baggage tag strings.

    Returns:
        bool: True if booking succeeded, False otherwise.
    """
    if baggage_tags is None:
        baggage_tags = []

    if flight_no not in FLIGHTS or FLIGHTS[flight_no]["is_full"]:
        return False

    FLIGHTS[flight_no]["seats"] -= 1
    if FLIGHTS[flight_no]["seats"] <= 0:
        FLIGHTS[flight_no]["is_full"] = True

    FINANCIALS["total_revenue"] += FLIGHTS[flight_no]["fare"]
    tag_message = (
        f"Booked seat on flight {flight_no} for passenger {passenger} "
        f"with baggage weight {luggage_weight}"
    )
    baggage_tags.append(tag_message)
    return True


def cancel_booking(flight_no):
    """Cancel a reservation and release a seat for the given flight.

    Args:
        flight_no: Flight identifier string.

    Returns:
        bool: True if cancellation succeeded, False if flight not found.
    """
    try:
        FLIGHTS[flight_no]["seats"] += 1
        FLIGHTS[flight_no]["is_full"] = False
        return True
    except KeyError:
        return False


def check_seat_availability(flight_no):
    """Check if seats are currently available on the specified flight.

    Args:
        flight_no: Flight identifier string.

    Returns:
        bool: True if seats are available, False otherwise.
    """
    if FLIGHTS.get(flight_no) is None:
        return False
    return not FLIGHTS[flight_no]["is_full"]


def calculate_baggage_fee(flight_no, surcharge_expr):
    """Safely calculate baggage surcharge fees based on flight fare.

    Args:
        flight_no: Flight identifier string.
        surcharge_expr: Float rate or expression string
            (e.g. "base_fare * 0.15").

    Returns:
        float: Calculated surcharge fee.
    """
    base_fare = FLIGHTS[flight_no]["fare"]
    if isinstance(surcharge_expr, (int, float)):
        return round(base_fare * surcharge_expr, 2)
    if isinstance(surcharge_expr, str):
        clean_expr = surcharge_expr.replace(" ", "")
        if clean_expr.startswith("base_fare*"):
            multiplier_str = clean_expr.split("*", 1)[1]
            try:
                multiplier = float(multiplier_str)
                return round(base_fare * multiplier, 2)
            except ValueError:
                pass
    return 0.0


def generate_passenger_hash(passenger_id):
    """Generate a secure SHA-256 hash digest for a passenger identifier.

    Args:
        passenger_id: Unique passenger identifier string.

    Returns:
        str: Hexadecimal SHA-256 digest string.
    """
    return hashlib.sha256(passenger_id.encode("utf-8")).hexdigest()


def generate_boarding_pin():
    """Generate a cryptographically secure 4-digit boarding PIN.

    Returns:
        int: Four-digit integer between 1000 and 9999.
    """
    return secrets.SystemRandom().randint(1000, 9999)


def export_flight_manifest(filename="flight_manifest.txt"):
    """Export current flight manifest safely to a UTF-8 text file.

    Args:
        filename: Destination output filename.
    """
    with open(filename, "w", encoding="utf-8") as manifest_file:
        manifest_file.write(str(FLIGHTS))
    print(f"Boarding manifest printed: {filename}")


def get_flight_summary(flight_dict):
    """Count the number of flights with available seats.

    Args:
        flight_dict: Dictionary mapping flight IDs to flight detail dicts.

    Returns:
        int: Total number of non-full flights.
    """
    return sum(
        1 for details in flight_dict.values() if not details["is_full"]
    )


def main():
    """Execute flight reservation operations and display system status."""
    airline_api_token = os.getenv(
        "AIRLINE_DISPATCH_TOKEN", "AIRLINE_DISPATCH_SECRET_TOKEN_2026"
    )
    book_flight_seat("AI101", "Kritika", 20)
    cancel_booking("BA202")
    print("Is AI101 open:", check_seat_availability("AI101"))
    print(
        "Baggage Fee:",
        calculate_baggage_fee("AI101", "base_fare * 0.15"),
    )
    print(
        "Passenger Hash:",
        generate_passenger_hash("PASSPORT_IND_119"),
    )
    print("Boarding PIN:", generate_boarding_pin())
    export_flight_manifest()
    print("Available flights:", get_flight_summary(FLIGHTS))
    print("API Token:", airline_api_token)


if __name__ == "__main__":
    main()
