import requests
import boto3
import uuid
from botocore.exceptions import NoCredentialsError
from typing import Optional

class StabilityImageGenerationError(Exception):
    """Custom exception for Stability image generation errors."""

class S3UploadError(Exception):
    """Custom exception for errors during S3 upload."""

class StabilityImageGenerator:
    """
    Class for generating and uploading AI-generated images using Stability AI API and AWS S3.
    """

    def __init__(self, api_key: str, aws_access_key: str, aws_secret_key: str, bucket_name: str):
        self.api_key = api_key
        self.base_url = "https://api.stability.ai/v2beta/stable-image/edit/inpaint"
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

    def inpaint(self, image_path: str, mask_path: str, prompt: str, output_format: str = "png") -> bytes:
        """
        Perform inpainting using the Stability AI API.

        Args:
            image_path (str): Path to the image to inpaint.
            mask_path (str): Path to the mask image.
            prompt (str): The prompt to guide the inpainting process.
            output_format (str): The format of the output image. Defaults to "png".

        Returns:
            bytes: The binary content of the inpainted image.

        Raises:
            StabilityImageGenerationError: If the inpainting request fails.
        """
        with open(image_path, "rb") as image_file, open(mask_path, "rb") as mask_file:
            files = {
                "image": image_file,
                "mask": mask_file
            }
            data = {
                "prompt": prompt,
                "output_format": output_format
            }
            response = requests.post(self.base_url, headers=self.headers, files=files, data=data)
        
            if response.status_code == 200:
                return response.content
            raise StabilityImageGenerationError(f"Inpainting failed: {response.json()}")

    def upload_image_to_s3(self, image_content: bytes, s3_file_path: str) -> str:
        """
        Upload the inpainted image to an S3 bucket.

        Args:
            image_content (bytes): The binary content of the image.
            s3_file_path (str): The file path in the S3 bucket where the image will be stored.

        Returns:
            str: The URL of the uploaded image in S3.

        Raises:
            S3UploadError: If the upload to S3 fails.
        """
        try:
            self.s3_client.put_object(Bucket=self.bucket_name, Key=s3_file_path, Body=image_content)
            return f"https://{self.bucket_name}.s3.amazonaws.com/{s3_file_path}"
        except NoCredentialsError:
            raise S3UploadError("AWS credentials are not available.")
        except Exception as e:
            raise S3UploadError(f"Failed to upload image to S3: {str(e)}")


def inpaint(api_key: str, aws_access_key: str, aws_secret_key: str, bucket_name: str, image_path: str, mask_path: str, prompt: str) -> str:
    """
    Inpaint an image using Stability AI and upload the result to an S3 bucket.

    Args:
        api_key (str): API key for Stability AI.
        aws_access_key (str): AWS access key ID for S3.
        aws_secret_key (str): AWS secret access key for S3.
        bucket_name (str): S3 bucket name where images will be uploaded.
        image_path (str): Path to the image to be inpainted.
        mask_path (str): Path to the mask image.
        prompt (str): The prompt to guide the inpainting process.

    Returns:
        str: The URL of the uploaded inpainted image in S3.
    """
    generator = StabilityImageGenerator(api_key, aws_access_key, aws_secret_key, bucket_name)
    image_content = generator.inpaint(image_path=image_path, mask_path=mask_path, prompt=prompt)
    
    unique_id = uuid.uuid4()
    s3_file_path = f"images/{unique_id}.png"
    
    return generator.upload_image_to_s3(image_content, s3_file_path)
