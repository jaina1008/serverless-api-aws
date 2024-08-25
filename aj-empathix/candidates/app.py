import boto3
from flask_lambda import FlaskLambda
from flask import Flask, request, jsonify


# Initialise the FlaskLambda application
app = FlaskLambda(__name__)

# Initialise the DynamoDDB resource
ddb = boto3.resource('dynamodb')

# Reference the existing DynamoDB table 'candidates'
table = ddb.Table('candidates')


# Default route to check if the app is running
@app.route('/')
def index():
    try:
        return json_response("Hello World")
    except Exception as e:
        response= {
            'status': 'error',
            'message': str(e)
        }
        return json_response(response)


# Route to handle GET requests to retrieve a candidate by id
@app.route('/candidates/<id>', methods=['GET'])
def get_candidate(id):
    try:
        key= {'id': id}
        candidate= table.get_item(Key=key).get('Item')

        if not candidate:
            return json_response(f"No Entry Found for id: {id}", 404)
        else:
            return json_response("Candidate Found!", candidate)
    except Exception as e:
        return json_response("error", 501)


# Route to handle POST requests to create a new candidate
@app.route('/candidates', methods=['POST'])
def create_candidate():
    try:
        data= request.get_json()

        if not data or 'id' not in data:
            return json_response("Missing 'id' ", 400)

        # Validate that 'id' is a string
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


# Route to handle PUT requests to update the existing candidate
@app.route('/candidates/<id>', methods=['PUT'])
def update_candidate(id):
    try:    
        data= request.get_json()

        if not data:
            return json_response("No Data Provided", 400)

        # Validate that 'id' is a string
        if not isinstance(data['id'], str):
            return json_response("ID must be a string", 400)
        
        # Ensure the id in the path mathes the id in the data
        if id != data['id']:
            return json_response("id mismatch", 400)
        
        item= {'id': id}
        item.update(data)
        table.put_item(Item= item)
        return json_response("Candidate Updated Successfully!", item, 200)
    except Exception as e:
        return json_response("error", 501)


# Route to handkle DELETE requests to remove a candidate by id
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
    

# Helper function to generate a JSON response
def json_response(message, *args, **kwargs):
    response= {"Message": message}

    if args:
        response['args']= args
    if kwargs:
        response['kwargs']= kwargs

    return jsonify(response)


# Test application locally
# if __name__=="__main__":
#     app.run(debug=True)  # run the Flask app in debug mode