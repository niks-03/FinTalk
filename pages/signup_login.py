import streamlit as st
from pages.Cipher_1 import login_user, register_user  #make comment while page testing 
#from Cipher_1 import login_user, register_user       #make comment while app testing
from pages.chat import get_user

import re
from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/nikhil_db')
db = client['chatbot']
user_collection = db["users"]

def password_is_valid(password):
    if len(password) < 8 or len(password) > 100:
        return "Password must be between 8 and 100 characters."
    if not re.search("[a-z]", password):
        return "Password must contain at least one lowercase letter."
    if not re.search("[A-Z]", password):
        return "Password must contain at least one uppercase letter."
    if not re.search("[0-9]", password):
        return "Password must contain at least one digit."
    if not re.search("[@#$%^&+=!]", password):
        return "Password must contain at least one special character."
    return None


def login():
    flag = 0
    st.header("Login here!")
    with st.form("login_form"):
        mail = st.text_input("Enter your email", placeholder="ex: test@gmail.com")
        password = st.text_input("Enter your password", placeholder="must be minimum 8 characters", type="password")
        st.checkbox("Remember Me!")
        login_btn = st.form_submit_button("Login")

        if login_btn:
            response = login_user(mail.lower(), password)

            if response == True:
                st.success("Login successfully")
                get_user(mail.lower())
                flag = 1
            elif response == False:
                st.warning("Invalid Password or email")
            else :
                st.warning("user not found")
            #check_authorization(mail, password)
    return flag

                

def signup():
    flag = 0
    st.header("Sign Up here!")
    with st.form("signup_form"):
        mail = st.text_input("Enter your email", placeholder="ex: test@gmail.com")
        password = st.text_input("Enter your password", placeholder="must be minimum 8 characters", type="password")
        confirm_password = st.text_input("Confirm Password", placeholder="Re-enter password", type="password")
        signup_btn = st.form_submit_button("Sign Up")

        if signup_btn:
            if mail:
                # if len(password)<8 or len(confirm_password)<8:
                #     st.warning("Password must be 8 characters")
                password_check = password_is_valid(password)
                if password_check:
                    st.warning(password_check)

                elif password == confirm_password:
                    if user_collection.count_documents({"user_id": mail}) == 0:
                        register_user(mail.lower(), password)
                        st.success("Sign up successful!")
                        get_user(mail.lower())
                        flag = 1

                    else:
                        st.warning("User with this mail is already present")

                else:
                    st.warning("Passwords do not match. Please recheck your password")
            else:
                st.warning("Please provide an email")
    return flag


#login()
#signup()