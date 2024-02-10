#importing all the required librairies
import git
import os
import pandas as pd
import json
import requests
import psycopg2
import streamlit as st


# cloning github respository and making connection
def git_connect():
    try:
        git.Repo.clone_from("https://github.com/PhonePe/pulse.git", "C:/FSA IT/DATA SCIENCE COURSE/phonepe_project/Phonepe_project01022024/pulse")
    except:
        pass


git_connect()


# connecting to the local database postgresql

my_db = psycopg2.connect(
                        host="localhost",
                        user="postgres",
                        password="sa",
                        database="phonepe",
                        port="5432"
)

mycursor = my_db.cursor()


# extracting the aggregated transaction data from the pulse folder
class data_extract:
    def aggregated_transaction():
        try:
            path = 'C:/FSA IT/DATA SCIENCE COURSE/phonepe_project/Phonepe_project01022024/pulse/data/aggregated/transaction/country/india/state/'
            agg_state_list = os.listdir(path)

            data = {'State': [], 'Year': [], 'Quarter': [], 'Transaction_type': [],
                    'Transaction_count': [], 'Transaction_amount': []}

            for i in agg_state_list:
                path_i = path + i + '/'
                agg_year_list = os.listdir(path_i)

                for j in agg_year_list:
                    path_j = path_i + j + "/"
                    agg_year_json = os.listdir(path_j)

                    for k in agg_year_json:
                        path_k = path_j + k
                        file = open(path_k, "r")
                        d = json.load(file)

                        for z in d['data']['transactionData']:
                            type = z['name']
                            count = z['paymentInstruments'][0]['count']
                            amount = z['paymentInstruments'][0]['amount']

                            data['State'].append(i)
                            data['Year'].append(j)
                            data['Quarter'].append(k[0])
                            data['Transaction_type'].append(type)
                            data['Transaction_count'].append(count)
                            data['Transaction_amount'].append(amount)

            return data

        except:
            pass
    
    #Extractig the aggregated user data fom the ule folder
    def aggregated_user():
        try:
            path = "C:/FSA IT/DATA SCIENCE COURSE/phonepe_project/Phonepe_project01022024/pulse/data/aggregated/user/country/india/state/"
            agg_state_list = os.listdir(path)
            data = {'State': [], 'Year': [], 'Quarter': [],
                    'User_brand': [], 'User_count': [], 'User_percentage': []}
            for i in agg_state_list:
                path_i = path + i + '/'
                agg_year_list = os.listdir(path_i)
                for j in agg_year_list:
                    path_j = path_i + j + '/'
                    agg_year_json = os.listdir(path_j)
                    for k in agg_year_json:
                        path_k = path_j + k
                        file = open(path_k, 'r')
                        d = json.load(file)
                        try:
                            for z in d['data']['usersByDevice']:
                                brand = z['brand']
                                count = z['count']
                                percentage = (z['percentage']*100)

                                data['State'].append(i)
                                data['Year'].append(j)
                                data['Quarter'].append(k[0])
                                data['User_brand'].append(brand)
                                data['User_count'].append(count)
                                data['User_percentage'].append(percentage)

                        except:
                            pass

            return data

        except:
            pass
    
    #Extracting map transaction data from the pulse folder
    def map_transaction():
        try:
            path = "C:/FSA IT/DATA SCIENCE COURSE/phonepe_project/Phonepe_project01022024/pulse/data/map/transaction/hover/country/india/state/"
            agg_state_list = os.listdir(path)
            data = {'State': [], 'Year': [], 'Quarter': [], 'District': [],
                    'Transaction_count': [], 'Transaction_amount': []}
            for i in agg_state_list:
                path_i = path + i + '/'
                agg_year_list = os.listdir(path_i)
                for j in agg_year_list:
                    path_j = path_i + j + '/'
                    agg_year_json = os.listdir(path_j)
                    for k in agg_year_json:
                        path_k = path_j + k
                        f = open(path_k, 'r')
                        d = json.load(f)
                        for z in d['data']['hoverDataList']:
                            #need to check with the guvi team
                            district = z['name'].split(' district')[0]
                            count = z['metric'][0]['count']
                            amount = z['metric'][0]['amount']
                            data['State'].append(i)
                            data['Year'].append(j)
                            data['Quarter'].append(k[0])
                            data['District'].append(district)
                            data['Transaction_count'].append(count)
                            data['Transaction_amount'].append(amount)
            return data

        except:
            pass

    # Extracting the map user data from the folder pulse folder
    def map_user():
        try:
            path = "C:/FSA IT/DATA SCIENCE COURSE/phonepe_project/Phonepe_project01022024/pulse/data/map/user/hover/country/india/state/"
            agg_state_list = os.listdir(path)

            data = {'State': [], 'Year': [], 'Quarter': [],
                    'District': [], 'Registered_user': [], 'App_opens': []}

            for i in agg_state_list:
                path_i = path + i + "/"
                agg_year_list = os.listdir(path_i)

                for j in agg_year_list:
                    path_j = path_i + j + "/"
                    agg_year_json = os.listdir(path_j)
                    for k in agg_year_json:
                        path_k = path_j + k
                        file = open(path_k, "r")
                        d = json.load(file)

                        for z_key, z_value in d['data']['hoverData'].items():
                            district = z_key.split(' district')[0]
                            reg_user = z_value['registeredUsers']
                            app_opens = z_value['appOpens']
                            data['State'].append(i)
                            data['Year'].append(j)
                            data['Quarter'].append(k[0])
                            data['District'].append(district)
                            data['Registered_user'].append(reg_user)
                            data['App_opens'].append(app_opens)
            return data

        except:
            pass
    
    #Extracting top transaction data from the pulse folder
    def top_transaction():
        try:
            path = "C:/FSA IT/DATA SCIENCE COURSE/phonepe_project/Phonepe_project01022024/pulse/data/top/transaction/country/india/state/"
            agg_state_list = os.listdir(path)
            data = {'State': [], 'Year': [], 'Quarter': [], 'District': [],
                    'Transaction_count': [], 'Transaction_amount': []}
            for i in agg_state_list:
                path_i = path + i + '/'
                agg_year_list = os.listdir(path_i)
                for j in agg_year_list:
                    path_j = path_i + j + '/'
                    agg_year_json = os.listdir(path_j)
                    for k in agg_year_json:
                        path_k = path_j + k
                        f = open(path_k, 'r')
                        d = json.load(f)
                        for z in d['data']['districts']:
                            district = z['entityName']
                            count = z['metric']['count']
                            amount = z['metric']['amount']
                            data['State'].append(i)
                            data['Year'].append(j)
                            data['Quarter'].append(k[0])
                            data['District'].append(district)
                            data['Transaction_count'].append(count)
                            data['Transaction_amount'].append(amount)
            return data
        except:
            pass

   
    #Extracting top user data from the pulse folder
    def top_user():
        try:
            path = "C:/FSA IT/DATA SCIENCE COURSE/phonepe_project/Phonepe_project01022024/pulse/data/top/user/country/india/state/"
            agg_state_list = os.listdir(path)
            data = {'State': [], 'Year': [], 'Quarter': [],
                    'District': [], 'Registered_user': []}
            for i in agg_state_list:
                path_i = path + i + '/'
                agg_year_list = os.listdir(path_i)
                for j in agg_year_list:
                    path_j = path_i + j + '/'
                    agg_year_json = os.listdir(path_j)
                    for k in agg_year_json:
                        path_k = path_j + k
                        f = open(path_k, 'r')
                        d = json.load(f)
                        for z in d['data']['districts']:
                            district = z['name']
                            reg_user = z['registeredUsers']
                            data['State'].append(i)
                            data['Year'].append(j)
                            data['Quarter'].append(k[0])
                            data['District'].append(district)
                            data['Registered_user'].append(reg_user)
            return data

        except:
            pass


