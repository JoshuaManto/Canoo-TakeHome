import json
import pymysql
import os

#Configuration Values

endpoint = os.environ['HOST']
username = os.environ['USER']
password = os.environ['PASS']
database_name = os.environ['DBNAME']

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

    # Get payload from event body
    # Should be an array of objects
    payload = event['payload']

    query = 'INSERT INTO Logs (device_id, error_number, time_stamp) VALUES (%s, %s, %s)'

    # Build data to be inserted to the database
    # Array of tuples
    data = []
    
    for row in payload:
        data.append((row['deviceID'], row['err'], row['timestamp']))

    cursor = connection.cursor()

    # Handles 1 or more incoming data
    if(len(data) == 1):
        # print('1 data')
        cursor.execute(query, data[0])
    elif(len(data) > 1):
        # print('2 or more data')
        cursor.executemany(query, data)

    body = {
        "result": "Success. {0} number of data inserted".format(cursor.rowcount)
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response




if __name__ == '__main__':
    endpoint = os.environ['HOST']
    print(endpoint)
