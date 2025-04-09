import streamlit as st

# This must be the first Streamlit command
st.set_page_config(
    page_title="Volunteer Management System",  # Default title
    layout="centered"
)

# Login page (no email or password check)
def login():
    st.title("Login to Your Account")
    
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if email and password:
            # Skip database check and allow login immediately
            st.success("Login successful!")
            st.session_state.logged_in = True
            st.session_state.username = email  
            st.session_state.page = "Home"  # Set page to "Home" after login
        else:
            st.error("Please enter both email and password.")

#search volunteer page
def search_volunteer():
    st.markdown("## ค้นหาอาสาสมัคร")

    with st.container():
        st.markdown("### ข้อมูลส่วนตัว")

        col1, col2 = st.columns(2)
        with col1:
            volunteer_id = st.text_input("เลขประจำตัวอาสาสมัคร")
        with col2:
            last_name = st.text_input("นามสกุล")

        col3, col4 = st.columns(2)
        with col3:
            first_name = st.text_input("ชื่อ")
        with col4:
            st.text("")  # เพิ่มระยะห่างสำหรับไอคอนค้นหา (ไม่ได้มีผลจริง)
            st.button("🔍", key="search_name")

        st.markdown("### พื้นที่ที่รับผิดชอบ")

        col5, col6, col7 = st.columns(3)
        with col5:
            district = st.selectbox("เขต", ["เลือกเขต", "เขตคลองหลวง", "เขตหนองจอก", "เขตบางนา"])
        with col6:
            community = st.selectbox("ชุมชน", ["เลือกชุมชน", "ชุมชน A", "ชุมชน B"])
        with col7:
            health_center = st.selectbox("ศูนย์บริการสาธารณสุข", ["เลือกศูนย์", "ศูนย์ 1", "ศูนย์ 2"])

        st.markdown("---")
        center_button = st.columns([3, 1, 3])[1]
        with center_button:
            if st.button("🔍 search"):
                st.success("กำลังค้นหาอาสาสมัคร...")

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
        page = st.sidebar.selectbox("Choose an option", ["Home", "Search Volunteer", "Enter Data"])

        if page == "Home":
            st.session_state.page = "Home"
            st.title(f"Welcome, {st.session_state.username}!")
            st.write("You are now logged in.")
            st.write("Please select an option from the menu.")

        elif page == "Search Volunteer":
            st.session_state.page = "Search Volunteer"
            search_volunteer()  # Show the data Search Volunteer page
    
        elif page == "Enter Data":
            st.session_state.page = "Enter Data"
            data_entry_page()  # Show the data entry page

if __name__ == '__main__':
    main()