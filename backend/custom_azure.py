from storages.backends.azure_storage import AzureStorage

import os
from dotenv import load_dotenv
load_dotenv()

class AzureMediaStorage(AzureStorage):
    account_name = 'beproject' # <storage_account_name>
    account_key = str(os.getenv('ACCOUNT_KEY')) # <storage_account_key>
    azure_container = 'media'
    expiration_secs = None

class AzureStaticStorage(AzureStorage):
    account_name = 'beproject' # <storage_account_name>
    account_key = str(os.getenv('ACCOUNT_KEY')) # <storage_account_key>
    azure_container = 'static'
    expiration_secs = None