import requests

requests.post("http://127.0.0.1:5000/cart", json={
    'id': "je8zng",
    'quantity': 1
})
requests.post("http://127.0.0.1:5000/cart", json={
    'id': "je8zng",
    'quantity': 2
})

req = requests.patch("http://127.0.0.1:5000/cart", json={
    'id': "je8zng",
    'quantity': 10
})

print(requests.get("http://127.0.0.1:5000/cart").json())

req = requests.delete("http://127.0.0.1:5000/cart", json={
    'id': "je8zng"
})

print(req.status_code, req.json())
print(requests.get("http://127.0.0.1:5000/cart").json())