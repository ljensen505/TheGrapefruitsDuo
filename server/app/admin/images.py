# Set your Cloudinary credentials
# ==============================


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
    """
    Custom exception for Cloudinary errors.
    """

    pass


def delete_image(public_id: str) -> None:
    """
    Deletes an image from the Cloudinary cloud.

    :param str public_id: The public ID of the image to delete
    :raises CloudinaryException: If the image deletion fails
    """
    result = uploader.destroy(public_id)

    if result.get("result") != "ok":
        raise CloudinaryException("Failed to delete image")


def get_image_data(public_id: str) -> dict:
    """
    Retrieves the metadata for an image from the Cloudinary cloud.

    :param str public_id: The public ID of the image to retrieve
    :return dict: The metadata for the image
    """
    data = cloudinary.api.resource(public_id)
    return data


def get_image_url(public_id: str) -> str:
    """
    Retrieves the URL for an image from the Cloudinary cloud.

    :param str public_id: The public ID of the image to retrieve
    :raises CloudinaryException: If the image URL retrieval fails
    :return str: The URL of the image
    """
    url = cloudinary.utils.cloudinary_url(public_id)[0]
    if url is None:
        raise CloudinaryException("Failed to get image URL")
    return url
