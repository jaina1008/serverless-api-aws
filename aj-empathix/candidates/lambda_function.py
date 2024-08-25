from app import app
from serverless_wsgi import handle_request

# This is the entry point for AWS Lambda function execution.
def lambda_handler(event, context):
    # The handle_request function processes incoming request using Flask app instance.
    return handle_request(app, event, context)