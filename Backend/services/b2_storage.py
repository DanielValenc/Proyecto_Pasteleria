from b2sdk.v2 import InMemoryAccountInfo, B2Api
from Backend.config import B2_KEY_ID, B2_APPLICATION_KEY ,BUCKET_NAME


info = InMemoryAccountInfo()
b2_api = B2Api(info)
b2_api.authorize_account("production", B2_KEY_ID, B2_APPLICATION_KEY)
bucket = b2_api.get_bucket_by_name(BUCKET_NAME)

def upload_to_b2(file_data: bytes, file_name: str):
    bucket.upload_bytes(file_data, file_name)
    return f"https://f005.backblazeb2.com/file/{BUCKET_NAME}/{file_name}"
