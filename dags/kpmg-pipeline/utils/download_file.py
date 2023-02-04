from azure.storage.blob import BlobServiceClient
import os

def download_file(local_file_desired_path: str, blob_name: str) -> str:
    """
    Download a blob (file) from an Azure Storage container and save it to a local file.

    :param local_file_desired_path: The path to the local file to save the blob to.
    :param blob_name: The name of the blob (file) to download.
    :return: The path to the local file.
    """

    # Load environment variables
    connection_string = os.getenv("AZURE_CONNECTION_STRING")
    container_name = os.getenv("STORAGE_CONTAINER")

    # Raise an error if the environment variables are not found
    if not connection_string or not container_name:
        raise ValueError("Missing environment variables... Please check your .env file")

    # Initialize the connection to Azure
    blob_service_client =  BlobServiceClient.from_connection_string(connection_string)
    
    # Create blob (file) with same name as local file name
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    
    print(f"Downloading file: {blob_name}...")
    
    blob_data = blob_client.download_blob().read()

    # print("File's data: ", blob_data)

    print("Writing data to local file...")
    # Write data to local file 
    # (Not mandatory if you just want to read the data!)
    with open(local_file_desired_path, "wb") as file:
        file.write(blob_data)
    
    print("File downloaded!")
    
    return local_file_desired_path