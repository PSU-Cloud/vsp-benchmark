#have to have ffmepg layer: https://aws.amazon.com/blogs/media/processing-user-generated-content-using-aws-lambda-and-ffmpeg/
import boto3
import subprocess
import random 
import urllib.request

def encode(bucket, name):
    

    print('Encoding ', name)
    urllib.request.urlretrieve(address, '/tmp/'+name)
    
    cmd = ['/opt/bin/ffmpeg' , '-i', '/tmp/'+name, '-r', '15', '-vf', 'scale=512:-1', '/tmp/out.gif']
    
    subprocess.call(cmd)
    out_name = name +'-GIF.gif'
    s3.upload_file('/tmp/out.gif', bucket, out_name)

def lambda_handler(event, context):
    name = event['name']
    bucket = event['bucket']
    address = event['address']
    encode(bucket, name, address)
    return {'statusCode':200, 'body':'AWS',}

