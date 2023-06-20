import os
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import azure.functions as func

app = func.FunctionApp()

@app.function_name(name="SendImages")
@app.route("images", methods=["POST"])
def post_image(req: func.HttpRequest) -> func.HttpResponse:
    image = req.get_json
    url = image["url"]
    name = image=["name"]
    status = image["status"]
    UploadToBlobUrl(url,name,status)
    


def UploadToBlobUrl(url,file_name,status):
    try:
        connect_str = ""
        if status == "done":
            connect_str= "DefaultEndpointsProtocol=https;EndpointSuffix=core.windows.net;AccountName=pictureblobsumthing2;AccountKey=xUxH7/gsVUMV7J3sVVpQabdC9h5u3m00++sNRSRVQnpWbjvXuLYKVSwQvxA8PFC0mktLun7RLLba+AStNT8kVg==;BlobEndpoint=https://pictureblobsumthing2.blob.core.windows.net/;FileEndpoint=https://pictureblobsumthing2.file.core.windows.net/;QueueEndpoint=https://pictureblobsumthing2.queue.core.windows.net/;TableEndpoint=https://pictureblobsumthing2.table.core.windows.net/"
        elif status == "tentative":
            connect_str= "DefaultEndpointsProtocol=https;EndpointSuffix=core.windows.net;AccountName=pictureblobsumthing2;AccountKey=xUxH7/gsVUMV7J3sVVpQabdC9h5u3m00++sNRSRVQnpWbjvXuLYKVSwQvxA8PFC0mktLun7RLLba+AStNT8kVg==;BlobEndpoint=https://pictureblobsumthing2.blob.core.windows.net/;FileEndpoint=https://pictureblobsumthing2.file.core.windows.net/;QueueEndpoint=https://pictureblobsumthing2.queue.core.windows.net/;TableEndpoint=https://pictureblobsumthing2.table.core.windows.net/"
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)

        blob_client = blob_service_client.get_blob_client(container="images",blob=file_name)
        blob_client.upload_blob_from_url(url)

    except Exception as ex:
        print("Exception")
        print(ex)



def CreateContainer(name):
    try:
        print("executing code")
        connect_str= "DefaultEndpointsProtocol=https;EndpointSuffix=core.windows.net;AccountName=pictureblobsumthing2;AccountKey=xUxH7/gsVUMV7J3sVVpQabdC9h5u3m00++sNRSRVQnpWbjvXuLYKVSwQvxA8PFC0mktLun7RLLba+AStNT8kVg==;BlobEndpoint=https://pictureblobsumthing2.blob.core.windows.net/;FileEndpoint=https://pictureblobsumthing2.file.core.windows.net/;QueueEndpoint=https://pictureblobsumthing2.queue.core.windows.net/;TableEndpoint=https://pictureblobsumthing2.table.core.windows.net/"

        blob_service_client = BlobServiceClient.from_connection_string(connect_str)
        container_name = name
        
        container_client= blob_service_client.create_container(container_name)

    except Exception as ex:
        print("Exception")
        print(ex)

def uploadToBlob(file_path, file_name):
    try:
        connect_str= "DefaultEndpointsProtocol=https;EndpointSuffix=core.windows.net;AccountName=pictureblobsumthing2;AccountKey=xUxH7/gsVUMV7J3sVVpQabdC9h5u3m00++sNRSRVQnpWbjvXuLYKVSwQvxA8PFC0mktLun7RLLba+AStNT8kVg==;BlobEndpoint=https://pictureblobsumthing2.blob.core.windows.net/;FileEndpoint=https://pictureblobsumthing2.file.core.windows.net/;QueueEndpoint=https://pictureblobsumthing2.queue.core.windows.net/;TableEndpoint=https://pictureblobsumthing2.table.core.windows.net/"
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)

        blob_client = blob_service_client.get_blob_client(container="images",blob=file_name)
        blob_client.upload_blob()

        with open(file_path, "rb") as data:
            blob_client.upload_blob(data)
            print("UPLOADED" + file_name)
    
    except Exception as ex:
        print(ex)

def DownloadImgFromBlob(file_name):
    print("Downloading image")
    connect_str= "DefaultEndpointsProtocol=https;EndpointSuffix=core.windows.net;AccountName=pictureblobsumthing2;AccountKey=xUxH7/gsVUMV7J3sVVpQabdC9h5u3m00++sNRSRVQnpWbjvXuLYKVSwQvxA8PFC0mktLun7RLLba+AStNT8kVg==;BlobEndpoint=https://pictureblobsumthing2.blob.core.windows.net/;FileEndpoint=https://pictureblobsumthing2.file.core.windows.net/;QueueEndpoint=https://pictureblobsumthing2.queue.core.windows.net/;TableEndpoint=https://pictureblobsumthing2.table.core.windows.net/"
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    container_client = blob_service_client.get_container_client(container="images")
    local_path = "./Images/" + file_name
    with open(file=local_path, mode="wb") as download_file:
        download_file.write(container_client.download_blob(blob=file_name).readall())