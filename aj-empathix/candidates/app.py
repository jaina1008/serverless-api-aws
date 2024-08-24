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
    print('dir to request LOOKS LIKE THIS: ', dir(request))
    print('request get_data LOOKS LIKE THIS: ', request.get_data)
    print('request get json LOOKS LIKE THIS: ', request.get_json)
    print('request content_encoding LOOKS LIKE THIS: ', request.content_encoding)

    try:
        data = request.json

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
    

  # Entrypoint to GET, PUT and DELETE requests from database with specific ID
# @app.route('/candidates/<id>', methods=['GET', 'PATCH', 'DELETE'])
# def get_patch_delete_candidate(id):
#     key = {'id': id}
#     if request.method == 'GET':
#         candidate = table.get_item(Key=key).get('Item')
#         if candidate:
#             return json_response(candidate)
#         else:
#             return json_response({"message": "candidate not found"}, 404)
#     elif request.method == 'PATCH':
#         attribute_updates = {key: {'Value': value, 'Action': 'PUT'}
#                              for key, value in request.form.items()}
#         table.update_item(Key=key, AttributeUpdates=attribute_updates)
#         return json_response({"message": "candidate entry updated"})
#     else:
#         table.delete_item(Key=key)
#         return json_response({"message": "candidate entry deleted"})

# # Returns data and response code in JSON format
# def json_response(data, response_code=200):
#     return json.dumps(data), response_code, {'Content-Type': 'application/json'}


    # except ValueError as ve:
    #     response= {
    #         'status': 'Value error',
    #         'message': str(ve)
    #     }
    #     return jsonify(response), 400
    
    # except Exception as e:
    #     response= {
    #         'status': 'Generic error',
    #         'message': str(e)
    #     }
    #     return jsonify(response), 500
        

# # Returns data and response code in JSON format
# def json_response(data, response_code=200):
#     return (json.dumps(data),
#             response_code,
#             {'Content-Type': 'application/json'}
#             )


if __name__=="__main__":
    app.run(debug=True)  # Run the Flask app in debug mode