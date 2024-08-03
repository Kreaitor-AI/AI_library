import requests
import boto3
from botocore.exceptions import NoCredentialsError
import uuid

class StabilityImageGenerator:
    def __init__(self, api_key, aws_access_key, aws_secret_key, bucket_name):
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
    
    def generate_image(self, prompt, aspect_ratio="1:1", model="sd3-large", seed=0, output_format="png", negative_prompt=None):
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
            files={"none": ''},  # Ensures the request is recognized as multipart/form-data
            data=data
        )
        
        if response.status_code == 200:
            return response.content
        else:
            raise Exception(str(response.json()))
    
    def upload_image_to_s3(self, image_content, s3_file_path):
        try:
            self.s3_client.put_object(Bucket=self.bucket_name, Key=s3_file_path, Body=image_content)
            return f"https://{self.bucket_name}.s3.amazonaws.com/{s3_file_path}"
        except NoCredentialsError:
            raise Exception("Credentials not available for AWS S3")

def stability(api_key, aws_access_key, aws_secret_key, bucket_name, prompt, aspect_ratio="1:1", model="sd3-large", seed=0, output_format="png", negative_prompt=None):
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
