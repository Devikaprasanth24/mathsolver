
import os
import django
from django.conf import settings

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'math_solve.settings')
django.setup()

from math_api.classifier import detect_topic, detect_difficulty
from math_api.utils import clean_math_text
from math_api.verify import verify_answer

def test_components():
    print("Testing Math API Components...")
    
    # 1. Test Cleaning
    raw = "2x + 5 = 15 ?"
    cleaned = clean_math_text(raw)
    print(f"Cleaning '{raw}' -> '{cleaned}'")
    assert cleaned.replace(" ", "") == "2x+5=15"
    
    # 2. Test Classification
    topic = detect_topic("sin(x)")
    diff = detect_difficulty("sin(x)")
    print(f"Prop: sin(x) -> Topic: {topic}, Diff: {diff}")
    assert topic == "Trigonometry"
    assert diff == "Medium"
    
    topic = detect_topic("2x+5=10")
    diff = detect_difficulty("2x+5=10")
    print(f"Prop: 2x+5=10 -> Topic: {topic}, Diff: {diff}")
    assert topic == "Algebra - Equation"
    assert diff == "Easy"
    
    # 3. Test Verification (SymPy)
    # Simple linear
    ans = verify_answer("2*x - 10 = 0")
    print(f"Verify '2*x - 10 = 0' -> {ans}")
    assert ans == "[5]"
    
    # Simple arithmetic
    ans = verify_answer("2+2")
    print(f"Verify '2+2' -> {ans}")
    assert ans == "4"
    
    print("\nAll component tests passed!")

if __name__ == "__main__":
    test_components()
