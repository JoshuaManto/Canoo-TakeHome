import json
import pymysql
import os

# access credentials
db_name = os.environ.get('DBNAME')
user = os.environ.get('USER')
host = os.environ.get('HOST')
password = os.environ.get('PASS')
port = os.environ.get('PORT')


def hello(event, context):

    print(db_name, user, host, password, port)

    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response

    # Use this code if you don't use the http event with the LAMBDA-PROXY
    # integration
    """
    return {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "event": event
    }
    """
