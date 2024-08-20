import json
import boto3
from flask_lambda import FlaskLambda
from flask import request

# Creating insances of Flask Lambda
app = FlaskLambda(__name__)
# Creating insances of DynamoDB database
ddb = boto3.resource('dynamodb')
# Creating a new table 'candidates' in database
table = ddb.Table('candidates')

# Setting up default route
@app.route('/')
def index():
    return json_response({"message": "Hello world - from app.py"})

#  Entrypoint to GET and POST requests from database
@app.route('/candidates', methods=['GET', 'POST'])
def put_list_candidate():
    if request.method == 'GET':
        # Scan the database
        candidates = table.scan()['Items']
        return json_response(candidates)
    else:
        table.put_item(Item=request.form.to_dict())
        return json_response({"message": "candidate entry created"})


#  Entrypoint to GET and POST requests from database with specific ID
@app.route('/candidates/<id>', methods=['GET', 'PATCH', 'DELETE'])
def get_patch_delete_candidate(id):
    key = {'id': id}
    if request.method == 'GET':
        candidate = table.get_item(Key=key).get('Item')
        if candidate:
            return json_response(candidate)
        else:
            return json_response({"message": "candidate not found"}, 404)
    elif request.method == 'PATCH':
        attribute_updates = {key: {'Value': value, 'Action': 'PUT'}
                             for key, value in request.form.items()}
        table.update_item(Key=key, AttributeUpdates=attribute_updates)
        return json_response({"message": "candidate entry updated"})
    else:
        table.delete_item(Key=key)
        return json_response({"message": "candidate entry deleted"})

# Returns data and response code in JSON format
def json_response(data, response_code=200):
    return json.dumps(data), response_code, {'Content-Type': 'application/json'}