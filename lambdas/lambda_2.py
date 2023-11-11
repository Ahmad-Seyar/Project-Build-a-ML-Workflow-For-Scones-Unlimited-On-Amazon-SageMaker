import json
import sagemaker
import base64
import boto3
import sagemaker
from sagemaker.serializers import IdentitySerializer

# Fill this in with the name of your deployed model
ENDPOINT = 'image-classification-2023-10-26-10-34-35-929' ## TODO: fill in

runtime= boto3.client('runtime.sagemaker')

def lambda_handler(event, context):

    # # Decode the image data
    image = base64.b64decode(event["body"]["image_data"])
    
    # Make a prediction:
    predictor = runtime.invoke_endpoint(EndpointName=ENDPOINT,
                                    #   ContentType='image/png',
                                    ContentType='application/x-image',
                                      Body=image)
    
    # We return the data back to the Step Function    
    event["inferences"] = json.loads(predictor['Body'].read().decode('utf-8'))
    return {
        'statusCode': 200,
        # 'body': json.dumps(event)
        "body": {
            "image_data": event["body"]['image_data'],
            "s3_bucket": event["body"]['s3_bucket'],
            "s3_key": event["body"]['s3_key'],
            "inferences": event['inferences'],
      }
    }
