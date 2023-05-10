import requests

response = requests.get("https://api.stripe.com/v1/invoices",
headers ={'Authorization: Bearer pk_test_51MqFlcAoQeT5gshm7zkRPtXwPvRiZbMxpDfsgfo07XFDRJZKOIFoBqpZ2N9JA6FLxVe9vrcDoZh07eteYjdgMTsW00w9bhen42'})

data = response.json()

print(data)