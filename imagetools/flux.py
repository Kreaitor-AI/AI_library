import fal_client
import boto3
from botocore.exceptions import NoCredentialsError
import uuid
import os

class flux:
    def __init__(self, fal_key, aws_access_key, aws_secret_key, bucket_name):
        # Initialize credentials and clients
        self.fal_key = fal_key
        self.bucket_name = bucket_name

        # Set the environment variable for FAL_KEY
        os.environ["FAL_KEY"] = self.fal_key

        # Initialize AWS S3 client
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key
        )
    
    def generate_image(self, prompt):
        handler = fal_client.submit(
            "fal-ai/flux/schnell",
            arguments={"prompt": prompt},
        )
        result = handler.get()
        if 'image' in result:
            return result['image']  # Assuming the image content is returned here
        else:
            raise Exception("Image generation failed.")
    
    def upload_image_to_s3(self, image_content, s3_file_path):
        try:
            self.s3_client.put_object(Bucket=self.bucket_name, Key=s3_file_path, Body=image_content)
            return f"https://{self.bucket_name}.s3.amazonaws.com/{s3_file_path}"
        except NoCredentialsError:
            raise Exception("Credentials not available for AWS S3")

def flux(fal_key, aws_access_key, aws_secret_key, bucket_name, prompt):
    generator = flux(fal_key, aws_access_key, aws_secret_key, bucket_name)
    
    # Generate the image
    image_content = generator.generate_image(prompt)
    
    # Generate a unique filename
    unique_id = uuid.uuid4()
    s3_file_path = f"images/{unique_id}.png"  # Assuming the output format is PNG
    
    # Upload the image to S3
    return generator.upload_image_to_s3(image_content, s3_file_path)
