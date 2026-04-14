import os
import django
import json
from django.test import RequestFactory
from chatbot.views import chatbot_response

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'math_solve.settings')
django.setup()

def verify_view():
    factory = RequestFactory()
    data = {'message': 'Hi SolBot, how are you?'}
    request = factory.post('/chatbot/ask/', data=json.dumps(data), content_type='application/json')
    
    response = chatbot_response(request)
    print(f"Status Code: {response.status_code}")
    print(f"Content: {response.content.decode()}")

if __name__ == "__main__":
    verify_view()
