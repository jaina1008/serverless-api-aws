import json
import boto3
from flask_lambda import FlaskLambda
from flask import request

# Creating insances of Flask Lambda
app = FlaskLambda(__name__)
# Creating insances of DynamoDB database
ddb = boto3.resource('dynamodb')
# Creating a new table in database
table = ddb.table('candidates')

# Setting up default route
@app.route('/')
def index():
    return json_response({"message": "Hello world -> from app.py"})

# Setting up candidates route to get or post candidate from/to database
@app.route('/candidates', methods=['GET', 'POST'])
def put_list_candidate():
    if request.method == 'GET':
        candidates = table.scan()['Items']
        return json_response(candidates)
    else:
        table.put_item(Item=request.form.to_dict())
        return json_response({"message": "candidate entry created"})


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


def json_response(data, response_code=200):
    return json.dumps(data), response_code, {'Content-Type': 'application/json'}