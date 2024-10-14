import requests
import boto3
import uuid
from botocore.exceptions import NoCredentialsError

class ImageEditError(Exception):
    """Custom exception for image editing errors using Stability AI."""

class S3UploadError(Exception):
    """Custom exception for errors during S3 upload."""

class StabilityImageEditor:
    """
    Class for editing and uploading AI-generated images using Stability AI API and AWS S3.
    
    Parameters:
        - api_key (str): Stability AI API key.
        - aws_access_key (str): AWS access key ID for S3 access.
        - aws_secret_key (str): AWS secret access key for S3.
        - bucket_name (str): Name of the S3 bucket for storing images.
        
    Processing Logic:
        - Bearer token for API authentication is constructed using the api_key.
        - S3 client is instantiated with AWS credentials for image uploads.
        - The base url is hardcoded for Stability AI's image editing (search-and-replace) endpoint.
        - Custom exceptions are raised to handle specific error scenarios.
    """
    def __init__(self, api_key: str, aws_access_key: str, aws_secret_key: str, bucket_name: str):
        """
        Initialize the StabilityImageEditor with API and AWS credentials.

        Args:
            api_key (str): API key for Stability AI.
            aws_access_key (str): AWS access key ID for S3.
            aws_secret_key (str): AWS secret access key for S3.
            bucket_name (str): S3 bucket name where images will be uploaded.
        """
        self.api_key = api_key
        self.base_url = "https://api.stability.ai/v2beta/stable-image/edit/search-and-replace"
        self.headers = {
            "authorization": f"Bearer {self.api_key}",
            "accept": "image/*"
        }
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key
        )
        self.bucket_name = bucket_name

    def search_replace(self, image_path: str, prompt: str, search_prompt: str, output_format: str = "png") -> bytes:
        """
        Perform a search and replace operation on an image using Stability AI API.

        Args:
            image_path (str): The file path of the image to edit.
            prompt (str): The prompt specifying what to replace the search term with.
            search_prompt (str): The term in the image to search for and replace.
            output_format (str): The format of the resulting image. Defaults to "png".

        Returns:
            bytes: The binary content of the edited image.

        Raises:
            ImageEditError: If the image editing process fails.
        """
        files = {
            "image": open(image_path, "rb"),
        }
        data = {
            "prompt": prompt,
            "search_prompt": search_prompt,
            "output_format": output_format
        }

        response = requests.post(
            self.base_url,
            headers=self.headers,
            files=files,
            data=data
        )

        if response.status_code == 200:
            return response.content
        raise ImageEditError(f"Image edit failed: {response.json()}")

    def upload_image_to_s3(self, image_content: bytes, s3_file_path: str) -> str:
        """
        Upload the edited image to an S3 bucket.

        Args:
            image_content (bytes): The binary content of the edited image.
            s3_file_path (str): The file path in the S3 bucket where the image will be stored.

        Returns:
            str: The URL of the uploaded image in S3.

        Raises:
            S3UploadError: If the upload to S3 fails due to credential issues or other errors.
        """
        try:
            self.s3_client.put_object(Bucket=self.bucket_name, Key=s3_file_path, Body=image_content)
            return f"https://{self.bucket_name}.s3.amazonaws.com/{s3_file_path}"
        except NoCredentialsError:
            raise S3UploadError("AWS credentials are not available.")
        except Exception as e:
            raise S3UploadError(f"Failed to upload image to S3: {str(e)}")


def search_replace(api_key: str, aws_access_key: str, aws_secret_key: str, bucket_name: str, image_path: str, prompt: str, search_prompt: str, output_format: str = "png") -> str:
    """
    Perform a search and replace operation on an image, upload the edited image to S3, and return the S3 URL.

    Args:
        api_key (str): API key for Stability AI.
        aws_access_key (str): AWS access key ID for S3.
        aws_secret_key (str): AWS secret access key for S3.
        bucket_name (str): S3 bucket name where images will be uploaded.
        image_path (str): The file path of the image to edit.
        prompt (str): The prompt specifying what to replace the search term with.
        search_prompt (str): The term in the image to search for and replace.
        output_format (str): The format of the resulting image. Defaults to "png".

    Returns:
        str: The URL of the uploaded image in S3.

    Raises:
        ImageEditError: If the image editing process fails.
        S3UploadError: If the upload to S3 fails.
    """
    editor = StabilityImageEditor(api_key, aws_access_key, aws_secret_key, bucket_name)
    edited_image_content = editor.search_replace(image_path, prompt, search_prompt, output_format)

    unique_id = uuid.uuid4()
    s3_file_path = f"edited-images/{unique_id}.{output_format}"

    return editor.upload_image_to_s3(edited_image_content, s3_file_path)
