# https://docs.microsoft.com/nl-nl/azure/storage/queues/storage-python-how-to-use-queue-storage?tabs=python2%2Cenvironment-variable-windows
from flask import Flask, request, jsonify
import requests, random, string, os
from datetime import datetime
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
from azure.identity import AzureCliCredential

from azure.storage.queue import QueueClient

#credential = DefaultAzureCredential()
credential=AzureCliCredential()

app = Flask(__name__)
app.config["DEBUG"] = True


# Next, get the client for the Key Vault.
# Make sure to set the prefix 
# Locally , it should be in a .env file
# In Azure, it should be in the config settings
number_url = os.environ.get("THIRD_PARTY_API_ENDPOINT")
api_secret_name = os.environ.get("THIRD_PARTY_API_SECRET_NAME")
key_vault_url = os.environ.get("KEY_VAULT_URL")
connect_st = os.environ.get("MAIN_APP_STORAGE_CONN_STRING")
queue_name = os.environ.get("STORAGE_QUEUE_NAME")

keyvault_client = SecretClient(vault_url=key_vault_url, credential=credential)
vault_secret = keyvault_client.get_secret(api_secret_name)
access_key = vault_secret.value

queue_client = QueueClient.from_connection_string(conn_str=connect_st,queue_name=queue_name)

@app.route('/', methods=['GET'])
def home():
    return f'Home page of the main app. Make a request to <a href="./api/v1/getcode">/api/v1/getcode</a>.'


def random_char(num):
       return ''.join(random.choice(string.ascii_letters) for x in range(num))


@app.route('/api/v1/getcode', methods=['GET'])
def get_code():
    headers = {
        'Content-Type': 'application/json',
        'x-functions-key': access_key
        }

    r = requests.get(url = number_url, headers = headers)
    
    if (r.status_code != 200):       
        return "Could not get you a code.", r.status_code

    data = r.json()
    code =  str(data['value'])+'_'+str(datetime.utcnow()) 
    
    queue_client.send_message(code)

    return jsonify(code)

if __name__ == '__main__':
    app.run()
