import streamlit as st
import pandas as pd
from datetime import datetime
import os
from streamlit.runtime.scriptrunner import get_script_run_ctx
import hashlib
st.title("** Welcome **")
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

with tab1:
    st.title("Registration for Students!!")
    Name = st.text_input("Enter your name: ", placeholder='E.g: RAAMA')
    Roll_no = st.text_input("Enter Roll Number: ", placeholder='E.g: BI')
    if st.button('Submit'):
        if Roll_no not in options:
            st.error("YOU ARE NOT A MEMBER OF CLASS")
        else:
            if st.session_state['user'] is not None and st.session_state['user'] != Roll_no:
                st.error(f"Sorry! This device is marked for {st.session_state['user']}") 
            else:
                st.success("**ACCESS GRANTED**")


with tab2:
    st.title('CSE Attendance Checker!!')
    st.header('Enter the following details:')

    role = st.radio('Select Your Role:', ['Student', 'Class Representative'])

    if role == 'Student':
        try:
            from streamlit_geolocation import streamlit_geolocation
            location = streamlit_geolocation()
        except ImportError:
            location = {}
            st.warning('streamlit_geolocation package not found. Location fetch will not work!')

        selected = st.selectbox('Who are You?', [Roll_no])
        password = st.text_input("Enter Secret Password:", type='password')

        if st.button('Mark Present?'):
            today = datetime.today().strftime('%Y-%m-%d')

            # Unique session block: Only allow the first selected name per session!
            if st.session_state['user'] is None:
                # First mark for this browser session, user selection is saved
                if passwords[selected] == password:
                    if location.get("latitude") and location.get("longitude"):
                        lat = location['latitude']
                        long = location['longitude']
                        if (lat >= 18.0180 and lat <= 18.0285) and (long >= 83.3965 and long <= 83.4041):
                            st.session_state['user'] = selected  # Save the selection in session
                            already_marked = attendance_df[
                                (attendance_df['Name'] == selected) &
                                (attendance_df['Date'] == today)
                            ]
                            if already_marked.empty:
                                data = [
                                    [st.session_state['session_id'], selected, today]
                                ]
                                new_df = pd.DataFrame(data, columns=['SessionID', 'Name', 'Date'])
                                attendance_df = pd.concat([attendance_df, new_df], ignore_index=True)
                                attendance_df.to_csv(ATTENDANCE_FILE, index=False)
                                st.success(f"You ({selected}) are now marked as present for {today}!")
                            else:
                                st.warning(f"{selected} is already marked present for {today}.")
                        else:
                            st.error("Your Location is not matching i.e you aren't there in college!!")
                    else:
                        st.error("Didn't fetch Location, try providing location once more!!")
                else:
                    st.error('WRONG PASSWORD!!')
            else:
                # Session has already a user who marked attendance 
                if st.session_state['user'] != selected:
                    st.error(f"This device/browser is already used by {st.session_state['user']}. "
                        "You cannot mark for others during this session!")
                else:
                    st.warning(f"{selected} has already marked attendance for this session.")

        if st.session_state['user'] is not None:
            if st.button("Change User"):
                # (1) Remove the last attendance row for this session, if marked
                today = datetime.today().strftime('%Y-%m-%d')
                mask = ~((attendance_df['SessionID'] == st.session_state['session_id']) & (attendance_df['Date'] == today))
                attendance_df = attendance_df[mask]
                attendance_df.to_csv(ATTENDANCE_FILE, index=False)
                
                # (2) Clear session state and assign a new session ID
                st.session_state['user'] = None
                st.session_state['session_id'] = get_session_id()
                st.success("Session released! You can select a new user and try again.")
            

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


with tab3:
      MESSAGE_FILE = "messages.csv"
      if not os.path.exists(MESSAGE_FILE):
        message_df = pd.DataFrame(columns=['Roll_no', 'Message'])
        message_df.to_csv(MESSAGE_FILE, index=False)
      else:
          message_df = pd.read_csv(MESSAGE_FILE)  
      issue = st.chat_input("Enter your issue: ")
      if Roll_no != "" and Roll_no in options:
        if issue:
            new_msg = pd.DataFrame({"Roll_no":[Roll_no],"Message":[issue]})
            message_df = pd.concat([message_df,new_msg], ignore_index=True) 
            message_df.to_csv(MESSAGE_FILE) 
      else:
          st.error("!Enter NAME and ROLL NUMBER first!")  
      for idx,row in message_df.iterrows():
          st.write(f"{row['Roll_no']}: {row['Message']}")

      if st.button("Reset"):
            message_df = pd.DataFrame(columns=message_df.columns)
            message_df.to_csv(MESSAGE_FILE, index=False)
            for idx, row in message_df.iterrows():
                st.write(f"{row['Roll_no']}: {row['Message']}")
      if st.button("REFRESH"):
          st.rerun()



