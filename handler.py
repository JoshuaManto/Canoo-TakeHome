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

# GET REQUEST
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

# POST REQUEST
def addLogs(event, context):

    print(event)

    # [{"deviceID": "any_device_token", "err": 107, "timestamp": 1514864773 }]  

    deviceID = event['deviceID']
    err = event['err']
    timestamp = event['timestamp']

    print(deviceID, err, timestamp)
    print(type(err))
    print(type(timestamp))

    query = 'INSERT INTO Logs (device_id, error_number, time_stamp) VALUES (%s, %s, %s)'

    cursor = connection.cursor()
    cursor.execute(query, (deviceID, err, timestamp))

    rows = connection.commit()
    print('rows: ', rows)
    print(cursor)
    print(cursor.rowcount)
    # for row in rows:
    #     print("{0} {1} {2} {3}".format(row[0], row[1], row[2], row[3]))


    body = {
        "result": "Success"
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response




if __name__ == '__main__':
    endpoint = os.environ['HOST']
    print(endpoint)
