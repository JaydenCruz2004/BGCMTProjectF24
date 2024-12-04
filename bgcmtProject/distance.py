from geopy.geocoders import Nominatim
from geopy.distance import geodesic

def get_distance(address1, address2):
    """Calculates the distance between two addresses in kilometers."""

    geolocator = Nominatim(user_agent="distance_calculator")

    # Get coordinates for address1
    location1 = geolocator.geocode(address1)
    if location1 is None:
        return "Address 1 not found"
    coords1 = (location1.latitude, location1.longitude)

    # Get coordinates for address2
    location2 = geolocator.geocode(address2)
    if location2 is None:
        return "Address 2 not found"
    coords2 = (location2.latitude, location2.longitude)

    # Calculate distance
    distance = geodesic(coords1, coords2).km

    return distance

if __name__ == "__main__":
    address1 = input("Enter the first address: ")
    address2 = input("Enter the second address: ")

    distance = get_distance(address1, address2)

    if isinstance(distance, str):  # Error handling
        print(distance)
    else:
        print(f"The distance between the two addresses is: {distance:.2f} km")