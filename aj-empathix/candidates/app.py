import json
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
@app.route('/candidates', methods=['GET'])
def get_candidates():
    try:
        data= table.scan()['Items']
        response= {'status': 'SUCCESS!, Here are all the candidates:',
                   'data': data
                   }
        return jsonify(response)
    except Exception as e:
        response= {
            'status': 'error',
            'message': str(e)
        }
        return jsonify(response)


# Entrypoint to POST request from database
@app.route('/candidates', methods=['POST'])
def create_candidate():

    # try:
    #     data = {
    #         "id": "7",
    #         "name": "Testing Via Hardcoded Data",
    #         "department": "Technology"
    #     }
    #     table.put_item(Item=data)
    #     response = {
    #         "Message": "SUCCESS! Candidate entry created",
    #         "Data Entered": data
    #         }
    #     return jsonify(response)
    # except Exception as e:
    #     response = {
    #         "message": "Error sending via hardcoded method",
    #         "error": str(e)
    #     }
    #     return jsonify(response)

    try:
        # data = jsonify(request.data())
        data= request.get_json()
        table.put_item(Item=data)

        response = {
            "returned request body": data
        }
        return jsonify(response)
    except Exception as e:
        response = {
            'message': "At line 73 and it failed",
            'error': str(e)
        }
        return jsonify(response)

    except Exception as e:
        response= {
            'message': 'Raw Data is the problem',
            'error': str(e)
        }
        return jsonify(response)
    
    try:
        if not data:
            raise ValueError("No Data Provided")
        
        if 'id' not in data or 'name' not in data or 'department' not in data:
            raise ValueError(f"Missing Required fields. Input Provided: {data}")
        
        table.put_item(Item=data)
        response = {
            "Message": "SUCCESS! Candidate entry created",
            "Data Entered": data
            }
        return jsonify(response)
    except Exception as e:
        response= {
            'message': 'Data was not added to the table',
            'error': str(e)
        }
        return jsonify(response)

