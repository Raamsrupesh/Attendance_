import streamlit as st
import pandas as pd
from datetime import datetime
import os
from streamlit.runtime.scriptrunner import get_script_run_ctx
import hashlib
import sqlite3
import uuid

DB_PATH = "attendance.sqlite"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            roll_number TEXT PRIMARY KEY,
            device_id TEXT,
            mark_date TEXT,
            mark_time TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS user_bindings (
            roll_number TEXT PRIMARY KEY,
            device_id TEXT,
            name TEXT
        )
    """)
    return conn

# Fallback: Generate a unique device ID using session context (not truly device-bound, but unique per session)
ctx = get_script_run_ctx()
if ctx and ctx.session_id:
    device_id = hashlib.sha256(ctx.session_id.encode()).hexdigest()
else:
    device_id = str(uuid.uuid4())  # Fallback UUID if no session

tab1, tab2, tab3 = st.tabs(['Register/Login', 'Student/CR', 'Ask Permission'])
# ===== Unique session ID generation function =====
def get_session_id():
    ctx = get_script_run_ctx()
    if ctx and ctx.session_id:
        return hashlib.sha256(ctx.session_id.encode()).hexdigest()
    else:
        return hashlib.sha256(str(datetime.now()).encode()).hexdigest()

# ====== Constants/Initializations ======
ATTENDANCE_FILE = 'attendance.csv'
options = [
    'X1', 'X2', 'X3', 'X4', 'X5', 'X6', 'X7', 'X8', 'X9', 'Y0', 'Y1', 'Y2', 'Y3',
    'Y4', 'Y5', 'Y6', 'Y7', 'Y8', 'Y9', 'Z0', 'Z1', 'Z2', 'Z3', 'Z4', 'Z5', 'Z6',
    'Z7', 'Z8', 'Z9', 'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'AG', 'AH', 'AI', 'AJ',
    'AK', 'AL', 'AM', 'AN', 'AO', 'AP', 'AQ', 'AR', 'AS', 'AT', 'AU', 'AV', 'AW',
    'AX', 'AY', 'AZ', 'BA', 'BB', 'BC', 'BD', 'BE', 'BF', 'BG', 'BH', 'BI', 'BJ',
    'BK', 'BL', 'BM', 'BN', 'BO', 'BP', 'BQ', 'BR', 'BS', 'BT', 'BU', 'BV', 'BW',
    'BX', 'BY', 'BZ'
]
passwords = {rn: 'In' + rn + '@123' for rn in options}
rep_password = 'REP123'

# ====== Create attendance file if needed ======
if not os.path.exists(ATTENDANCE_FILE):
    df = pd.DataFrame(columns=['SessionID', 'Name', 'Date'])
    df.to_csv(ATTENDANCE_FILE, index=False)

attendance_df = pd.read_csv(ATTENDANCE_FILE)

# ====== Initialize session context ======
if 'session_id' not in st.session_state:
    st.session_state['session_id'] = get_session_id()
if 'user' not in st.session_state:
    st.session_state['user'] = None

def is_bound_to_another_device(roll_number):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT device_id FROM user_bindings WHERE roll_number=?", (roll_number,))
    row = cur.fetchone()
    conn.close()
    if row:
        return row[0] != device_id
    return False

with tab1:
    no_of_times = 1 #First Time 
    st.title("Registration for Students!!")
    Name = st.text_input("Enter your name: ", placeholder='E.g: RAAMA')
    Roll_no = st.text_input("Enter Roll Number: ", placeholder='E.g: BI')
    if no_of_times == 1:
        st.session_state['user'] = Roll_no
        no_of_times += 1
    if st.button('Submit'):
        if Roll_no not in options:
            st.error("YOU ARE NOT A MEMBER OF CLASS")
        elif is_bound_to_another_device(Roll_no):
            st.error(f"ERROR: Roll number {Roll_no} is enrolled with another device. Access denied.")
        elif st.session_state['user'] is not None and st.session_state['user'] != Roll_no:
            st.error(f"This device is aldready bound to another Roll NO: {st.session_state['user']}!!")
        else:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("SELECT device_id FROM user_bindings WHERE roll_number=?", (Roll_no,))
            row = cur.fetchone()
            if row:
                st.success("**ACCESS GRANTED** (Already registered to this device)")
            else:
                # Bind roll number to this device
                cur.execute("INSERT INTO user_bindings (roll_number, device_id, name) VALUES (?, ?, ?)", (Roll_no, device_id, Name))
                conn.commit()
                st.success("**ACCESS GRANTED** (Registered to this device)")
            conn.close()

with tab2:
    st.title('CSE Attendance Checker!!')
    st.header('Enter the following details:')

    roll_no_tab2 = Roll_no
    if roll_no_tab2 and roll_no_tab2 in options:
        if is_bound_to_another_device(roll_no_tab2):
            st.error(f"ERROR: Roll number {roll_no_tab2} is enrolled with another device. Access denied.")
        elif st.session_state['user'] is not None and st.session_state['user'] != roll_no_tab2:
            st.error("PROVIDE **VALID DETAILS** FIRST!")
        else:
            role = st.radio('Select Your Role:', ['Student', 'Class Representative'])

            if role == 'Student':
                try:
                    from streamlit_geolocation import streamlit_geolocation
                    location = streamlit_geolocation()
                    st.write(f"📍You are at {location['latitude']} N and at {location['longitude']} E")  # Temporary debug line
                except ImportError:
                    location = {}
                    st.warning('streamlit_geolocation package not found. Location fetch will not work!')
                except Exception as e:  # Catch other errors like timeouts
                    location = {}
                    st.error(f"Error fetching location: {str(e)}. Check browser permissions.")

                selected = st.selectbox('Who are You?', [roll_no_tab2])
                password = st.text_input("Enter Secret Password:", type='password')

                if st.button('Mark Present?'):
                    today = datetime.today().strftime('%Y-%m-%d')
                    input_time = datetime.now().strftime("%H:%M:%S")

                    if st.session_state['user'] is None:
                        # First mark for this browser session, user selection is saved
                        if passwords[selected] == password:
                            if location.get("latitude") and location.get("longitude"):
                                lat = location['latitude']
                                long = location['longitude']
                                if (lat >= 18.08646 and lat <= 18.0999) and (long >= 83.37392 and long <= 83.3999):
                                    st.session_state['user'] = selected  # Save the selection in session
                                    # Device-bound check for attendance
                                    conn = get_db_connection()
                                    cur = conn.cursor()
                                    cur.execute("SELECT device_id, mark_date, mark_time FROM attendance WHERE roll_number=?", (selected,))
                                    row = cur.fetchone()
                                    if row:
                                        bound_device_id, mark_date, mark_time = row
                                        if bound_device_id != device_id:
                                            st.error(f"ERROR: Roll number {selected} already marked as present by another device on {mark_date} at {mark_time}. Multiple marks are NOT allowed.")
                                        else:
                                            st.warning(f"{selected} is already marked present (by this device).")
                                    else:
                                        # Mark attendance
                                        cur.execute("INSERT INTO attendance (roll_number, device_id, mark_date, mark_time) VALUES (?, ?, ?, ?)", (selected, device_id, today, input_time))
                                        conn.commit()
                                        # Also update CSV for compatibility
                                        already_marked = attendance_df[(attendance_df['Name'] == selected) & (attendance_df['Date'] == today)]
                                        if already_marked.empty:
                                            data = [[st.session_state['session_id'], selected, today]]
                                            new_df = pd.DataFrame(data, columns=['SessionID', 'Name', 'Date'])
                                            attendance_df = pd.concat([attendance_df, new_df], ignore_index=True)
                                            attendance_df.to_csv(ATTENDANCE_FILE, index=False)
                                        st.success(f"You ({selected}) are now marked as present for {today}!")
                                else:
                                    st.error("Your Location is not matching i.e you aren't there in college!!")
                            else:
                                st.error(f"Didn't fetch location, open settings and grant permission of accessing Loaction for this device!!")
                        else:
                            st.error('WRONG PASSWORD!!')
                    else:
                        # Session has already a user who marked attendance 
                        if st.session_state['user'] != selected:
                            st.error(f"This device/browser is already used by {st.session_state['user']}. You cannot mark for others during this session!")
                        else:
                            st.warning(f"{selected} has already marked attendance for this session.")
                # if st.session_state['user'] is not None:
                #     if st.button("Change User"):
                #         # (1) Remove the last attendance row for this session, if marked
                #         today = datetime.today().strftime('%Y-%m-%d')
                #         mask = ~((attendance_df['SessionID'] == st.session_state['session_id']) & (attendance_df['Date'] == today))
                #         attendance_df = attendance_df[mask]
                #         attendance_df.to_csv(ATTENDANCE_FILE, index=False)
                        
                #         # (2) Clear session state and assign a new session ID
                #         st.session_state['user'] = None
                #         st.session_state['session_id'] = get_session_id()
                #         st.success("Session released! You can select a new user and try again.")

            elif role == 'Class Representative':
                rep_pass = st.text_input("Enter Rep Password:", type='password')
                selected_date = st.date_input("Select Date to View Attendance:", value=datetime.today())
                selected_date_str = selected_date.strftime('%Y-%m-%d')

                if st.button('View Attendance'):
                    if rep_pass == rep_password:
                        daily_attendance = attendance_df[attendance_df['Date'] == selected_date_str]
                        present_list = daily_attendance['Name'].tolist()
                        absent_list = [name for name in options if name not in present_list]

                        st.subheader(f'Attendance for {selected_date_str}:')
                        col1, col2, col3 = st.columns([1, 2, 1])
                        with col2:
                            cola, colb = st.columns(2)
                            with cola:
                                st.write('**Presenties:**')
                                if present_list:
                                    for name in present_list:
                                        st.write(f"- {name}")
                                else:
                                    st.write("No one present.")
                            with colb:
                                st.write('**Absenties:**')
                                if absent_list:
                                    for name in absent_list:
                                        st.write(f"- {name}")
                                else:
                                    st.write("Everyone present!")
                    else:
                        st.error('Wrong Rep Password!')

                if st.button('Reset Attendance for Selected Date') and rep_pass == rep_password:
                    attendance_df = attendance_df[attendance_df['Date'] != selected_date_str]
                    attendance_df.to_csv(ATTENDANCE_FILE, index=False)
                    st.info(f"Attendance reset for {selected_date_str}!")
    else:
        st.error("Please enter a valid roll number.")

#======================= Chat Arrangement ======================== 
import html  # For basic sanitization

st.markdown("""
<link rel="stylesheet"
      href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">

