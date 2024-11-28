import http.client
import json

conn = http.client.HTTPSConnection("apex.oracle.com")

payload = json.dumps({
  "product_name": "Product4",
  "codigo_barras": "10000000",
  "peso": 5.5,
  "status": "Available"
})
headers = {
  'Content-Type': 'application/json'
}
conn.request("POST", "/pls/apex/iot_project/api/products/addProduct", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))
