#!/usr/bin/env python3
from datetime import datetime, timedelta
import os
from azure.storage.blob import BlobClient
from azure.core.exceptions import ResourceExistsError

# Azure Data 
AZURE_ACC_KEY = ""
AZURE_ENDPOINT_SUFFIX = "core.windows.net"
AZURE_ACC_NAME = ""
AZURE_ENDPOINT = "{}.table.{}".format(AZURE_ACC_NAME, AZURE_ENDPOINT_SUFFIX)
AZURE_CONN_STR = "DefaultEndpointsProtocol=https;AccountName={};AccountKey={};EndpointSuffix={}".format(
    AZURE_ACC_NAME, AZURE_ACC_KEY, AZURE_ENDPOINT_SUFFIX
)
LOG_FILE = '-'.join([
    '/'.join([os.getcwd(), 'logs', 'log']),
    datetime.now().strftime("%Y%m%d")
]) + '.txt'

def disk_to_blob():
    MY_PATH = '/'.join([
        os.getcwd(),
        'shadowserver'
    ])
    try:   
        os.makedirs('/'.join([os.getcwd(), 'logs']))
    except FileExistsError:
        pass
    for d in os.listdir(MY_PATH):
        FILE = '-'.join([yesterday.strftime("%Y-%m-%d"), d]) + '.csv'
        BLOB = os.path.join(d, FILE)
        SHADOW_FILE = os.path.join(MY_PATH, d, FILE)
        with open(LOG_FILE, 'a', encoding='utf-8') as l:
            l.write(
                ' '.join([
                    datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S:%f")[:-3],
                    '+00:00',
                    '[INF]',
                    'Uploading',
                    FILE,
                    'to Sucuri Blob Storage'
                    '\n'
                ])
            )
        l.close()
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
    disk_to_blob()
