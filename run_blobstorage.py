import os
from datetime import datetime
import logging
import warnings
from isodate import tz_isoformat
import urllib3
from dotenv import load_dotenv

from azure.storage.blob import BlobServiceClient, BlobClient
# from az_helper import ContainerBlobStorage

# Config Logger format
FORMAT = '%(asctime)-15s - %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger("main.py")
logger.setLevel("INFO")
warnings.filterwarnings(action='once')
urllib3.disable_warnings()

env_path = os.path.join('setup', '.env')
load_dotenv(env_path)

# Load variables
environment = os.environ['ENVIRONMENT']
connect_str = os.environ['AZ_STORAGE_CONNECTION_STRING']

# Create a file in the local data directory to upload and download
local_path = "data/logs/"
local_file_name = f"datadump-log-{environment}.txt"
complete_path = local_path + local_file_name

def write_text(complete_path):
    '''
    Create temporary log file
    '''
    # Write text to the file
    with open(complete_path, 'w', encoding='utf-8') as f:
        f.write("Sherlock Data Pipeline succedeed!\n")
        f.write(f"Recorded at {datetime.utcnow()}")

def create_blob_file(complete_path):
    '''
    create blob file
    '''
    # Create the BlobServiceClient object which will be used to create a container client
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)

    # Create a unique name for the container
    container_name = "az-devops-logs"

    # Create a blob client using the local file name as the name for the blob
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=local_file_name)

    logger.info("\nUploading to Azure Storage as blob:\n\t" + local_file_name)

    # Create temporary file on local
    write_text(complete_path)

    # Upload the created file Blob Storagecl
    with open(complete_path, "rb") as data:
        blob_client.upload_blob(data, overwrite=True)


# Call Main function
if __name__ == '__main__':
    create_blob_file(complete_path)