class data_transform:

    # transforming data related to transactions to pandas data frame
    df_aggregated_transaction = pd.DataFrame(data_extract.aggregated_transaction())
    df_aggregated_transaction["State"] = df_aggregated_transaction["State"].str.replace("andaman-&-nicobar-islands","Andaman & Nicobar")
    df_aggregated_transaction["State"] = df_aggregated_transaction["State"].str.replace("-"," ")
    df_aggregated_transaction["State"] = df_aggregated_transaction["State"].str.title()
    df_aggregated_transaction['State'] = df_aggregated_transaction['State'].str.replace("Dadra & Nagar Haveli & Daman & Diu", "Dadra and Nagar Haveli and Daman and Diu")
    
    df_map_transaction = pd.DataFrame(data_extract.map_transaction())
    df_map_transaction["State"] = df_map_transaction["State"].str.replace("andaman-&-nicobar-islands","Andaman & Nicobar")
    df_map_transaction["State"] = df_map_transaction["State"].str.replace("-"," ")
    df_map_transaction["State"] = df_map_transaction["State"].str.title()
    df_map_transaction['State'] = df_map_transaction['State'].str.replace("Dadra & Nagar Haveli & Daman & Diu", "Dadra and Nagar Haveli and Daman and Diu")
    
    df_top_transaction = pd.DataFrame(data_extract.top_transaction())
    df_top_transaction["State"] = df_top_transaction["State"].str.replace("andaman-&-nicobar-islands","Andaman & Nicobar")
    df_top_transaction["State"] = df_top_transaction["State"].str.replace("-"," ")
    df_top_transaction["State"] = df_top_transaction["State"].str.title()
    df_top_transaction['State'] = df_top_transaction['State'].str.replace("Dadra & Nagar Haveli & Daman & Diu", "Dadra and Nagar Haveli and Daman and Diu")
    
  

    # transforming data related to users to pandas data frame
    df_aggregated_users = pd.DataFrame(data_extract.aggregated_user())
    df_aggregated_users["State"] = df_aggregated_users["State"].str.replace("andaman-&-nicobar-islands","Andaman & Nicobar")
    df_aggregated_users["State"] = df_aggregated_users["State"].str.replace("-"," ")
    df_aggregated_users["State"] = df_aggregated_users["State"].str.title()
    df_aggregated_users['State'] = df_aggregated_users['State'].str.replace("Dadra & Nagar Haveli & Daman & Diu", "Dadra and Nagar Haveli and Daman and Diu")

    df_map_users = pd.DataFrame(data_extract.map_user())
    df_map_users["State"] = df_map_users["State"].str.replace("andaman-&-nicobar-islands","Andaman & Nicobar")
    df_map_users["State"] = df_map_users["State"].str.replace("-"," ")
    df_map_users["State"] = df_map_users["State"].str.title()
    df_map_users['State'] = df_map_users['State'].str.replace("Dadra & Nagar Haveli & Daman & Diu", "Dadra and Nagar Haveli and Daman and Diu")

    df_top_users = pd.DataFrame(data_extract.top_user())
    df_top_users["State"] = df_top_users["State"].str.replace("andaman-&-nicobar-islands","Andaman & Nicobar")
    df_top_users["State"] = df_top_users["State"].str.replace("-"," ")
    df_top_users["State"] = df_top_users["State"].str.title()
    df_top_users['State'] = df_top_users['State'].str.replace("Dadra & Nagar Haveli & Daman & Diu", "Dadra and Nagar Haveli and Daman and Diu")
  
    #Create csv files

    df_aggregated_transaction.to_csv('aggregated_transaction.csv',index = False)
    df_map_transaction.to_csv('map_transaction.csv',index = False)
    df_top_transaction.to_csv('top_transaction.csv',index = False)
    df_aggregated_users.to_csv('aggregated_users.csv',index = False)
    df_map_users.to_csv('map_users.csv',index = False)
    df_top_users.to_csv('top_users.csv',index = False)


    df_agg_trans = pd.read_csv('aggregated_transaction.csv')
    df_map_trans = pd.read_csv('map_transaction.csv')
    df_top_trans = pd.read_csv('top_transaction.csv')
    df_agg_users = pd.read_csv('aggregated_users.csv')
    df_map_users = pd.read_csv('map_users.csv')
    df_top_users = pd.read_csv('top_users.csv')

    #Check the null values
    print(df_agg_trans.isnull().sum())
    print()
    print(df_map_trans.isnull().sum())
    print()
    print(df_top_trans.isnull().sum())
    print()
    print(df_agg_users.isnull().sum())
    print()
    print(df_map_users.isnull().sum())
    print()
    print(df_top_users.isnull().sum())
    
    #Check the datatypes
    print(df_agg_trans.info())
    print()
    print(df_map_trans.info())
    print()
    print(df_top_trans.info())
    print()
    print(df_agg_users.info())
    print()
    print(df_map_users.info())
    print()
    print(df_top_users.info())

    print(df_agg_trans.head())
    print()
    print(df_map_trans.head())
    print()
    print(df_top_trans.head())
    print()
    print(df_agg_users.head())
    print()
    print(df_map_users.head())
    print()
    print(df_top_users.head())

    #df_agg_users['User_percentage'] = df_agg_users['User_percentage'].astype(float).round(2)

