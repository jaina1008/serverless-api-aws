import json
from flask_lambda import FlaskLambda

app = FlaskLambda(__name__)

@app.route('/hello')
def index():
    data = {
        "message": "Hello from app.py"
    }

    return (
        json.dumps(data),
        200,
        {'Content-Type': "application/json"}
    )

    # return json_response

# def json_response(data, response_code=200):
#     return json.dumps(data), response_code, {'Content-Type': 'application/json'}