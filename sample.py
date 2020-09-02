import csv
import dns
import xlrd
import os
import re
import pandas as pd
from pymongo import MongoClient




def clear_db(myCollection):
    x = myCollection.delete_many({})
    print(x.deleted_count, " documents deleted.")

def preprocess_data(data):
    for col in data.columns:
        if col in ['NAME', 'name', 'CustomerName', 'CLIENT', 'Company / Account', 'Opportunity Name', 'Full_Name']:
            data = data.rename(columns={col: 'Name'})
        elif col == 'Main_Phone':
            data = data.rename(columns={col: 'Phone'})
        elif col in ['AltPhone', 'Phone.1']:
            data = data.rename(columns={col: 'Phone_1'})
            print('Converted phone number header to Phone / Phone_1')
        elif col in ['CLIENT EMAIL', 'Contact:Email', 'Email_Address', 'Email Address']:
            data = data.rename(columns={col: 'Email'})
    return data

def regular_expression(data):
    for col in data.columns:
        if re.search('phone', col, flags=re.I):
            if data[col].dtypes == 'float':
                data = data.astype({col: 'int'}, copy=False, errors='ignore')
            if data[col].dtypes != 'str':
                data = data.astype({col: 'str'}, copy=False)
    return data


def csv_to_json(filename, header=0):
    data = pd.read_csv(filename, header=header, engine='python')
    data = preprocess_data(data)
    data = regular_expression(data)
    print(data.dtypes)
    print('size', data.size)
    return data.to_dict('records')

def excel_to_json(filename, header=0):
    data = pd.read_excel(filename, header=header)
    data = preprocess_data(data)
    data = regular_expression(data)
    print(data.dtypes)
    print('size', data.size)
    return data.to_dict('records')

def main():
    client = MongoClient("mongodb+srv://dbAdmin:insolar@cluster0.huuha.mongodb.net/insolar?retryWrites=true&w=majority")

    database = client['insolar']
    collection = database['contact']
    filepath = './flaskr/data/datachunk1009.xlsx'
    _, file_extension = os.path.splitext(filepath)
    if file_extension == '.csv':
        json_obj = csv_to_json(filepath)
    elif file_extension in ['.xlsx', '.xls']:
        json_obj = excel_to_json(filepath)
    else:
        print('This is not a valid file type!')
    print(json_obj[0])

    #collection.insert_many(json_obj)


main()


