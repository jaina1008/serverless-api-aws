import boto3
import awsgi
from flask import Flask, request, jsonify

# Creating insances of Flask
app = Flask(__name__)
# Creating insances of DynamoDB database
ddb = boto3.resource('dynamodb')
# Creating a new table 'candidates' in database
table = ddb.Table('candidates')


@app.before_request
def set_url_scheme():
    if 'wsgi.url_scheme' not in request.environ:
        request.environ['wsgi.url_scheme'] = 'https' 


# Setting up default route
@app.route('/')
def index():
    return jsonify(message="Hello world - from app.py")

# Setting up candidates route to get or post candidate from/to database
@app.route('/candidates', methods=['GET', 'POST'])
def put_list_candidate():
    if request.method == 'GET':
        # Scan the database
        candidates = table.scan()['Items']
        return jsonify(message=candidates)
    else:
        request_json = request.get_json()
        table.put_item(Item=request_json)
        return jsonify(message="candidate entry created")


def handler(event, context):
    return awsgi.response_from_flask(app, event, context)