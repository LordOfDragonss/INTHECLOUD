import os, uuid
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

try:
    print("Azure Blob Storage python")
    #put some startup code here
    connect_str= "DefaultEndpointsProtocol=https;EndpointSuffix=core.windows.net;AccountName=pictureblobsumthing2;AccountKey=xUxH7/gsVUMV7J3sVVpQabdC9h5u3m00++sNRSRVQnpWbjvXuLYKVSwQvxA8PFC0mktLun7RLLba+AStNT8kVg==;BlobEndpoint=https://pictureblobsumthing2.blob.core.windows.net/;FileEndpoint=https://pictureblobsumthing2.file.core.windows.net/;QueueEndpoint=https://pictureblobsumthing2.queue.core.windows.net/;TableEndpoint=https://pictureblobsumthing2.table.core.windows.net/"

    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    container_name = str(uuid.uuid4())

    container_client= blob_service_client.create_container(container_name)

    #test file to add to blob
    local_path = "./data"
    os.mkdir(local_path)

    local_file_name = "test" + ".txt"
    upload_file_path = os.path.join(local_path, local_file_name)

    file = open(file=upload_file_path, mode='w')
    file.write("Hello Friend")
    file.close()

    blob_client = blob_service_client.get_blob_client(container=container_name,blob=local_file_name)
    print("uploading file to blob: " + local_file_name)

    with open(file=upload_file_path, mode="rb") as data:
        blob_client.upload_blob(data)
    #check if it's uploaded
    print("Showing blobs")
    blob_list = container_client.list_blobs()
    for blob in blob_list:
        print("\t" + blob.name)

    #download the file to compare files
    input()
    download_file_path = os.path.join(local_path, str.replace(local_file_name, '.txt', 'DOWNLOAD.txt'))
    container_client =  blob_service_client.get_container_client(container= container_name)
    print("DOWNLOADING" + download_file_path)

    with open(file=download_file_path, mode="wb") as download_file:
        download_file.write(container_client.download_blob(blob.name).readall())

    #deletion
    print("deleting please enter a key to start clean-up")
    input()

    print("DELETING CONTAINER...")
    container_client.delete_container()

    print("DELETING FILES")
    os.remove(upload_file_path)
    os.remove(download_file_path)
    os.rmdir(local_path)

    print("DONE")



except Exception as ex:
    print('Exception:')
    print(ex)