#!/usr/bin/env python3
import threading, requests, re
from datetime import datetime, timedelta
from azure.storage.blob import BlobClient
from azure.core.exceptions import ResourceExistsError

#Shadowserver Info
MATCH = '(https:\/\/dl.shadowserver.org\/[^"]+)'
SS_URL = "https://dl.shadowserver.org/reports/index.php"

# Azure Storage Blob Info
AZURE_ACC_KEY = "..."
AZURE_ENDPOINT_SUFFIX = "core.windows.net"
AZURE_ACC_NAME = "..."
AZURE_ENDPOINT = "{}.table.{}".format(AZURE_ACC_NAME, AZURE_ENDPOINT_SUFFIX)
AZURE_CONN_STR = "DefaultEndpointsProtocol=https;AccountName={};AccountKey={};EndpointSuffix={}".format(
    AZURE_ACC_NAME, AZURE_ACC_KEY, AZURE_ENDPOINT_SUFFIX
)

def ss_to_blob(session, url, date):
    RESPONSE = session.get(url)
    if RESPONSE.status_code == 200:
        try:
            FILENAME = re.findall(f"filename={date}-(.+)", RESPONSE.headers['content-disposition'])[0][:-4]
        except:
            pass
        else:
            BLOB = '/'.join([FILENAME, '-'.join([date, FILENAME]) + '.csv'])
            with BlobClient.from_connection_string(conn_str=AZURE_CONN_STR, container_name="...", blob_name=BLOB) as blob:
                try:
                    blob.upload_blob(RESPONSE.content)
                except ResourceExistsError:
                    pass

if __name__ == "__main__":
    SESSION = requests.Session()
    RESPONSE = SESSION.post(
        SS_URL,
        data={
        'user': "...",
        'password': "...",
        'login':'Login'
        }
    )
    HTML_CONTENT = RESPONSE.content.decode('utf-8')
    yesterday = datetime.now() - timedelta(1)
    threads = list()
    URLS = [download_me.group(1) for download_me in re.finditer(MATCH, HTML_CONTENT, re.MULTILINE)][4400:]
    for URL in URLS:
        x = threading.Thread(target=ss_to_blob, args=(SESSION, URL, yesterday.strftime("%Y-%m-%d")), daemon=True)
        threads.append(x)
        x.start()
    for index, thread in enumerate(threads):
        thread.join()
