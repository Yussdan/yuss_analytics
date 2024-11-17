import requests
import logging
import os
import boto3
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger('api')


class S3Client:
    def __init__(self, aws_access_key_id=None, aws_secret_access_key=None, endpoint_url=None, region=None):
        """
        S3 client initialization.
        ::param aws_access_key_id: JAWS access key (by default, it is taken from the environment variable 's3_key_id').
        :param aws_secret_access_key: AWS secret key (by default from the environment variable 's3_key_pass').
        :param endpoint_url: S3 storage URL (optional).
        :param region: S3 region (optional).
        """
        self.aws_access_key_id =  aws_access_key_id or os.getenv('s3_key_id')
        self.aws_secret_access_key = aws_secret_access_key or os.getenv('s3_key_pass')
        self.endpoint_url = endpoint_url or "https://s3.cloud.ru/"
        self.region = region or "ru-central-1"
        
        if not self.aws_access_key_id or not self.aws_secret_access_key:
            raise ValueError("AWS keys must be specified either explicitly or through environment variables.")

        self.s3 = None

    def _get_session(self):
        """Creates an S3 session if it has not already been created."""
        if self.s3 is None:
            self.s3 = boto3.session.Session(
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key,
                region_name=self.region
            ).client(service_name='s3', endpoint_url=self.endpoint_url)

    def _ensure_session(self):
        """Checks for an active session, creating it if necessary."""
        if not self.s3:
            self._get_session()

    def upload_image(self, bucket: str, local_file: str, bucket_file: str):
        """
        Uploads the file to S3.
        : param bucket: name bucket-A.
        : param local_file: local path to the file.
        : param bucket_file:file name in bucket-E.
        """
        self._ensure_session()
        try:
            self.s3.upload_fileobj(local_file, bucket, bucket_file)
            return(f"File {local_file} successfully uploaded to {bucket}/{bucket_file}.")
        except Exception as e:
            raise Exception(f"Error uploading the file:{e}")

    def download_image(self, bucket: str, bucket_file: str):
        """
        Downloads a file from S3.
        :param bucket: The name of the bucket.
        :param bucket_file: The name of the file in the bucket.
        :param local_file: The local path to save the file.
        """
        self._ensure_session()
        try:
            return self.s3.get_object(Bucket=bucket, Key=bucket_file)['Body'].read()
        except Exception as e:
            raise Exception(f"Error downloading the file: {e}")
            

def make_request(endpoint='', params=None, url='https://min-api.cryptocompare.com/data/'):
    try:
        response = requests.get(url + endpoint, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Request error: {e}")
        return {"error": str(e)}
    