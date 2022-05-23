from flask import Flask, request, jsonify
import os
import boto3
from botocore.config import Config

app = Flask(__name__)

my_config = Config(
    region_name = 'us-east-1'
)

rds_data = boto3.client('rds-data', config=my_config, aws_access_key_id='AKIAU5LCV4RZJQSV2A62', aws_secret_access_key='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')

#Database Configuration Items
aurora_db_name = 'tce_it' #os.environ['DB_NAME']
aurora_cluster_arn = 'arn:aws:rds:us-east-1:337898759282:cluster:database-1' #os.environ['CLUSTER_ARN']
aurora_secret_arn = 'arn:aws:secretsmanager:us-east-1:337898759282:secret:eniyan123-uJxzWF' #os.environ['SECRET_ARN']

@app.route('/getPerson') # API 1 - getPerson
def getPerson():
    personId = request.args.get('personId')
    response = callDbWithStatement("SELECT * FROM Persons WHERE personId='" + str(personId) + "'" )
    person = {}
    records = response['records']
    for record in records:
        person['personId'] = record[0]['longValue']
        person['firstName'] = record[1]['stringValue']
        person['lastName'] = record[2]['stringValue']
    print(person)
    return jsonify(person)

@app.route('/createPerson',  methods=['POST']) # API 2 - createPerson
def createPerson():
    request_data = request.get_json()
    personId = str(request_data['personId'])
    firstName = request_data['firstName']
    lastName = request_data['lastName']
    callDbWithStatement("INSERT INTO Persons(personId, firstName, lastName) VALUES ('" 
    + personId + "', '" + firstName + "', '" + lastName + "');")
    return ""
    
def callDbWithStatement(statement):
    response = rds_data.execute_statement(
            database = aurora_db_name,
            resourceArn = aurora_cluster_arn,
            secretArn = aurora_secret_arn,
            sql = statement,
            includeResultMetadata = True
        )
    print("Making Call " + statement)
    print(response) #Delete this in production
    return response

if __name__ == '__main__':
    app.run(threaded=True,host='0.0.0.0',port=8081)