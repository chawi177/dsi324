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
                    st.session_state.page = "Home"  # Set page to "Home" after login
                else:
                    st.error("Incorrect email or password.")  
            else:
                st.error("Please enter both email and password.")
        else:
            st.error("Invalid email domain. Please use a valid organization email.")

# Data entry page
def data_entry_page():
    st.write("แบบรายงานผลการปฏิบัติงานอาสาสมัครสาธารณสุขกรุงเทพมหานคร ด้านการป้องกันและแก้ไขปัญหายาเสพติด")
    
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
    # Check if user is logged in
    if 'logged_in' not in st.session_state or not st.session_state.logged_in:
        login()  # Show login page if not logged in
    else:
        # Check if page state is set
        if 'page' not in st.session_state:
            st.session_state.page = "Home"  # Default to "Home" page if not set
        
        # Use sidebar for page selection
        page = st.sidebar.selectbox("Choose an option", ["Home", "Enter Data"])

        if page == "Home":
            st.session_state.page = "Home"
            st.title(f"Welcome, {st.session_state.username}!")
            st.write("You are now logged in.")
            st.write("Please select an option from the menu.")
        
        elif page == "Enter Data":
            st.session_state.page = "Enter Data"
            data_entry_page()  # Show the data entry page

if __name__ == '__main__':
    main()

# #search volenteer page
# st.set_page_config(page_title="ค้นหาอาสาสมัคร", layout="centered")

# st.markdown("## ค้นหาอาสาสมัคร")

# with st.container():
#     st.markdown("### ข้อมูลส่วนตัว")

#     col1, col2 = st.columns(2)
#     with col1:
#         volunteer_id = st.text_input("เลขประจำตัวอาสาสมัคร", value="1234567890")
#     with col2:
#         last_name = st.text_input("นามสกุล")

#     col3, col4 = st.columns(2)
#     with col3:
#         first_name = st.text_input("ชื่อ")
#     with col4:
#         st.text("")  # เพิ่มระยะห่างสำหรับไอคอนค้นหา (ไม่ได้มีผลจริง)
#         st.button("🔍", key="search_name")

#     st.markdown("### พื้นที่ที่รับผิดชอบ")

#     col5, col6, col7 = st.columns(3)
#     with col5:
#         district = st.selectbox("เขต", ["เลือกเขต", "เขตคลองหลวง", "เขตหนองจอก", "เขตบางนา"])
#     with col6:
#         community = st.selectbox("ชุมชน", ["เลือกชุมชน", "ชุมชน A", "ชุมชน B"])
#     with col7:
#         health_center = st.selectbox("ศูนย์บริการสาธารณสุข", ["เลือกศูนย์", "ศูนย์ 1", "ศูนย์ 2"])

#     st.markdown("---")
#     center_button = st.columns([3, 1, 3])[1]
#     with center_button:
#         if st.button("🔍 search"):
#             st.success("กำลังค้นหาอาสาสมัคร...")
