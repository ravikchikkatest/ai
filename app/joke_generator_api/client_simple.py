import requests

# 1. Define the API Endpoint
# LangServe automatically creates an '/invoke' endpoint for single requests
url = "http://localhost:8000/joke-generator/invoke"

# 2. Prepare the input data
# The server expects an "input" dictionary containing your variables
payload = { "input": {"topic": "Python Programmers"}}

print(f"Sending request to {url}...")

# 3. Send the POST request
try:
    response = requests.post(url, json=payload)
    response.raise_for_status() # Check for errors (like 404 or 500)

    # 4. Parse the JSON response
    # LangServe wraps the result in an "output" key
    data = response.json()
    joke = data.get("output")
    
    print("\n--- Joke Received ---")
    print(joke)
    print("---------------------")

except requests.exceptions.ConnectionError:
    print("Error: Could not connect to the server. Is it running?")
except Exception as e:
    print(f"An error occurred: {e}")