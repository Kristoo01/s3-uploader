import boto3
import argparse
import os
import logging
from tqdm import tqdm
import threading

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

class ProgressPercentage:
    """Helper class to show upload/download progress with tqdm."""
    def __init__(self, filename):
        self._filename = filename
        self._size = float(os.path.getsize(filename))
        self._seen_so_far = 0
        self._lock = threading.Lock()
        self._progress_bar = tqdm(
            total=self._size, unit='B', unit_scale=True, desc=filename
        )

    def __call__(self, bytes_amount):
        with self._lock:
            self._seen_so_far += bytes_amount
            self._progress_bar.update(bytes_amount)
            if self._seen_so_far >= self._size:
                self._progress_bar.close()

# Load configuration from environment variables
BUCKET_NAME = os.getenv('AWS_S3_BUCKET')
REGION_NAME = os.getenv('AWS_REGION', 'eu-north-1')  # Default region fallback

# Initialize the S3 client
s3 = boto3.client('s3', region_name=REGION_NAME)

def upload_file(file_path):
    """Upload a file to the S3 bucket with validation and progress bar."""
    if not os.path.isfile(file_path):
        logger.error("File does not exist.")
        return

    if os.path.getsize(file_path) == 0:
        logger.warning("File is empty.")
        return

    allowed_extensions = {'.txt', '.pdf', '.jpg', '.png'}
    _, ext = os.path.splitext(file_path)
    if ext.lower() not in allowed_extensions:
        logger.error(f"File type '{ext}' not allowed. Allowed types: {', '.join(allowed_extensions)}")
        return

    filename = os.path.basename(file_path)
    s3.upload_file(
        file_path,
        BUCKET_NAME,
        filename,
        Callback=ProgressPercentage(file_path)
    )
    logger.info(f"Uploaded '{filename}' to bucket '{BUCKET_NAME}'.")

def download_file(file_name):
    """Download a file from the S3 bucket with progress bar."""
    s3.download_file(
        BUCKET_NAME,
        file_name,
        file_name,
        Callback=ProgressPercentage(file_name)
    )
    logger.info(f"Downloaded '{file_name}' from bucket '{BUCKET_NAME}'.")

def list_files():
    """List all files currently stored in the S3 bucket."""
    response = s3.list_objects_v2(Bucket=BUCKET_NAME)
    if 'Contents' in response:
        logger.info("Files in bucket:")
        for obj in response['Contents']:
            logger.info(f"- {obj['Key']}")
    else:
        logger.info("Bucket is empty.")

if __name__ == "__main__":
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="S3 CLI Uploader")
    parser.add_argument("action", choices=["upload", "download", "list"], help="Action to perform")
    parser.add_argument("filename", nargs="?", help="File to upload/download (not required for 'list')")
    args = parser.parse_args()

    # Perform the selected action
    if args.action == "upload":
        if not args.filename:
            logger.error("Please provide the file path to upload.")
        else:
            upload_file(args.filename)

    elif args.action == "download":
        if not args.filename:
            logger.error("Please provide the file name to download.")
        else:
            download_file(args.filename)

    elif args.action == "list":
        list_files()