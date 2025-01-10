def lambda_handler(event, context):
    """
    Test handler for the Agile Coach Lambda function
    """
    return {
        'statusCode': 200,
        'body': {
            'message': 'Agile Coach function executed successfully',
            'input': event
        }
    }
