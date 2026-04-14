from google import genai

GEMINI_API_KEY = 'AIzaSyCpalvFXIZmc94WIXmQaITKODDF70v04d0'

def test():
    client = genai.Client(api_key=GEMINI_API_KEY)
    print("Testing gemini-flash-latest...")
    response = client.models.generate_content(
        model='gemini-flash-latest',
        contents='Hi'
    )
    print("Response: " + response.text)

if __name__ == "__main__":
    test()
