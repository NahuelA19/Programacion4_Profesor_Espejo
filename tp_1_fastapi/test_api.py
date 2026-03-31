import json
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi.testclient import TestClient
from app.main import create_app

app = create_app()
client = TestClient(app)

print("--- TEST 1: POST /clientes/ (Crear correctos) ---")
res1 = client.post("/clientes/", json={
    "nombre": "Nahuel Gonzalez",
    "email": "nahuel@ejemplo.com",
    "telefono": "12345678",
    "activo": True,
    "tipo": "Premium"
})
print("Status:", res1.status_code)
print("Response:", json.dumps(res1.json(), indent=2))
print()

print("--- TEST 2: POST /clientes/ (Duplicado - Error 400) ---")
res2 = client.post("/clientes/", json={
    "nombre": "Nahuel Gonzalez 2",
    "email": "nahuel@ejemplo.com",
    "tipo": "Regular"
})
print("Status:", res2.status_code)
print("Response:", json.dumps(res2.json(), indent=2))
print()

print("--- TEST 3: POST /clientes/ (Email Inválido - Error 422) ---")
res3 = client.post("/clientes/", json={
    "nombre": "Nahuel 3",
    "email": "correo-invalido",
    "tipo": "VIP"
})
print("Status:", res3.status_code)
print("Response:", json.dumps(res3.json(), indent=2))
print()

print("--- TEST 4: GET /clientes/ con query params ---")
res4 = client.get("/clientes/?tipo=Premium")
print("Status:", res4.status_code)
print("Response:", json.dumps(res4.json(), indent=2))
print()

print("--- TEST 5: GET /clientes/999 (No encontrado - Error 404) ---")
res5 = client.get("/clientes/999")
print("Status:", res5.status_code)
print("Response:", json.dumps(res5.json(), indent=2))
print()

print("--- TEST 6: GET /clientes/1/clasificacion ---")
res6 = client.get("/clientes/1/clasificacion")
print("Status:", res6.status_code)
print("Response:", json.dumps(res6.json(), indent=2))
print()
