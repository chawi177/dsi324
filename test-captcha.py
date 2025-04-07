import streamlit as st
import mysql.connector 
from mysql.connector import Error
import google.generativeai as genai
import os
from dotenv import load_dotenv

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

# Load environment variables from .env
load_dotenv()

# Configure the API key for Google Gemini
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Create the model configuration once to be used across functions
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Create the generative model once
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    generation_config=generation_config,
)

# Function to generate CAPTCHA question using OpenAI API
def generate_captcha_question():
    
    prompt = "Create a simple but challenging CAPTCHA question that requires reasoning. Example: 'What is the next number in the series 2, 4, 6, ?'"

    # Start the chat session
    chat_session = model.start_chat(history=[])

    # Get the response from GenAI
    response = chat_session.send_message(prompt)

    question = response[0].text.strip()

    return question


# Login page with CAPTCHA
def login():
    st.title("Login to Your Account")
    
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    
    # Generate CAPTCHA question
    captcha_question = generate_captcha_question()
    user_captcha_answer = st.text_input(f"Answer the CAPTCHA question: {captcha_question}")
    
    if st.button("Login"):
        if '@dome.tu.ac.th' in email:
            if email and password and user_captcha_answer:
                if check_user_credentials(email, password):  
                    # Check if CAPTCHA is answered correctly (this part should be validated by your question's answer)
                    if user_captcha_answer.strip().lower() == "8":  # Example answer validation for "What is the next number in the series 2, 4, 6, ?"
                        st.success("Login successful!")
                        st.session_state.logged_in = True
                        st.session_state.username = email  
                        # Redirect to another page after successful login
                        st.experimental_rerun()  # This will refresh the page and trigger main()
                    else:
                        st.error("Incorrect CAPTCHA answer.")
                else:
                    st.error("Incorrect email or password.")  
            else:
                st.error("Please enter both email and password and answer the CAPTCHA.")
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