def create_sql_table():

    # table creation for transactions details
  

    # table for aggregated_transaction
    mycursor.execute("""create table if not exists aggregated_transaction(
    State    varchar(255),
    Year     int,
    Quarter  int,
    Transaction_type  varchar(255),
    Transaction_count bigint,
    Transaction_amount bigint
     )""")

    # table for map_transaction
    mycursor.execute("""create table if not exists map_transaction(
    State    varchar(255),
    Year     int,
    Quarter  int,
    District varchar(100),
    Transaction_count bigint,
    Transaction_amount bigint
    )""")

    # table for top_transaction
    mycursor.execute("""create table if not exists top_transaction(
    State    varchar(255),
    Year     int,
    Quarter  int,
    District  varchar(255),
    Transaction_count bigint,
    Transaction_amount bigint
    )""")

   

    # table creation for users details

    # table for aggregated_users
    mycursor.execute("""create table if not exists aggregated_users(
    State    varchar(255),
    Year     int,
    Quarter  int,
    User_brand  varchar(255),
    User_count bigint,
    User_percentage float
    ) """)

    # table for map_users
    mycursor.execute("""create table if not exists map_users(
    State    varchar(255),
    Year     int,
    Quarter  int,
    District  varchar(255),
    Registered_user bigint,
    App_opens bigint
    ) """)

    # table for top_users_district
    mycursor.execute("""create table if not exists top_users(
    State    varchar(255),
    Year     int,
    Quarter  int,
    District  varchar(255),
    Registered_user bigint
    ) """)


