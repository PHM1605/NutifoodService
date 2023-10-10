from core.settings import Settings
from azure.storage.blob import BlobServiceClient
from azure.storage.blob import ContentSettings
import datetime
import os
from urllib.parse import urlparse


settings = Settings()
connection_string = settings.AZURE_STORAGE_CONNECTION_STRING
print("connection_string: ", connection_string)
blob_service_client = BlobServiceClient.from_connection_string(
    conn_str=connection_string)


connection_string_2 = settings.AZURE_STORAGE_CONNECTION_STRING_2
blob_service_client_2 = BlobServiceClient.from_connection_string(
    conn_str=connection_string_2)

def upload_blob_logging(local_file_name):
    domain_container_name = "spvb-logging"
    now = datetime.datetime.now()
    print("local_file_name: ", local_file_name)
    
    blob_file_name = os.path.basename(local_file_name)
    blob_file_name = os.path.join(f'{now.year}/{now.month}/{now.day}', blob_file_name)
    print("blob_file_name: ", blob_file_name)
    blob_client = blob_service_client.get_blob_client(container=domain_container_name, blob=blob_file_name)
    with open(local_file_name, "rb") as data:
        print('data: ', data)
        # data = data.encode('utf-8')
        blob_client.upload_blob(data, overwrite=True)
    url_file = blob_client.url
    print('url_file: ', url_file)
    return url_file

def download_blob(url, destination_file):
    parsed_url = urlparse(url)
    path_parts = parsed_url.path.strip("/").split("/")
    container_name = path_parts[0]
    domain_container_name = container_name
    print('domain_container_name: ',domain_container_name)
    container_client = blob_service_client.get_container_client(domain_container_name)
    file_name = url.split(f'/{domain_container_name}/')[-1]
    blob_client = container_client.get_blob_client(file_name)
    exists = blob_client.exists()
    print(f"exists: {exists}")
    if exists:
        with open(destination_file, "wb") as my_blob:
            blob_data = blob_client.download_blob()
            blob_data.readinto(my_blob)
        return destination_file
    return 404


def download_blob_2(url, destination_file):
    parsed_url = urlparse(url)
    path_parts = parsed_url.path.strip("/").split("/")
    container_name = path_parts[0]
    domain_container_name = container_name
    print('domain_container_name: ',domain_container_name)
    container_client = blob_service_client_2.get_container_client(domain_container_name)
    file_name = url.split(f'/{domain_container_name}/')[-1]
    blob_client = container_client.get_blob_client(file_name)
    exists = blob_client.exists()
    print(f"exists: {exists}")
    if exists:
        with open(destination_file, "wb") as my_blob:
            blob_data = blob_client.download_blob()
            blob_data.readinto(my_blob)
        return destination_file
    return 404

def download_model(w, destination_file):
    file_name = w.split('/')[-1]
    print('file_name: ', file_name)
    container_name = 'spvb'
    container_client = blob_service_client.get_container_client(container_name)
    blob_client = container_client.get_blob_client(file_name)
    exists = blob_client.exists()
    print(f"exists: {exists}")
    if exists:
        with open(destination_file, "wb") as my_blob:
            blob_data = blob_client.download_blob()
            blob_data.readinto(my_blob)
        return w
    return 404

def download(name: str):
    container_name = 'spvb'
    container_client = blob_service_client.get_container_client(container_name)
    blob_client = container_client.get_blob_client(name)
    return blob_client.download_blob()


def upload(name: str, data):
    container_name = 'spvb'
    container_client = blob_service_client.get_container_client(container_name)
    blob_client = container_client.upload_blob(name, data)
    return blob_client

def upload_blob(local_file_name: str):
    domain_container_name = f"spvb"
    now = datetime.datetime.now()
    print("local_file_name: ", local_file_name)
    
    blob_file_name = os.path.basename(local_file_name)
    blob_file_name = os.path.join(f'{now.year}/{now.month}/{now.day}', blob_file_name)
    print("blob_file_name: ", blob_file_name)
    blob_client = blob_service_client.get_blob_client(container=domain_container_name, blob=blob_file_name)
    with open(local_file_name, "rb") as data:
        print('data: ', data)
        # data = data.encode('utf-8')
        blob_client.upload_blob(data, overwrite=True, content_settings=ContentSettings(content_type='image/jpeg'))
    url_file = blob_client.url
    print('url_file: ', url_file)
    return url_file

# upload file to azure blob with content type image/jpeg
def upload_blob_with_content_type(local_file_name: str):
    domain_container_name = f"spvb"
    now = datetime.datetime.now()
    print("local_file_name: ", local_file_name)
    
    blob_file_name = os.path.basename(local_file_name)
    blob_file_name = os.path.join(f'{now.year}/{now.month}/{now.day}', blob_file_name)
    print("blob_file_name: ", blob_file_name)
    blob_client = blob_service_client.get_blob_client(container=domain_container_name, blob=blob_file_name)
    with open(local_file_name, "rb") as data:
        print('data: ', data)
        # data = data.encode('utf-8')
        blob_client.upload_blob(data, overwrite=True, content_settings=ContentSettings(content_type='image/jpeg'))
    url_file = blob_client.url
    print('url_file: ', url_file)
    return url_file