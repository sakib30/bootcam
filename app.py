import mysql.connector as mysql
import pandas as pd
import time
from datetime import datetime
from PIL import Image
import json
import base64
import yagmail
import re
from re import search
import smtplib
 
import streamlit as st
import streamlit.components.v1 as components
from streamlit import caching
 
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
from sqlalchemy import create_engine
from mysql.connector.constants import ClientFlag
from uuid import uuid4
import yaml
from db_connection import get_database_connection

import yaml
import mysql.connector as mysql
from mysql.connector.constants import ClientFlag
from sqlalchemy import create_engine


with open('credintials.yml', 'r') as f:
    credintials = yaml.load(f, Loader=yaml.FullLoader)
    db_credintials = credintials['db']
    system_pass = credintials['system_pass']['admin']
    # email_sender = credintials['email_sender']


def get_database_connection():
    db = mysql.connect(host = db_credintials['host'],
                      user = db_credintials['user'],
                      passwd = db_credintials['passwd'],
                      database = db_credintials['database'],
                      auth_plugin= db_credintials['auth_plugin'])
    cursor = db.cursor()

    return cursor, db

st.set_page_config(
    page_title="Admission Form",
    page_icon=":smiley:",
    # layout="wide",
    initial_sidebar_state="expanded",
)
# database localhost connection
# @st.cache()

# def get_database_connection():
#     db = mysql.connect(host = "localhost",
#                       user = "root",
#                       passwd = "root",
#                       database = "mydatabase",
#                       auth_plugin='mysql_native_password')
#     cursor = db.cursor()
#     return cursor, db
 
cursor, db = get_database_connection()
 
cursor.execute("SHOW DATABASES")
 
databases = cursor.fetchall() ## it returns a list of all databases present
 
# st.write(databases)
# cursor.execute('''CREATE TABLE information (id varchar(255),
#                                                studentname varchar(255),
 
#                                                re_date date,
# 												status varchar(255))''')
# cursor.execute("Select * from information")
tables = cursor.fetchall()

def admin():
    username=st.sidebar.text_input('Username',key='user')
    password=st.sidebar.text_input('Password',type='password',key='pass')
    st.session_state.login=st.sidebar.checkbox('Login')
 
    if st.session_state.login==True:
        if username=="sakib" and password=='lagbena':
            st.sidebar.success('Login Success')

            date1=st.date_input('Date1')
            date2=st.date_input('Date2')
            cursor.execute(f"select * from information where re_date between '{date1}' and '{date2}'")
            # db.commit()
            tables =cursor.fetchall()
            # st.write(tables)
            for i in tables:
                with st.expander(i[1]):
                    st.write('Name : ',i[1])
                    st.write('Registration Date : ',i[2])
                    st.write('ID : ',i[0])
                    st.write('Status : ',i[4])
                    if i[4]=='In Progress':
                        Accept=st.button('Accept',key=i[0])
                        if Accept:
                            st.write('Accepted')
                            cursor.execute(f"Update information set status='Accepted' where id='{i[0]}'")
                            db.commit()
                            
                        Reject=st.button('Reject',key=i[0])
                        if Reject:
                            st.write('Rejected')
                            cursor.execute(f"Update information set status='Rejected' where id='{i[0]}'")
                            db.commit()

        else:
            st.sidebar.warning('Wrong Credintials')


def form():
    id=uuid4()
    id=str(id)[:10]
    with st.form(key='member form'):
        sname=st.text_input('Student Name')
        re_date=st.date_input('Registration Date')
        status='In Progress'
        if st.form_submit_button('Submit'):
            query = f'''INSERT INTO information (id,studentname,
                                                re_date,status) VALUES ('{id}','{sname}',
                                                '{re_date}','{status}')'''
            cursor.execute(query)
            db.commit()
            st.success(f'Congratulation *{sname}*! You have successfully Registered')
            st.code(id)
            st.warning("Please Store this code!!!")
        
# def info():
#     id=st.text_input('Your Code')
#     Submit=st.button(label='Search')
#     if Submit:
#     	cursor.execute(
#             f"select * from information where
#              id='{id}'")
#     	tables = cursor.fetchall()
#         st.info(f'Your status is : *{tables[0][2]}*')
        

def stat():
    id=st.text_input('Your Id')
    submit=st.button('Search',key='sub')
    if submit:
        cursor.execute(f"Select status from information where id='{id}'")
        table=cursor.fetchall()
        # st.write(table)
        st.info(f'Your status : *{table[0][0]}*')


def main():
    st.title('Diploma in Data Science Admission')
    st.write('Daffodil International University')
    selected=st.sidebar.selectbox('Select',
                        ('-----------',
                        'Admin',
                        'Registration',
                        'Status',
                        # 'Information'
                        ))
    if selected=='Admin':
        admin()
    elif selected=='Registration':
        form()
    elif selected=='Status':
        stat()
   # elif selected=='Information':
   #   st.write("hi")
if __name__=='__main__':
    main()
