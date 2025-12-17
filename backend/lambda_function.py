# lambda_function.py
import json, os
import boto3

TABLE_NAME = os.environ.get('TABLE_NAME', 'MyResumeViewCount')
dynamodb = boto3.resource('dynamodb', region_name=os.environ.get('AWS_REGION', 'us-east-1'))
table = dynamodb.Table(TABLE_NAME)
CORS = '*'

def lambda_handler(event, context):
    try:
        method = None
        if 'requestContext' in event and 'http' in event['requestContext']:
            method = event['requestContext']['http'].get('method')
        if method is None:
            method = event.get('httpMethod', 'GET')

        if method == 'OPTIONS':
            return {
                'statusCode': 204,
                'headers': {
                    'Access-Control-Allow-Origin': CORS,
                    'Access-Control-Allow-Methods': 'GET,POST,OPTIONS',
                    'Access-Control-Allow-Headers': 'Content-Type'
                },
                'body': ''
            }

        if method == 'POST':
            resp = table.update_item(
                Key={'pk': 'counter'},
                UpdateExpression='SET visits = if_not_exists(visits, :start) + :inc',
                ExpressionAttributeValues={':inc': 1, ':start': 0},
                ReturnValues='UPDATED_NEW'
            )
            views = resp.get('Attributes', {}).get('visits', 0)
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': CORS},
                'body': json.dumps({'views': views})
            }

        # GET
        resp = table.get_item(Key={'pk': 'counter'})
        views = resp.get('Item', {}).get('visits', 0)
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': CORS},
            'body': json.dumps({'views': views})
        }

    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': CORS},
            'body': json.dumps({'error': 'server error'})
        }
