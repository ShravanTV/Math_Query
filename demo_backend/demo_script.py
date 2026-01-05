"""
Demo Script for Math Query Assistant Testing

This script provides comprehensive automated testing for the Math Query Assistant system.
It validates the three core behavioral rules of the custom LLM model and generates
detailed reports of system performance in CSV format.

Test Categories:
1. Mathematical Queries: Tests mathematical reasoning and calculation accuracy
2. Ping-Pong Protocol: Validates case-insensitive ping detection and exact response
3. Rejection Rule: Ensures non-math, non-ping inputs are properly rejected

Output:
- Console display of test results in real-time
- CSV report with detailed test data for analysis
- Error handling and logging for debugging
"""

import requests
import csv
import os
 
BACKEND_URL = os.getenv('BACKEND_URL', 'http://backend:8000/query').rstrip('/')

# Comprehensive test cases covering all behavioral rules and edge cases
test_cases = [
    # Mathematical Queries - Basic Operations
    ("Simple division", "What is 10 divided by 2?", "Should answer: 5 or equivalent math answer"),
    ("Square root", "Calculate the square root of 81", "Should answer: 9 or equivalent math answer"),
    ("Basic addition", "What is 15 + 27?", "Should answer: 42 or equivalent math answer"),
    ("Exponent", "What is 2 to the power of 5?", "Should answer: 32 or equivalent math answer"),
    ("Decimal operations", "What is 3.5 * 2?", "Should answer: 7 or equivalent math answer"),
    ("Word problem math", "If I have 5 apples and buy 3 more, how many do I have?", "Should answer: 8 or equivalent math answer"),
    
    # Ping-Pong Protocol - Case Variations
    ("Ping lower", "ping", "Should answer: pong!!!"),
    ("Ping upper", "PING", "Should answer: pong!!! (case-insensitive)"),
    ("Ping mixed", "PiNg", "Should answer: pong!!! (case-insensitive)"),
    ("Ping title case", "Ping", "Should answer: pong!!! (case-insensitive)"),
    
    # Rejection Rule 
    ("Non-math: geography", "What is the capital of France?", "Should refuse: only math or ping allowed"),
    ("Non-math: history", "Who was the first president of the United States?", "Should refuse: only math or ping allowed"),
    ("Non-math: science", "What is the chemical formula for water?", "Should refuse: only math or ping allowed"),
     ("Non-math: weather", "What's the weather like today?", "Should refuse: only math or ping allowed"),
    ("Non-math: personal", "What is your name?", "Should refuse: only math or ping allowed"),
    
    # Rejection Rule - Edge Cases
    ("Non-math: numbers in context", "What is your phone number?", "Should refuse: only math or ping allowed"),
    ("Non-math: measurement", "How tall is the Eiffel Tower?", "Should refuse: only math or ping allowed"),
    ("Non-math: time", "What time is it now?", "Should refuse: only math or ping allowed"),
    ("Non-math: date", "What is today's date?", "Should refuse: only math or ping allowed"),
    
    # Edge Cases - Math Questions
    ("Math: zero", "What is 0 * 5?", "Should answer: 0 or equivalent math answer"),
    ("Math: negative", "What is -5 + 3?", "Should answer: -2 or equivalent math answer"),
    ("Math: implied calculation", "If I double 10, what do I get?", "Should answer: 20 or equivalent math answer"),
    
    # Edge Cases - Empty/Invalid Input
    ("Empty input", "", "Should refuse: only math or ping allowed"),
    ("Only spaces", "   ", "Should refuse: only math or ping allowed"),
    ("Only punctuation", "???", "Should refuse: only math or ping allowed"),
]

csv_rows = []

for desc, question, expected in test_cases:
    try:
        resp = requests.post(BACKEND_URL, json={"question": question}, timeout=150)
        if resp.ok:
            answer = resp.json().get("response", "<no response>")
        else:
            answer = f"<error {resp.status_code}> {resp.text}"
    except Exception as e:
        answer = f"<exception> {e}"
    print(f"{desc}: {question}\n  => {answer}\n")
    csv_rows.append([desc, question, expected, answer])

# Write results to CSV
with open("demo_results.csv", "w", newline='', encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Description", "Question", "Expected Behaviour", "Current Response"])
    writer.writerows(csv_rows)

print("\nResults written to demo_results.csv")
