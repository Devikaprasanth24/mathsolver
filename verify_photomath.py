import os
import requests
import json
from decouple import config

def test_photomath_integration():
    # Load config from .env
    api_key = config('RAPIDAPI_KEY')
    api_host = config('RAPIDAPI_HOST', default='photomath1.p.rapidapi.com')
    api_url = config('PHOTOMATH_API_URL', default='https://photomath1.p.rapidapi.com/maths/solve-problem')

    print(f"Testing Photomath API Integration...")
    print(f"Host: {api_host}")
    print(f"URL: {api_url}")

    # Check for image file to test
    image_path = "math_problem.png" # Assuming this exists or using a placeholder
    if not os.path.exists(image_path):
        print(f"Error: {image_path} not found. Please provide a sample image for testing.")
        return

    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": api_host
    }

    files = {
        'image': (image_path, open(image_path, 'rb'), 'image/jpeg')
    }
    data = {
        'locale': 'en'
    }

    try:
        response = requests.post(api_url, files=files, data=data, headers=headers)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("Successfully received response from Photomath!")
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"Failed to get response. Response: {response.text}")
            
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    test_photomath_integration()
