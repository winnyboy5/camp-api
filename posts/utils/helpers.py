import boto3, botocore
from app import app

s3 = boto3.client(
   "s3",
   aws_access_key_id=app.config['S3_KEY'],
   aws_secret_access_key=app.config['S3_SECRET']
)

def upload_file_to_s3(file, bucket_name, user_name, filename, content_type,acl="public-read"):
    
    try:

        s3.upload_fileobj(
            file,
            bucket_name,
            f"cpusers/{user_name}/media/{filename}",
            ExtraArgs={
                "ACL": acl,
                "ContentType": content_type
            }
        )

    except Exception as e:
        print("Something Happened: ", e)
        return e

    return f'{app.config["S3_LOCATION"]}cpusers/{user_name}/{filename}'