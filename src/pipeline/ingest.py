import os
from pathlib import Path
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient

load_dotenv()


def download_blob(local_path: str = "./tmp/source.parquet") -> str:
    connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    container_name = os.getenv("AZURE_CONTAINER_NAME")
    blob_name = os.getenv("AZURE_BLOB_NAME")

    if not all([connection_string, container_name, blob_name]):
        raise ValueError("Missing Azure Blob configuration")

    service_client = BlobServiceClient.from_connection_string(connection_string)
    blob_client = service_client.get_blob_client(container=container_name, blob=blob_name)

    Path(local_path).parent.mkdir(parents=True, exist_ok=True)
    with open(local_path, "wb") as download_file:
        download_file.write(blob_client.download_blob().readall())

    return local_path
