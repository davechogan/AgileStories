def lambda_handler(event, context):
    """
    Test handler for the Branding Config Lambda function
    """
    return {
        'statusCode': 200,
        'body': {
            'message': 'Branding Config function executed successfully',
            'input': event
        }
    } 