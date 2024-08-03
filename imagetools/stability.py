import requests
import boto3
from botocore.exceptions import NoCredentialsError

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
    
    def generate_image(self, prompt, aspect_ratio="1:1", model="sd3-medium", seed=0, output_format="jpeg", negative_prompt=None):
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
        else:
            raise Exception(str(response.json()))
    
    def upload_image_to_s3(self, image_content, s3_file_path):
        try:
            self.s3_client.put_object(Bucket=self.bucket_name, Key=s3_file_path, Body=image_content)
            print(f"Image successfully uploaded to S3 at {s3_file_path}")
            return f"https://{self.bucket_name}.s3.amazonaws.com/{s3_file_path}"
        except NoCredentialsError:
            raise Exception("Credentials not available for AWS S3")

def stability(api_key, aws_access_key, aws_secret_key, bucket_name, prompt, aspect_ratio="1:1", model="sd3-medium", seed=0, output_format="jpeg", negative_prompt=None, s3_file_path="output_image.jpeg"):
    generator = StabilityImageGenerator(api_key, aws_access_key, aws_secret_key, bucket_name)
    image_content = generator.generate_image(
        prompt=prompt,
        aspect_ratio=aspect_ratio,
        model=model,
        seed=seed,
        output_format=output_format,
        negative_prompt=negative_prompt
    )
    return generator.upload_image_to_s3(image_content, s3_file_path)
