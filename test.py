import requests
import json

def print_response(response):
    print(f"Status: {response.status_code}")
    print("Response:", json.dumps(response.json(), indent=2))

"""print("Ajout d'un smartphone au panier :")
response = requests.post(
    "http://127.0.0.1:5000/cart",
    json={"id": "je8zng", "quantity": 2}
)
print_response(response)

print("\nContenu du panier après ajout :")
response = requests.get("http://127.0.0.1:5000/cart")
print_response(response)"""


print("Contenu du panier :")
response = requests.get("http://127.0.0.1:5000/cart")
print_response(response)