<style>
.chat-container {
    display: flex;
    flex-direction: column;
    gap: 10px;
    margin-top: 20px;
    max-width: 100%;
    width: 100%;
    margin-bottom:20px;
}

.chat-bubble {
    padding: 10px 15px;
    border-radius: 15px;
    max-width: 70%;
    word-wrap: break-word;
    font-size: 16px;
}

.left-bubble {
    align-self: flex-start;
    background-color: #dcf8c6; /* light green */
    color: black;
    border-top-left-radius: 0;
    text-align: left;
}

.right-bubble {
    align-self: flex-end;
    background-color: #add8e6; /* light blue */
    color: black;
    border-top-right-radius: 0;
    text-align: right;
}
</style>
""", unsafe_allow_html=True)

with tab3:
    roll_no_tab3 = Roll_no
    if roll_no_tab3 and roll_no_tab3 in options:
        if is_bound_to_another_device(roll_no_tab3):
            st.error(f"ERROR: Roll number {roll_no_tab3} is enrolled with another device. Access denied.")
        elif st.session_state['user'] is not None and roll_no_tab3 != st.session_state['user']:
            st.error("Provide the Valid Roll NO first!")
        else:
            MESSAGE_FILE = "messages.csv"
            if not os.path.exists(MESSAGE_FILE):
                message_df = pd.DataFrame(columns=['Roll_no', 'Message'])
                message_df.to_csv(MESSAGE_FILE, index=False)
            else:
                message_df = pd.read_csv(MESSAGE_FILE)
            
            issue = st.chat_input("Enter your issue: ")
            if issue:
                # Sanitize input to prevent HTML injection
                sanitized_issue = html.escape(issue)
                new_msg = pd.DataFrame({"Roll_no": [roll_no_tab3], "Message": [sanitized_issue]})
                message_df = pd.concat([message_df, new_msg], ignore_index=True)
                message_df.to_csv(MESSAGE_FILE, index=False)
            
            # Sort by index for chronological order (assuming index represents time)
            message_df = message_df.sort_index()
            
            # Build the entire chat HTML in one go
            chat_html = "<div class='chat-container'>"
            for idx, row in message_df.iterrows():
                sanitized_roll = html.escape(str(row['Roll_no']))
                sanitized_msg = html.escape(str(row['Message']))
                if row['Roll_no'] == roll_no_tab3:
                    chat_html += f"<div class='chat-bubble left-bubble'><b>{sanitized_roll}</b>: {sanitized_msg}</div>"
                else:
                    chat_html += f"<div class='chat-bubble right-bubble'><b>{sanitized_roll}</b>: {sanitized_msg}</div>"
            chat_html += "</div>"
            st.markdown(chat_html, unsafe_allow_html=True)
            
            if st.button("Reset"):
                message_df = pd.DataFrame(columns=message_df.columns)
                message_df.to_csv(MESSAGE_FILE, index=False)
                st.rerun()
                

            if st.button("REFRESH"):
                st.rerun()
    else:
        st.error("Please enter a valid roll number.")
st.caption(f"Device ID: {device_id}")




