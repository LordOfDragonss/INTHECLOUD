import requests

response = requests.get("https://api.spotify.com/v1/playlists/6txGSI1X7kxbW0vevaFP31/tracks",
                        headers={'Authorization': 'Bearer BQC_sHciFzzmbLR1ImHPMfjIfZQ35ZxgecDVuhmAr158TnJ--QJECT5v2lN92sEfvbncvmACoucKq73DgnMjNYwnoDphwMSpyXnN32uVOXhnj4o_ddvrk_443YICfxG0EdFnTSHu3qL3LgvOIEWhKWpn6mjSGM2KvZaKMmXWfiqCoWOrJJRgKeRUfPo-xA'})

data = response.json()

print(data)

array = []
for item in data['items']:
    array.append({
        "id":item['track']['id'],
        "name":item['track']['name'],
        "artist":item['track']['artists'][0]['name'],
        "href":item['track']['external_urls']['spotify']
    })

from pymongo_get_database import get_database
dbname = get_database()
collection_name = dbname["Spotify_Songs"]

collection_name.insert_many(array)


