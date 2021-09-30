import boto3
import random
from PIL import Image
import urllib.request 


def resize(name, img, size, bucket):
    s3 = boto3.client('s3')

    w, h = size
    ratios = [0.9, 0.5, 0.3]
    
    for ratio in ratios:
        out = img.resize( [int(ratio * s) for s in img.size])
        out_name =name+str(ratio)+'.jpeg'
        out.save('/tmp/'+out_name, "JPEG")
        s3.upload_file('/tmp/'+out_name, bucket, out_name)
    img.thumbnail((128, 128), Image.ANTIALIAS)
    out_name =name+'thumbnail.jpeg'
    img.save('/tmp/'+out_name, "JPEG")
    s3.upload_file('/tmp/'+out_name, bucket, out_name)


def function_handler(event, context):
    input = event['name']
    bucket = event['bucket']
    address = event['address']
    print('Resizing ', input)
    urllib.request.urlretrieve(address, '/tmp/'+input)
    img = Image.open('/tmp/'+input)
    resize(input, img, img.size, bucket)
    return {'statusCode':200, 'body':'AWS'}
