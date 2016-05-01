import boto3

class FileUpload:

    def __init__(self):
        aws_access_key_id = "ExampleAccessString" #insert your access id
        aws_secret_access_key = "ExampleAccessKey" #insert your access key
        s3_bucket_name = "your-s3-bucket-name" #inster your s3 bucket

    #other_filenames should be a list of filenames. it is assumed they are in the tmp folder.
    def file_upload(self, other_filenames=None):

        s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id ,aws_secret_access_key=aws_secret_access_key)

        # Upload tmp.txt to bucket-name
        s3.upload_file("/tmp/price-comparison-recent.json", s3_bucket_name, "price-comparison-recent.json")
        s3.upload_file("/tmp/hills_urls.json", s3_bucket_name, "hills_urls.json")
        s3.upload_file("/tmp/1E-hills-prices-recent.json", s3_bucket_name, "1E-hills-prices-recent.json")
        s3.upload_file("/tmp/pages_to_check.json", s3_bucket_name, "pages_to_check.json")
        s3.upload_file("/tmp/pages_to_check_test.json", s3_bucket_name, "pages_to_check_test.json")
        s3.upload_file("/tmp/prices-recent.json", s3_bucket_name, "prices-recent.json")
        if other_filenames:
            for each_filename in other_filenames:
                s3.upload_file("/tmp/%s" % each_filename, s3_bucket_name, each_filename)
