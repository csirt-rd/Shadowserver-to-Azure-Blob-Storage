#!/usr/bin/env python3
from datetime import datetime, timedelta
import os
import threading
from azure.storage.blob import BlobClient
from azure.core.exceptions import ResourceExistsError

# Azure Storage Blob Info
AZURE_ACC_KEY = ""
AZURE_ENDPOINT_SUFFIX = "core.windows.net"
AZURE_ACC_NAME = ""
AZURE_ENDPOINT = "{}.table.{}".format(AZURE_ACC_NAME, AZURE_ENDPOINT_SUFFIX)
AZURE_CONN_STR = "DefaultEndpointsProtocol=https;AccountName={};AccountKey={};EndpointSuffix={}".format(
    AZURE_ACC_NAME, AZURE_ACC_KEY, AZURE_ENDPOINT_SUFFIX
)

def disk_to_blob(folder, date):
    FILE = '-'.join([date.strftime("%Y-%m-%d"), folder]) + '.csv'
    BLOB = os.path.join(folder, FILE)
    SHADOW_FILE = os.path.join(MY_PATH, folder, FILE)
    with BlobClient.from_connection_string(conn_str=AZURE_CONN_STR, container_name="shadowserver", blob_name=BLOB) as blob:
        try:
            with open(SHADOW_FILE, 'rb') as data:
                try:
                    blob.upload_blob(data)
                except ResourceExistsError:
                    pass
        except FileNotFoundError:
            pass

if __name__ == "__main__":
    yesterday = datetime.now() - timedelta(1)
    MY_PATH = os.path.join(os.getcwd(),'shadowserver')
    threads = list()
    for d in os.listdir(MY_PATH):
        x = threading.Thread(target=disk_to_blob, args=(d, yesterday), daemon=True)
        threads.append(x)
        x.start()
    for index, thread in enumerate(threads):
        thread.join()
