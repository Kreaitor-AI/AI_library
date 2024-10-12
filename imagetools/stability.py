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
    Parameters:
        - api_key (str): Stability AI API key.
        - aws_access_key (str): AWS access key ID for S3 access.
        - aws_secret_key (str): AWS secret access key for S3.
        - bucket_name (str): Name of the S3 bucket for storing images.
    Processing Logic:
        - Bearer token for API authentication is constructed using the api_key.
        - S3 client is instantiated with AWS credentials for later image uploads.
        - The base url is hardcoded and tailored to Stability AI's stable diffusion model v2beta.
        - Custom exceptions are raised to handle specific error scenarios.
    """
    def __init__(self, api_key: str, aws_access_key: str, aws_secret_key: str, bucket_name: str):
        """
        Initialize the StabilityImageGenerator with API and AWS credentials.

        Args:
            api_key (str): API key for Stability AI.
            aws_access_key (str): AWS access key ID for S3.
            aws_secret_key (str): AWS secret access key for S3.
            bucket_name (str): S3 bucket name where images will be uploaded.
        """
        self.api_key = api_key
        self.base_url = "https://api.stability.ai/v2beta/stable-image/generate/sd3"
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
    
    def generate_image(self, prompt: str, aspect_ratio: str = "1:1", model: str = "sd3-large", seed: int = 0, output_format: str = "png", negative_prompt: Optional[str] = None) -> bytes:
        """
        Generate an image using the Stability AI API.

        Args:
            prompt (str): The prompt to generate the image from.
            aspect_ratio (str): The aspect ratio of the generated image. Defaults to "1:1".
            model (str): The model to use for image generation. Defaults to "sd3-large".
            seed (int): The seed value for image generation. Defaults to 0.
            output_format (str): The format of the generated image. Defaults to "png".
            negative_prompt (Optional[str]): A negative prompt to steer away from specific features.

        Returns:
            bytes: The binary content of the generated image.

        Raises:
            StabilityImageGenerationError: If image generation fails or an error response is returned.
        """
        data = {
            "prompt": prompt,
            "aspect_ratio": aspect_ratio,
            "model": model,
            "seed": seed,
            "output_format": output_format
        }
        
        if negative_prompt:
            data['negative_prompt'] = negative_prompt
        
        response = requests.post(
            self.base_url,
            headers=self.headers,
            files={"none": ''}, 
            data=data
        )
        
        if response.status_code == 200:
            return response.content
        raise StabilityImageGenerationError(f"Image generation failed: {response.json()}")

    def upload_image_to_s3(self, image_content: bytes, s3_file_path: str) -> str:
        """
        Upload the generated image to an S3 bucket.

        Args:
            image_content (bytes): The binary content of the image.
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

def stability(api_key: str, aws_access_key: str, aws_secret_key: str, bucket_name: str, prompt: str, aspect_ratio: str = "1:1", model: str = "sd3-large", seed: int = 0, output_format: str = "png", negative_prompt: Optional[str] = None) -> str:
    """
    Generate an image using Stability AI and upload it to an S3 bucket.

    Args:
        api_key (str): API key for Stability AI.
        aws_access_key (str): AWS access key ID for S3.
        aws_secret_key (str): AWS secret access key for S3.
        bucket_name (str): S3 bucket name where images will be uploaded.
        prompt (str): The prompt to generate the image from.
        aspect_ratio (str): The aspect ratio of the generated image. Defaults to "1:1".
        model (str): The model to use for image generation. Defaults to "sd3-large".
        seed (int): The seed value for image generation. Defaults to 0.
        output_format (str): The format of the generated image. Defaults to "png".
        negative_prompt (Optional[str]): A negative prompt to steer away from specific features.

    Returns:
        str: The URL of the uploaded image in S3.

    Raises:
        StabilityImageGenerationError: If image generation fails.
        S3UploadError: If the upload to S3 fails.
    """
    generator = StabilityImageGenerator(api_key, aws_access_key, aws_secret_key, bucket_name)
    image_content = generator.generate_image(
        prompt=prompt,
        aspect_ratio=aspect_ratio,
        model=model,
        seed=seed,
        output_format=output_format,
        negative_prompt=negative_prompt
    )

    unique_id = uuid.uuid4()
    s3_file_path = f"images/{unique_id}.{output_format}"
    
    return generator.upload_image_to_s3(image_content, s3_file_path)
