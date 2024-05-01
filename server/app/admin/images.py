# Set your Cloudinary credentials
# ==============================

from pprint import pprint

from dotenv import load_dotenv

load_dotenv()


# Import the Cloudinary libraries
# ==============================
import cloudinary
import cloudinary.api
import cloudinary.uploader

# Set configuration parameter: return "https" URLs by setting secure=True
# ==============================
cloudinary.config(secure=True)

uploader = cloudinary.uploader


class CloudinaryException(Exception):
    pass


def delete_image(public_id: str) -> None:
    result = uploader.destroy(public_id)

    if result.get("result") != "ok":
        raise CloudinaryException("Failed to delete image")


def get_image_data(public_id: str) -> dict:
    data = cloudinary.api.resource(public_id)
    return data


def get_image_url(public_id: str) -> str:
    url = cloudinary.utils.cloudinary_url(public_id)[0]
    if url is None:
        raise CloudinaryException("Failed to get image URL")
    return url


if __name__ == "__main__":
    image_id = "coco_copy_jywbxm"