create_sql_table()


class insert_values_into_tables():

    # inserting values into aggregated_transaction table

    def insert_to_aggregated_transaction():
        data = data_transform.df_agg_trans.values.tolist()
        query = "insert into aggregated_transaction values(%s,%s,%s,%s,%s,%s)"
        for i in data:
            mycursor.execute(query, tuple(i))
        my_db.commit()

    # inserting values into map_transaction table
    def insert_to_map_transaction():
        data = data_transform.df_map_trans.values.tolist()
        query = "insert into map_transaction values(%s,%s,%s,%s,%s,%s)"
        for i in data:
            mycursor.execute(query, tuple(i))
        my_db.commit()

    # inserting values into top_transaction_district table
    def insert_to_top_transaction():
        data = data_transform.df_top_trans.values.tolist()
        query = "insert into top_transaction values(%s,%s,%s,%s,%s,%s)"
        for i in data:
            mycursor.execute(query, tuple(i))
        my_db.commit()

    # inserting values into users table

     # inserting values into aggregated users table

    def insert_to_aggregated_users():
        data = data_transform.df_agg_users.values.tolist()
        query = "insert into aggregated_users values(%s,%s,%s,%s,%s,%s)"
        for i in data:
            mycursor.execute(query, tuple(i))
        my_db.commit()

    # inserting values into  map_users table
    def insert_to_map_users():
        data = data_transform.df_map_users.values.tolist()
        query = "insert into map_users values(%s,%s,%s,%s,%s,%s)"
        for i in data:
            mycursor.execute(query, tuple(i))
        my_db.commit()

    # inserting values into  top_users table
    def insert_to_top_users():
        data = data_transform.df_top_users.values.tolist()
        query = "insert into top_users values(%s,%s,%s,%s,%s)"
        for i in data:
            mycursor.execute(query, tuple(i))
        my_db.commit()


def data_insertion_postgresql():
    try:
        insert_values_into_tables.insert_to_aggregated_transaction()
        insert_values_into_tables.insert_to_map_transaction()
        insert_values_into_tables.insert_to_top_transaction()
        insert_values_into_tables.insert_to_aggregated_users()
        insert_values_into_tables.insert_to_map_users()
        insert_values_into_tables.insert_to_top_users()
        
    except:
        pass


data_insertion_postgresql()