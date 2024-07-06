import boto3
import os

print(os.getenv("AWS_ACCESS_KEY_ID"))
AWS_S3_CREDS = {
    "aws_access_key_id":os.getenv("AWS_ACCESS_KEY"),
    "aws_secret_access_key":os.getenv("AWS_SECRET_KEY")
}
s3_client = boto3.resource('s3',**AWS_S3_CREDS)


my_bucket = s3_client.Bucket('miratech-project')

for file in my_bucket.objects.all():
    print(file.key)