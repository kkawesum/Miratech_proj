import boto3
import os
from auth import file_searched

class AWSConn():
    def conn_aws():
        AWS_S3_CREDS = {
            "aws_access_key_id":os.getenv("AWS_ACCESS_KEY"),
            "aws_secret_access_key":os.getenv("AWS_SECRET_KEY")
        }
        s3_client = boto3.resource('s3',**AWS_S3_CREDS)


        my_bucket = s3_client.Bucket('miratech-project')
        return my_bucket
    
    def check_file(file_searched, my_bucket):
        if file_searched in my_bucket.objects.all():
            return True


if __name__ == "__main__":
    connect = AWSConn()
    bucket = connect.conn_aws()
    file_present = connect.check_file(file_searched,bucket)

    