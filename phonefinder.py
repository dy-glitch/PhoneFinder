import requests
from termcolor import colored
from urllib.parse import quote  # For URL encoding
from geopy.geocoders import Nominatim  # For simulating GPS

# Embedded API Keys
NUMVERIFY_API_KEY = ""  # Replace with your NumVerify API key
OPENCAGE_API_KEY = ""  # Replace with your OpenCage API key

# Function to generate rainbow-colored text (red, yellow, green)
def rainbow_text(text):
    colors = ['red', 'yellow', 'green']
    rainbow_str = ''
    for i, char in enumerate(text):
        color = colors[i % len(colors)]
        rainbow_str += colored(char, color)
    return rainbow_str

# ASCII Art for PhoneFinder
def display_ascii_art():
    ascii_art = r"""
                                                                                                                              
                                                                                                                                                                      
                                                                                                                                                                      
       ██████▒   ██    ██   ░████░   ███   ██  ████████            ████████   ██████   ███   ██  █████▒    ████████  ██████▒                                          
       ███████▒  ██    ██   ██████   ███   ██  ████████            ████████   ██████   ███   ██  ███████   ████████  ███████▓                                         
       ██   ▒██  ██    ██  ▒██  ██▒  ███▒  ██  ██                  ██           ██     ███▒  ██  ██  ▒██▒  ██        ██   ▒██                                         
       ██    ██  ██    ██  ██▒  ▒██  ████  ██  ██                  ██           ██     ████  ██  ██   ▒██  ██        ██    ██                                         
       ██   ▒██  ██    ██  ██    ██  ██▒█▒ ██  ██                  ██           ██     ██▒█▒ ██  ██   ░██  ██        ██   ▒██                                         
       ███████▒  ████████  ██    ██  ██ ██ ██  ███████             ███████      ██     ██ ██ ██  ██    ██  ███████   ███████▒                                         
       ██████▒   ████████  ██    ██  ██ ██ ██  ███████             ███████      ██     ██ ██ ██  ██    ██  ███████   ██████▓                                          
       ██        ██    ██  ██    ██  ██ ▒█▒██  ██                  ██           ██     ██ ▒█▒██  ██   ░██  ██        ██  ▓██░                                         
       ██        ██    ██  ██▒  ▒██  ██  ████  ██                  ██           ██     ██  ████  ██   ▒██  ██        ██   ██▓                                         
       ██        ██    ██  ▒██  ██▒  ██  ▒███  ██                  ██           ██     ██  ▒███  ██  ▒██▒  ██        ██   ▒██                                         
       ██        ██    ██   ██████   ██   ███  ████████            ██         ██████   ██   ███  ███████   ████████  ██    ██▒                                        
       ██        ██    ██   ░████░   ██   ███  ████████            ██         ██████   ██   ███  █████▒    ████████  ██    ███                                        
                                                                                                                                                                      
    """
    print(rainbow_text(ascii_art))
    print("GitHub: dy-glitch | Instagram: gangnapper\n")

# Function to map Kenyan carriers based on phone number prefix
def get_kenyan_carrier(phone_number):
    prefixes = {
        "70": "Safaricom",
        "71": "Safaricom",
        "72": "Safaricom",
        "74": "Safaricom",
        "75": "Airtel",
        "76": "Airtel",
        "77": "Telkom",
        "78": "Telkom",
        "79": "Telkom",
    }
    prefix = phone_number[4:6]  # Extract the prefix (e.g., "74" from "+254746851226")
    return prefixes.get(prefix, "Unknown Carrier")

def get_phone_location(phone_number):
    """
    Fetch approximate location (city/region) of a phone number using NumVerify API.
    """
    url = f"https://apilayer.net/api/validate?access_key={NUMVERIFY_API_KEY}&number={phone_number}&format=1"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        data = response.json()
        
        if data.get("valid"):
            country = data.get("country_name", "Unknown Country")
            region = data.get("location", "Unknown Region")
            carrier = data.get("carrier", "")
            
            # If the carrier is empty and the country is Kenya, use manual mapping
            if not carrier and country == "Kenya (Republic of)":
                carrier = get_kenyan_carrier(phone_number)
            
            return {
                "country": country,
                "region": region,
                "carrier": carrier
            }
        else:
            print("Invalid phone number or no data found.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def get_lat_lon(location):
    """
    Convert a location (city/region) into latitude and longitude using OpenCage Geocoder API.
    """
    query = f"{location['region']}, {location['country']}"
    encoded_query = quote(query)  # URL encode the query
    url = f"https://api.opencagedata.com/geocode/v1/json?q={encoded_query}&key={OPENCAGE_API_KEY}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        data = response.json()
        
        if data.get("results"):
            lat = data["results"][0]["geometry"]["lat"]
            lon = data["results"][0]["geometry"]["lng"]
            return lat, lon
        else:
            print("No results found for the location.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def get_gps_location():
    """
    Simulate GPS location by fetching coordinates for a given city.
    """
    try:
        geolocator = Nominatim(user_agent="phonefinder")
        location = geolocator.geocode("Nairobi, Kenya")
        if location:
            print("\nSimulated GPS Location:")
            print(f"Latitude: {location.latitude}")
            print(f"Longitude: {location.longitude}")
        else:
            print("Failed to fetch simulated GPS location.")
    except Exception as e:
        print(f"GPS simulation error: {e}")

if __name__ == "__main__":
    # Display ASCII Art
    display_ascii_art()
    
    # Input phone number with country code (e.g., +254746851226)
    phone_number = input("Enter phone number with country code: ")
    
    # Step 1: Get approximate location using NumVerify API
    location = get_phone_location(phone_number)
    
    if location:
        print("\nPhone Number Details:")
        print(f"Country: {location['country']}")
        print(f"Region: {location['region']}")
        print(f"Carrier: {location['carrier']}")
        
        # Step 2: Get latitude and longitude using OpenCage Geocoder API
        lat_lon = get_lat_lon(location)
        
        if lat_lon:
            print("\nApproximate Latitude and Longitude:")
            print(f"Latitude: {lat_lon[0]}")
            print(f"Longitude: {lat_lon[1]}")
    
    # Step 3: Simulate GPS location
    print("\nFetching simulated GPS location...")
    get_gps_location()
