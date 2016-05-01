import boto3

class FileDownload:

    def __init__(self):
        aws_access_key_id = "ExampleAccessString" #insert your access id
        aws_secret_access_key = "ExampleAccessKey" #insert your access key
        s3_bucket_name = "your-s3-bucket-name" #inster your s3 bucket


    def file_download(self):
        s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id ,aws_secret_access_key=aws_secret_access_key)

        # Download tmp.txt as tmp2.txt
        s3.download_file(s3_bucket_name, "price-comparison-recent.json", "/tmp/price-comparison-recent.json")
        s3.download_file(s3_bucket_name, "hills_urls.json", "/tmp/hills_urls.json")
        s3.download_file(s3_bucket_name, "1E-hills-prices-recent.json", "/tmp/1E-hills-prices-recent.json")
        s3.download_file(s3_bucket_name, "pages_to_check.json", "/tmp/pages_to_check.json")
        s3.download_file(s3_bucket_name, "pages_to_check_test.json", "/tmp/pages_to_check_test.json")
        s3.download_file(s3_bucket_name, "prices-recent.json", "/tmp/prices-recent.json")
