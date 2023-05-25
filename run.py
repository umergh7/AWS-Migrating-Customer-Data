from sqlalchemy import create_engine, text
import pandas as pd
# import subprocess
import toml
import os
from dotenv import load_dotenv
import json
import boto3

app_config = toml.load('config.toml')

load_dotenv()


#establish connection to mysql server
password = os.getenv('password')
engine = create_engine(f'mysql+mysqlconnector://admin:{password}@aws-superstore-db.cs4mayiuqhbl.ca-central-1.rds.amazonaws.com:3306/superstore')


sql_query = text("select CustomerId, sum(sales) as Sales from orders GROUP BY CustomerId ORDER BY Sales DESC LIMIT 10")

#convert sql to dataframe
df=pd.read_sql(sql_query, con=engine)


jsondata = df.to_json(orient='split', index=False)

filepath='/home/ubuntu/python/data.json'

with open(filepath, 'w') as file:
    json.dump(jsondata, file)


#load the file onto a s3 bucket:
# upload the csv file to AWS S3
bucket = app_config['aws']['bucket']
folder = app_config['aws']['folder']

s3 = boto3.client('s3')

# s3 = boto3.resource('s3',
#          aws_access_key_id=ACCESS_ID,
#          aws_secret_access_key= ACCESS_KEY)

s3.upload_file('data.json', bucket, folder+'data.json')
