def lambda_handler(event, context):
    """
    Test handler for the Senior Dev Lambda function
    """
    return {
        'statusCode': 200,
        'body': {
            'message': 'Senior Dev function executed successfully',
            'input': event
        }
    }
