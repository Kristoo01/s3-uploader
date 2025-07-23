# S3 CLI Uploader

A minimal Python CLI tool for interacting with Amazon S3. This tool allows users to upload, download, and list files.

---

## Features

* Upload local files to an S3 bucket
* Download files from an S3 bucket
* List contents of a bucket
* Show file size for upload/download
* Logging to track upload/download activity
* Progress bars for long transfers

---

## Tech Stack

* Python 3
* Boto3 (AWS SDK for Python)
* AWS CLI
* Tqdm (for progress bars)

---

## CLI Commands

| Command                        | Description                           |
|-------------------------------|----------------------------------------|
| `upload <filename>`           | Upload a file to the S3 bucket         |
| `download <filename>`         | Download a file from the S3 bucket     |
| `list`                        | List all files in the bucket           |

---

## Running the Project

**1. Install dependencies:** Open and activate a virtual environment, then install required packages: `pip install -r requirements.txt`

**2. Configure AWS credentials:** Make sure your AWS CLI is installed and configured: `aws configure`

**3. Run the CLI:** Run the uploader with commands like: `python uploader.py upload file.txt`, `python uploader.py download file.txt`, or `python uploader.py list`

---

## Setting Up the Environment (Optional but Recommended)

# Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate       # On Windows use: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

---

## File Validation & Logging

* Only .txt, .pdf, .jpg, .png files are accepted
* Activity is logged in `uploader.log`
* Progress is displayed during upload/download

---

## Future Improvements

* Add support for batch file transfers
* Integrate unit tests
* Handle buckets dynamically via arguments or config

---

## Project Status

✅ Minimal viable project (MVP) complete.
