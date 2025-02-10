from pydantic import BaseModel


class ImageUploadRequest(BaseModel):
    imageUrl: str
    userEmail: str