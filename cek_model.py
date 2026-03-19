import requests

API_KEY = "AIzaSyCQ7u9aRscVl44sLJnokW-sc7ti71EYxdA"
URL = f"https://generativelanguage.googleapis.com/v1beta/models?key={API_KEY}"

response = requests.get(URL)
if response.status_code == 200:
    models = response.json()
    print("--- MODEL YANG TERSEDIA DI AKUN LO ---")
    for m in models['models']:
        print(f"Nama: {m['name']} | Support: {m['supportedGenerationMethods']}")
else:
    print(f"Error: {response.status_code} - {response.text}")