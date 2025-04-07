import streamlit as st
import mysql.connector 
from mysql.connector import Error

# Function to connect to the database
def connect_db():
    try:
        conn = mysql.connector.connect(
            host="mysql",  
            user="root",  
            password="1234",  
            database="test324"  
        )
        if conn.is_connected():
            print("Connected to MySQL database")
        return conn
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None

# Function to check user credentials
def check_user_credentials(email, password):
    conn = connect_db()
    if conn is None:
        return False
    
    try:
        cursor = conn.cursor()
        query = "SELECT password_hash FROM users WHERE email = %s"
        cursor.execute(query, (email,))
        result = cursor.fetchone()  
        if result is None:
            return False  
        stored_password_hash = result[0]  
        if stored_password_hash == password:
            return True  
        return False  
    except Error as e:
        print(f"Error while checking credentials: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

# Login page
def login():
    st.title("Login to Your Account")
    
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if '@dome.tu.ac.th' in email:
            if email and password:
                if check_user_credentials(email, password):  
                    st.success("Login successful!")
                    st.session_state.logged_in = True
                    st.session_state.username = email  
                    # Redirect to another page after successful login
                    st.experimental_rerun()  # This will refresh the page and trigger main()
                else:
                    st.error("Incorrect email or password.")  
            else:
                st.error("Please enter both email and password.")
        else:
            st.error("Invalid email domain. Please use a valid organization email.")

# Data entry page
def data_entry_page():
    st.title("Enter Your Information")
    
    # Create input fields for data entry
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=0)
    address = st.text_area("Address")
    
    if st.button("Submit"):
        if name and age and address:
            st.success(f"Data submitted successfully! {name}, {age}, {address}")
        else:
            st.error("Please fill out all fields.")

# Main function to control navigation
def main():
    if 'logged_in' not in st.session_state or not st.session_state.logged_in:
        login()  
    else:
        # If logged in, show a page selection menu
        page = st.selectbox("Select a page", ["Home", "Enter Data"])
        
        if page == "Home":
            st.title(f"Welcome, {st.session_state.username}!")
            st.write("You are now logged in.")
            st.write("Please select an option from the menu.")
        
        elif page == "Enter Data":
            data_entry_page()  # Show the data entry page

if __name__ == '__main__':
    main()
