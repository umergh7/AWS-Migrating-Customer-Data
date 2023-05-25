import requests
import pandas as pd
import json 
import sqlalchemy as db
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from datetime import date
import os
import toml 
import subprocess
import boto3
from datetime import date


def lambda_handler(event, context):

    print("Received event: " + json.dumps(event, indent=2))


    app_config = toml.load('./configuration.toml')

    api_url = app_config['api']['api_url']
    host=app_config['db']['host']
    port=app_config['db']['port']
    database=app_config['db']['database']
    username=app_config['db']['username']
    password=app_config['db']['password']

    #First step is to get the customer list from the S3 .json file

    #read json file to local machine
    access_key=os.getenv('access_key')
    secret_key=os.getenv('secret_key')

    s3 = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key)

    # bucket=app_config['aws']['bucket']
    # folder=app_config['aws']['folder']
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key'].split("/")[1]
    
    
    filepath = "/tmp/" +  key
    download_key = 'input/'+key
    
    s3.download_file(Bucket=bucket, Key= download_key, Filename=filepath)
    


    # current_dir = str(os.getcwd()) +'temp.json'
    # s3.download_file(bucket,'input/data.json', current_dir)

    #downloaded file onto current directory
    #now lets extract all of the customer ids from the json file


    with open(filepath, 'r') as file:
        stringdata = json.load(file)
        data = json.loads(stringdata)
        customerid = list(data['data'][i][0] for i in range(len(data['data'])))

    li=[]
    for id in customerid:
        li.append(str(id))

    id_string = "("+ ",".join(li)+")"

    #connect onto your RDS database and query for customerid, customername, and todays date
    #connect to RDS
    engine = create_engine(f'mysql+mysqlconnector://admin:{password}@aws-superstore-db.cs4mayiuqhbl.ca-central-1.rds.amazonaws.com:3306/superstore')

    sql_query = text(f"select CustomerId, CustomerName from customers WHERE customerid IN {id_string}")

    #convert sql to dataframe
    df=pd.read_sql(sql_query, con=engine)

    today=str(date.today())
    df['date']=today

    jsondata = df.to_json(orient='split', index=False )


    #now send this data to your API endpoint
    request = requests.post(api_url,data=jsondata)
    print(request.status_code)

