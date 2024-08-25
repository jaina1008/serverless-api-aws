import boto3
from flask_lambda import FlaskLambda
from flask import Flask, request, jsonify

# Creating insances of Flask Lambda
app = FlaskLambda(__name__)
# Creating insances of DynamoDB database
ddb = boto3.resource('dynamodb')
# Creating a new table 'candidates' in database
table = ddb.Table('candidates')


# Setting up default route
@app.route('/')
def index():
    try:
        response= {
            "Message": "Hello from app.py"
        }
        return jsonify(response)

    except Exception as e:
        response= {
            'status': 'error',
            'message': str(e)
        }
        return jsonify(response)


# Entrypoint to GET request from database
@app.route('/candidates/<id>', methods=['GET'])
def get_candidates(id):
    try:
        key= {'id': id}
        candidate= table.get_item(Key=key).get('Item')
        if not candidate:
            return json_response(f"No Entry Found for id: {id}", 404)
        else:
            return json_response("Candidate Found!", candidate)
    except Exception as e:
        return json_response("error", 501)


# Entrypoint to POST request from database
@app.route('/candidates', methods=['POST'])
def create_candidate():
    try:
        data= request.get_json()
        if not data or 'id' not in data:
            return json_response("Missing 'id' ", 400)

        # Check if 'id' is a string
        if not isinstance(data['id'], str):
            return json_response("ID must be a string", 400)
        
        key= {'id': data['id']}
        item= table.get_item(Key= key).get('Item')

        if item:
            return json_response("Candidate already exists", 400)
        else:
            table.put_item(Item= data)
            return json_response("Candidate Created!", data, 200)
    except Exception as e:
        return json_response("error", 501)


# Entrypoint to PUT request from database
@app.route('/candidates/<id>', methods=['PUT'])
def update_candidate(id):
    try:    
        data= request.get_json()
        if not data:
            return json_response("No Data Provided", 400)

        # Check if 'id' is a string
        if not isinstance(data['id'], str):
            return json_response("ID must be a string", 400)
        
        # Check if 'id' is a string
        if not isinstance(data['id'], str):
            return json_response("ID must be a string", 400)
        
        if id != data['id']:
            return json_response("id mismatch", 400)
        
        item= {'id': id}
        item.update(data)
        table.put_item(Item= item)
        return json_response("Candidate Updated Successfully!", item, 200)
    except Exception as e:
        return json_response("error", 501)


# Entrypoint to DELETE request from database
@app.route('/candidates/<id>', methods=['DELETE'])
def delete_candidate(id):
    try:
        key= {'id': id}
        candidate= table.get_item(Key=key).get('Item')

        if not candidate:
            return json_response(f"No Entry Found for id: {id}", 404)
        
        else:
            table.delete_item(Key=key)
            return json_response("Candidate is now Deleted")
    except Exception as e:
        return json_response("error", 501)
    


def json_response(message, *args, **kwargs):
    response= {"Message": message}
    if args:
        response['args']= args
    if kwargs:
        response['kwargs']= kwargs

    return jsonify(response)


if __name__=="__main__":
    app.run(debug=True)  # run the Flask app in debug mode