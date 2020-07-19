import json
import pymysql
import os

#Configuration Values

endpoint = 'canoo-test-2.cpgcp7tmn4qn.us-east-2.rds.amazonaws.com'
username = 'admin'
password = 'admin123'
database_name = 'Error_Logs'

#Connection
try:
    connection = pymysql.connect(endpoint, user=username, passwd=password, db=database_name)
    print('****connected to db****')
except:
    print('Error in connecting to db')


def getTenMostRecent(event, context):

    query = "SELECT error_number, time_stamp FROM Logs ORDER BY time_stamp DESC LIMIT 10"

    cursor = connection.cursor()
    cursor.execute(query)

    rows = cursor.fetchall()

    # Build the result variable
    # array of objects
    # Error code and timestamp only
    
    result = []
    for row in rows:
        data = {}
        data['error_code'] = row[0]
        data['timestamp'] = row[1]
        # print("{0} {1}".format(row[0], row[1]))
        result.append(data)

    

    body = {
        "result": result
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response

def addLogs(event, context):

    print(event.body)

 

    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Logs')

    rows = cursor.fetchall()
    for row in rows:
        print("{0} {1} {2} {3}".format(row[0], row[1], row[2], row[3]))


    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response




if __name__ == '__main__':
    endpoint = os.environ['HOST']
    print(endpoint)