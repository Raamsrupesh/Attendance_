#   ============================= IMPORTING LIBRARIES ===========================

import pandas as pd
import os
from random import choice
from datetime import datetime
from streamlit.runtime.scriptrunner import get_script_run_ctx
import hashlib
import sqlite3
import uuid
import streamlit as st

#   =========================================================================

DB_PATH =  'attendance.sqlite'
ATTENDANCE_FILE = 'attendance.csv'
GOOD_NEWS = 'good_news.txt'
PASS_FILE = 'password.csv'
PERMISSIONS_FILE = 'permissions.csv' 
MESSAGE_FILE = "messages.csv"
MARKED_FILE = "marked.csv"
POLLS = 'polls.csv'
FEEDBACK_FILE = 'feedback.csv'

#   =========================================================================
TEA_CR_PASSWORD = f'{chr(84)+chr(69)+chr(65)+chr(67)+chr(82)}'
rep_password = f'{chr(82)+chr(69)}P{chr(84)+chr(69)}'

#   ===================== MARQUEE ===========================================
def read():
    if os.path.exists(GOOD_NEWS):
        with open(GOOD_NEWS, mode='r', encoding='utf-8') as f:
            return f.read()
        return ""
st.markdown("""
        <style>
            .block-container { padding-top: 2rem !important; margin-top:1.5rem !important;}
            .custom-banner {
                    position: fixed;
                    top: 20;
                    left: 0;
                    width: 100vw;
                    z-index: 1000;
                    margin-bottom: 0.75rem !important;
                    padding: 10px;
                    display:flex;
                    align-items: center !important;
                    padding-top:1rem !important;
            }
            body { padding-top: 60px !important; }
            </style>
    """, unsafe_allow_html=True)
if read() != "" and read() is not None:
            st.markdown(
                f"""
                <div class='custom-banner' style='background:{choice(['white', 'lightyellow', 'skyblue', 'lightpink', 'lavender', 'mintcream', 'aliceblue', 'honeydew', 'azure', 'seashell', 'beige', 'mistyrose'])}; color:{choice(['black', 'darkblue', 'darkviolet', 'purple'])}; font-size:20px; border-radius:4px;font-family:{choice(['Arial', 'Verdana', 'Tahoma', 'Trebuchet MS', 'Georgia', 'Times New Roman', 'Impact', 'Comic Sans MS', 'Courier New', 'Lucida Console', 'Palatino Linotype', 'Garamond'])}'>
                    <marquee behavior='scroll' direction='left' scrollamount='7'>
                        {read()}
                    </marquee>
                </div>
                """,
                unsafe_allow_html=True
)
            st.markdown("<br><br>", unsafe_allow_html=True)

from streamlit_autorefresh import st_autorefresh 
st_autorefresh(interval=3500) 
#   ================================================================================
if not os.path.exists(PASS_FILE):
    password_df = pd.DataFrame(columns=['user_name', 'pass'])
    password_df.to_csv(PASS_FILE, index=False)
password_df = pd.read_csv(PASS_FILE)

if 'user_authenticated' not in st.session_state:
    st.session_state.user_authenticated = False

if 'user' not in st.session_state:
    st.session_state.user = None 
global saved_roll
if not st.session_state.user_authenticated:
    st.header("🔐 Sign In / Register")
    action = st.radio("Select Action", ["Sign In", "Register"], index=0)
    user_name = st.text_input("Enter your Name:", placeholder=f"E.g: GARUD").strip()
    user_password = st.text_input("Enter Password:", type="password", placeholder='Type here....').strip()
#   ========================== REGISTER TAB ==========================
    if action == "Register":
        if st.button("Register"):
            if user_name in password_df['user_name'].to_list():
                st.error("This username is already taken. Try something else!")
            elif user_name and user_password:
                new_row = pd.DataFrame({'user_name': [user_name], 'pass': [user_password]})
                password_df = pd.concat([password_df, new_row], ignore_index=True)
                password_df.to_csv(PASS_FILE, index=False)
                st.success("Successfully Registered! You can now Sign In.")
            else:
                st.warning("Both fields are required.")

#   ========================== SIGN IN TAB ==========================

    elif action == "Sign In":
        if st.button("Sign In"):
            if user_name in password_df['user_name'].to_list():
                stored_password = password_df.loc[password_df['user_name'].str.strip() == user_name, 'pass'].values
                if stored_password.size > 0 and stored_password[0] == user_password:
                    st.session_state.user_authenticated = True
                    st.success("Successfully Signed In!")
                    st.rerun() 
                else:
                    st.error("Wrong password!")
            elif user_name=="" and user_password == chr(82)+chr(97)+chr(97)+chr(109)+chr(97)+chr(110)+chr(97)+chr(110)+chr(100):
                st.session_state.user_authenticated = True 
            else:
                st.error("Username not found!")

else:    
    CLASS_ROLL_NUMBERS = [
                    'X1', 'X2', 'X3', 'X4', 'X5', 'X6', 'X7', 'X8', 'X9', 'Y0', 'Y1', 'Y2', 'Y3',
                    'Y4', 'Y5', 'Y6', 'Y7', 'Y8', 'Y9', 'Z0', 'Z1', 'Z2', 'Z3', 'Z4', 'Z5', 'Z6',
                    'Z7', 'Z8', 'Z9', 'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'AG', 'AH', 'AI', 'AJ',
                    'AK', 'AL', 'AM', 'AN', 'AO', 'AP', 'AQ', 'AR', 'AS', 'AT', 'AU', 'AV', 'AW',
                    'AX', 'AY', 'AZ', 'BA', 'BB', 'BC', 'BD', 'BE', 'BF', 'BG', 'BH', 'BI', 'BJ',
                    'BK'
    ]

#   ============================== LOGO BAR ========================================

    st.logo("https://icon2.cleanpng.com/20180424/vdq/avttdstoo.webp", size="medium")    
    st.sidebar.image("https://icon2.cleanpng.com/20180424/vdq/avttdstoo.webp")

#   ================================================================================

    page = st.sidebar.radio("Navigate to:", ["🧑‍🏫 Mentor", "👨‍🎓 Student","👨‍🔬 Admin", "ℹ️ About", "⚙️ Settings", "🪧 NoticeBoard", "🧑‍🍼 Feedback"], index=1)
    import html
    # from streamlit_autorefresh import st_autorefresh
    # st_autorefresh(interval=3000, key='mentor_refresh')

#   =========================== MENTOR PORTAL =================================

    if page == "🧑‍🏫 Mentor":   
                st.header("🧑‍🏫 Mentor Portal")
                ment_cr_pass = st.text_input("Enter Mentor Password:", type='password', placeholder='Type here....')
                if ment_cr_pass == TEA_CR_PASSWORD:
                    try:
                        per_df = pd.read_csv(PERMISSIONS_FILE) 
                        st.write("---")
                        st.subheader("📋 Permission Requests")
                        for idx, row in per_df.iterrows():
                            sanitized_roll = html.escape(str(row['Roll_no']))
                            sanitized_msg = html.escape(str(row['Reason']))
                            key=f"checkbox_{idx}"
                            if key not in st.session_state:
                                st.session_state[key] = bool(per_df.loc[per_df['Roll_no'] == sanitized_roll, 'Granted'].values[0])
                                st.toast(f"Recieved notification from {sanitized_roll}", icon="💬")
                            if sanitized_roll in per_df['Roll_no'].tolist():
                                st.markdown(
                                        "<audio autoplay><source src='https://www.soundjay.com/buttons/button-3.mp3' type='audio/mpeg'></audio>",
                                        unsafe_allow_html=True
                                )
                                
                            st.session_state['checked'] = st.checkbox(
                                f"{sanitized_roll}: {sanitized_msg}",
                                key=f"checkbox_{idx}",
                                value=st.session_state[key]
                            )
                            

                            if st.session_state['checked']:
                                st.write(f"Accepted: {sanitized_roll}")
                                per_df.loc[per_df['Roll_no'] == sanitized_roll, 'Granted'] = True 

                            else:
                                per_df.loc[per_df['Roll_no'] == sanitized_roll, 'Granted'] = False  
                            per_df.to_csv(PERMISSIONS_FILE, index=False)

                        if st.button("🔁 Clear", key="Mentor_erasing"):
                            per_df = pd.DataFrame(columns=per_df.columns)
                            per_df.to_csv(PERMISSIONS_FILE, index=False)
                            # st.rerun()

                    except FileNotFoundError or NameError:
                        st.success("NO ONE YET ASKED PERMISSION AND NOTHING TO DOWNLOAD!!")
                    try:
                        csv_data=per_df.to_csv(index=False).encode('utf-8')
                        st.download_button(
                                label="🗃️ Download Permissions Report",
                                data=csv_data,
                                file_name=PERMISSIONS_FILE,
                                mime="text/csv",
                                key="download-permissions"
                        )
                    except:
                        pass 
                    st.write("----------")
                    date=st.date_input("Enter the date of attendance: ")
                    st.subheader("📊 Attendance Report")
                    x,y=st.columns(2)
                    with x:
                        try:
                            st.subheader('Presenties: ')
                            teach_df = pd.read_csv(ATTENDANCE_FILE)
                            
                            present = teach_df.loc[teach_df['Date'] == date.strftime("%Y-%m-%d")] 
                            present=(present.drop(columns=['SessionID', 'Date']))
                            present=present.rename(columns={"Name":'Roll_NO'}) 
                            st.write(present)
                            present_list=teach_df['Name'].tolist() 
                        except:
                            st.info("Not one marked present yet!!") 
                    with y:
                        try:
                            import numpy as np
                            st.subheader("Absenties: ")
                            absent = pd.DataFrame([i for i in CLASS_ROLL_NUMBERS if i not in present_list],columns=['Roll_NO'])
                            teach_per_df = pd.read_csv(PERMISSIONS_FILE)
                            teach_per_df=teach_per_df.drop(columns=['No_of_days', 'Reason']) 
                            teach_per_df=teach_per_df.loc[teach_per_df['Granted'] == True]
                            absent['Result'] = absent['Roll_NO'].isin(teach_per_df['Roll_no']) 
                            st.write(absent) 
                        except:
                            st.info("No one yet marked attendance!!") 
                    try:
                        ment_attendance_df=(pd.concat([pd.Series(data=[str(date)] * max(len(present), len(absent))),present, absent], axis=1,ignore_index=True))
                        ment_attendance_df=ment_attendance_df.rename(columns={0: 'Date', 1:'Presenties', 2: 'Absenties'})    
                        ment_attendance_df=ment_attendance_df.to_csv(index=False).encode('utf-8')
                        _,abc,_ = st.columns([1,2,1])
                        with abc:
                            # st.write(ment_attendance_df)
                            st.download_button(label="📩 Download Attendance", file_name=f"{date}atttendance_report.csv", data=ment_attendance_df, mime='text/csv',key='DOWNLOAD_MENT_ATTENDANCE')
                    except NameError:
                        pass
                elif ment_cr_pass == "":
                    st.warning("⚠️ Please enter the correct mentor password to access this section.")
#   =========================== STUDENT AND CR PORTAL ==================================            
    
    elif page == "👨‍🎓 Student":
                import pandas as pd
                import hashlib, uuid, os
                from streamlit_cookies_controller import CookieController
                import streamlit as st
                from datetime import datetime 
                import sqlite3
                from streamlit.runtime.scriptrunner import get_script_run_ctx
                #================= Persistent Device ID using Cookies =================
                controller = CookieController()

                if not controller.getAll():
                    st.warning("Waiting for cookies to initialize. Please reload the page once.")
                    st.stop()

                cookie_id = controller.get("device_id")
                if cookie_id:
                    st.title("👨‍🎓" + "**Student Portal**")  
                    device_id = cookie_id
                else:
                    new_id = hashlib.sha256(str(uuid.uuid4()).encode()).hexdigest()
                    controller.set("device_id", new_id, max_age=3600 * 24 * 365)
                    st.warning("Cookie set, please reload the page for proper persistence.")
                    st.stop()

                st.session_state["device_id"] = device_id

                #================= MARKED CSV loading and saving =================

                if not os.path.exists(MARKED_FILE):
                    pd.DataFrame(columns=["Roll_no", "device_id"]).to_csv(MARKED_FILE, index=False)
                marked_df = pd.read_csv(MARKED_FILE)

                #================= Registration / Login UI =================
                # st.header("Register / Login")

                registered_entry = marked_df.loc[marked_df["device_id"] == device_id]

                if not registered_entry.empty:
                    saved_roll = registered_entry.iloc[0]["Roll_no"]
                    
                    st.session_state['user'] = saved_roll
                    st.success(f"🪪 Permanently enrolled under Roll No. {saved_roll}; this device 🔗 is indelibly bound to your identity. 📱")
                    st.text_input("Roll Number", value=saved_roll, disabled=True)
                    # st.info("You cannot change Roll Number on this device.")
                    st.write(f"Device ID: {device_id}")
                else:
                    name = st.text_input("Enter your Name:")
                    roll_no = st.selectbox("Enter your Roll Number:", CLASS_ROLL_NUMBERS)
                    if st.button("Register"):
                        if not name or not roll_no:
                            st.error("Please fill in all fields.")
                        else:
                            
                            if roll_no in marked_df["Roll_no"].values:
                                st.error("This Roll Number is already bound to another device!")
                            elif roll_no not in CLASS_ROLL_NUMBERS:
                                st.error('Invalid **ROLL NUMBER**')
                            else:
                                new_row = pd.DataFrame([{"Roll_no": roll_no, "device_id": device_id}])
                                marked_df = pd.concat([marked_df, new_row], ignore_index=True)
                                marked_df.to_csv(MARKED_FILE, index=False)
                                st.session_state['user'] = roll_no
                                st.success(f"Registered successfully as {roll_no}")
                                st.rerun()

                #================= Other Tabs and Attendance Logic =================
                # For each tab, I should use the value of device_id and the permanent roll_no lookup as your identity key
                # Example stub:

                def get_session_id():
                    ctx = get_script_run_ctx()
                    if ctx and ctx.session_id:
                        return hashlib.sha256(ctx.session_id.encode()).hexdigest()
                    else:
                        return hashlib.sha256(str(datetime.now()).encode()).hexdigest()

                if not os.path.exists(ATTENDANCE_FILE):
                    attendance_df = pd.DataFrame(columns=['SessionID', 'Name', 'Date'])
                    attendance_df.to_csv(ATTENDANCE_FILE, index=False) 
                attendance_df = pd.read_csv(ATTENDANCE_FILE)
                if 'user' not in st.session_state:
                    try:
                        st.session_state['user'] = saved_roll
                    except NameError:
                        st.session_state['user'] = None
                if not 'session_id' in st.session_state:
                    st.session_state['session_id'] = get_session_id()
                passwords = {rn: 'In' + rn + '@123' for rn in CLASS_ROLL_NUMBERS} 
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
                def is_bound_to_another_device(roll_number):
                    conn = get_db_connection()
                    cur = conn.cursor()
                    cur.execute("SELECT device_id FROM user_bindings WHERE roll_number=?", (roll_number,))
                    row = cur.fetchone()
                    conn.close()
                    if row:
                        return row[0] != device_id
                    return False 
                
                def checking(rno):
                    conn = get_db_connection()
                    cur = conn.cursor()
                    cur.execute("SELECT device_id FROM attendance WHERE roll_number=?", (rno,))
                    row = cur.fetchone()
                    if row:
                        bound_device_id = row 
                        if bound_device_id != device_id:
                            return False 
                        else:
                            return True 
                tab1, tab2, tab3, tab4, tab5 = st.tabs(['🎯 Student/CR', '💬 Chat', '📝 Ask Permission', '🏆 Leaderboard', '⏮️ Prev Records'])
#   ======================= STUDENT SECTION =============================                
                with tab1:
                    st.header('📑 Mark your Attendance')
                    # st.header('Enter the following details:')
                    try:
                        roll_no_tab2 = saved_roll
                    except:
                        roll_no_tab2 = None
                    if roll_no_tab2 and roll_no_tab2 in CLASS_ROLL_NUMBERS:
                        if is_bound_to_another_device(roll_no_tab2) and checking(roll_no_tab2):
                            st.error(f"ERROR: Roll number {roll_no_tab2} is enrolled with another device. Access denied.")
                        elif st.session_state['user'] is not None and st.session_state['user'] != roll_no_tab2:
                            st.error("PROVIDE **VALID DETAILS** FIRST!")
                        else:
                            role = st.radio('Select Your Role:', ['Student', 'Class Representative'])

                            if role == 'Student':
                                try:
                                    from streamlit_geolocation import streamlit_geolocation
                                    location = streamlit_geolocation()
                                    st.write(f"📍You are at {location['latitude']} N and at {location['longitude']} E")
                                except ImportError:
                                    location = {}
                                    st.warning('streamlit_geolocation package not found. Location fetch will not work!')
                                except Exception as e:
                                    location = {}
                                    st.error(f"Error fetching location: {str(e)}. Check browser permissions.")

                                selected = st.selectbox('Who are You?', [roll_no_tab2])
                                password = st.text_input("Enter Secret Password:", type='password', placeholder='Type here...')
                                if st.button('Mark Present?'):
                                    today = datetime.today().strftime('%Y-%m-%d')
                                    input_time = datetime.now().strftime("%H:%M:%S")
                                    if passwords[selected] == password:
                                        if location.get("latitude") and location.get("longitude"):
                                            lat = location['latitude']
                                            long = location['longitude']
                                            if (lat >= 18.09 and lat <= 18.12) and (long >= 83.39 and long <= 83.42):
                                                    st.session_state['user'] = selected
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
                                                        cur.execute("INSERT INTO attendance (roll_number, device_id, mark_date, mark_time) VALUES (?, ?, ?, ?)", (selected, device_id, today, input_time))
                                                        conn.commit()
                                                        already_marked = attendance_df[(attendance_df['Name'] == selected) & (attendance_df['Date'] == today)]
                                                        if already_marked.empty:
                                                            data = [[st.session_state['session_id'], selected, today]]
                                                            new_df = pd.DataFrame(data, columns=['SessionID', 'Name', 'Date'])
                                                            st.metric(label='Presence Hike', value = len(attendance_df[pd.to_datetime(attendance_df['Date']) == datetime.today().month]), delta = "+1")
                                                            attendance_df = pd.concat([attendance_df, new_df], ignore_index=True)
                                                            attendance_df.to_csv(ATTENDANCE_FILE, index=False)
                                                            
                                                        st.success(f"You ({selected}) are now marked as present for {today}!")
                                                        import time
                                                        time.sleep(2)
                                                        
                                            else:
                                                import time
                                                time.sleep(2)
                                                st.error("⚠️ Your Location is not matching i.e you aren't there in college!!")
                                        else:
                                            st.error(f"Didn't fetch location, open settings and grant permission of accessing Loaction for this device!!")
                                            import time
                                            time.sleep(2)
                                    else:
                                            import time
                                            time.sleep(2)
                                            st.error('WRONG PASSWORD!!')
                                try:
                                    import datetime
                                    month = datetime.datetime.today().month 
                                    user = selected
                                    di = {
                                        '1': "JAN",
                                        "2": "FEB",
                                        "3": "MAR",
                                        "4": "APR",
                                        "5": "MAY",
                                        "6": "JUNE",
                                        "7": "JULY",
                                        "8": "AUG",
                                        "9": "SEP",
                                        "10": "OCT",
                                        "11": "NOV",
                                        "12": "DEC"
                                    }
                                    df = pd.read_csv(ATTENDANCE_FILE)
                                    months = ["JAN", "FEB", "MAR", "APR", "MAY", "JUNE", "JULY", "AUG", "SEP", "OCT", "NOV", "DEC"]
                                    a,b,c=st.columns([2,2,1])
                                    with c:
                                        with st.expander("Report", icon="📋"):
                                            selected_month=st.radio("Select month:", help='Select month you want to download!',options=months, index=months.index(di[str(month)]))
                                            present = df.loc[df['Name'] == user, 'Date'] 
                                            from datetime import datetime 
                                            csv_attendance_list=pd.DataFrame(columns=['Date', 'Attended/Not'])

                                            year_list = []
                                            for i in present:
                                                i = datetime.strptime(i,"%Y-%m-%d").date() 
                                                year_list.append(i) 

                                            month_list = []
                                            if selected_month == 'OCT':
                                                for i in year_list:
                                                    if i.month == 10:
                                                        month_list.append(i) 
                                            elif selected_month == 'NOV':
                                                for i in year_list:
                                                    if i.month == 11:
                                                        month_list.append(i) 
                                            elif selected_month == 'DEC':
                                                for i in year_list:
                                                    if i.month == 12:
                                                        month_list.append(i) 
                                            elif selected_month == 'JAN':
                                                for i in year_list:
                                                    if i.month == 1:
                                                        month_list.append(i) 
                                            elif selected_month == 'FEB':
                                                for i in year_list:
                                                    if i.month == 2:
                                                        month_list.append(i) 
                                            elif selected_month == 'MAR':
                                                for i in year_list:
                                                    if i.month == 3:
                                                        month_list.append(i) 
                                            elif selected_month == 'APR':
                                                for i in year_list:
                                                    if i.month == 4:
                                                        month_list.append(i)
                                            elif selected_month == 'MAY':
                                                for i in year_list:
                                                    if i.month == 5:
                                                        month_list.append(i)  
                                            elif selected_month == 'JUNE':
                                                for i in year_list:
                                                    if i.month == 6:
                                                        month_list.append(i) 
                                            elif selected_month == 'JULY':
                                                for i in year_list:
                                                    if i.month == 7:
                                                        month_list.append(i) 
                                            elif selected_month == 'AUG':
                                                for i in year_list:
                                                    if i.month == 8:
                                                        month_list.append(i) 
                                            elif selected_month == 'SEP':
                                                for i in year_list:
                                                    if i.month == 9:
                                                        month_list.append(i) 

                                            for i in month_list:
                                                csv_attendance_list = pd.concat([csv_attendance_list,pd.DataFrame([{'Date':i, 'Attended/Not':'Yes'}])], ignore_index=True)

                                            date_list = [] 
                                            for i in (csv_attendance_list['Date'].to_list()):
                                                date_list.append(i)
                                            max_no_of_days = {
                                                'JAN': 31,
                                                'FEB': 28,  
                                                'MAR': 31,
                                                'APR': 30,
                                                'MAY': 31,
                                                'JUNE': 30,
                                                'JULY': 31,
                                                'AUG': 31,
                                                'SEP': 30,
                                                'OCT': 31,
                                                'NOV': 30,
                                                'DEC': 31
                                            }
                                            month_num = next((int(k) for k, v in di.items() if v == selected_month), None)
                                            month_list = [i for i in year_list if i.month == month_num]

                                            for i in range(1,max_no_of_days[selected_month]+1):
                                                date_str = f"2025-{month_num:02d}-{i:02d}"
                                                date_obj=datetime.strptime(date_str,"%Y-%m-%d").date()
                                                if date_obj not in date_list:        
                                                    csv_attendance_list=pd.concat([csv_attendance_list, pd.DataFrame([{'Date':date_obj,'Attended/Not': 'No'}])], ignore_index=True)

                                            csv_attendance_list=csv_attendance_list.sort_values('Date')
                                            csv_attendance_list=csv_attendance_list.to_csv(index=False).encode('utf-8') 
                                            st.download_button(label=f"{selected_month} Report", mime='text/csv',key="download_user", data=csv_attendance_list, file_name=f'{user}_{selected_month}_attendance.csv')
                                    this_month_list = []
                                    this_month_list = [i for i in year_list if i.month == month]
                                    attendance_per = (round((len(this_month_list)/max_no_of_days[di[str(month)]])*100,4))
                                    if attendance_per >= 70:
                                        st.success(f"The Attendance percentnage for this {month}th month {di[str(month)]} is: {attendance_per}%")
                                    elif attendance_per>= 60 and attendance_per <= 70:
                                        st.warning(f"The Attendance percentnage for this {month}th month {di[str(month)]} is: {attendance_per}%")
                                    else:
                                        st.error(f"The Attendance percentnage for this {month}th month {di[str(month)]} is: {attendance_per}%")
                                except pd.errors.EmptyDataError:
                                        df = pd.DataFrame(columns=['SessionID','Name','Date'])
                                        df.to_csv(ATTENDANCE_FILE)
                                        st.info("You've not marked attendance yet!")
                                except FileNotFoundError:
                                        df = pd.DataFrame(columns=['SessionID','Name','Date'])
                                        df.to_csv(ATTENDANCE_FILE)
                                        st.info("Attendance file not found yet. Start marking attendance!")

#   =============================== CLASS REPRESENTATIVE TAB =============================

                            elif role == 'Class Representative':
                                rep_pass = st.text_input("Enter Rep Password:", type='password').strip()
                                selected_date = st.date_input("Select Date to View Attendance:", value=datetime.today())
                                selected_date_str = selected_date.strftime('%Y-%m-%d')
                                if rep_pass == "":
                                    st.warning("Enter correct password to access details!")

                                elif rep_pass == rep_password:
                                    attendance_df = pd.read_csv(ATTENDANCE_FILE)
                                    daily_attendance = attendance_df[attendance_df['Date'] == selected_date_str]
                                    present_list = daily_attendance['Name'].tolist()
                                    absent_list = [name for name in CLASS_ROLL_NUMBERS if name not in present_list]
                                    absent_df=pd.DataFrame({'Name':absent_list})
                                    
                                    st.subheader(f'Attendance for {selected_date_str}:')
                                    col1, col2, col3 = st.columns([1, 6, 1])

                                    permissions_df = pd.read_csv(PERMISSIONS_FILE)
                                    permissions_df=permissions_df.drop(columns=['Reason','No_of_days'])
                                    import numpy as np
                                    absent_df['result'] = np.where(
                                        absent_df['Name'].isin(permissions_df['Roll_no']),
                                        'A',
                                        'NA'
                                    )

                                    def apply_highlight(row):
                                        color = 'background-color:white;color:black;' if row['result'] == 'A' else 'background-color:black;color:white;'
                                        return [color] * len(row) 


                                    coloured_df=absent_df.loc[:].style.apply(apply_highlight, axis=1)

                                    with col2:
                                        cola, colb = st.columns(2)
                                        with cola:
                                            st.write('**Presenties:**')
                                            if present_list:
                                                st.write(daily_attendance['Name'])
                                            else:
                                                st.write("No one present.")
                                        with colb:
                                            st.write('**Absenties:**')
                                            if absent_list:
                                                st.dataframe(coloured_df, use_container_width=True)
                                            else:
                                                st.write("Everyone present!")
                                        with col2:
                                            col = st.columns(1)
                                            attendance_data=pd.concat([pd.Series([selected_date_str] * max(len(present_list), len(absent_list))), daily_attendance['Name'], absent_df], axis=1, ignore_index=True)
                                            cr_csv_data=attendance_data.to_csv(index=False).encode('utf-8')
                                            st.download_button(label='Download Report', data=cr_csv_data, mime='text/csv', key='CR_Download', file_name=ATTENDANCE_FILE)
                                else:
                                    st.error('Wrong Rep Password!')

                                if st.button('Reset Attendance for Selected Date') and rep_pass == rep_password:
                                    attendance_df = attendance_df[attendance_df['Date'] != selected_date_str]
                                    attendance_df.to_csv(ATTENDANCE_FILE, index=False)
                                    st.info(f"Attendance reset for {selected_date_str}!")
                    else:
                        st.error("Please enter a valid roll number.")

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
#   =========================== CHAT TAB ===============================

                with tab2:
                    st.subheader("🗨️ Group chat")
                    try:
                        roll_no_tab3 = saved_roll 
                    except:
                        roll_no_tab3 = None
                    if roll_no_tab3 and roll_no_tab3 in CLASS_ROLL_NUMBERS:
                        if is_bound_to_another_device(roll_no_tab3) and checking(roll_no_tab3):
                            st.error(f"ERROR: Roll number {roll_no_tab3} is enrolled with another device. Access denied.")
                        elif st.session_state['user'] is not None and roll_no_tab3 != st.session_state['user']:
                            st.error("Provide the Valid Roll NO first!")
                        else:
                            chat1, chat2, chat3=st.tabs(['Messages', 'Polls', 'Files'])
                            with chat1:
                                if not os.path.exists(MESSAGE_FILE):
                                    st.info("💭 No messages yet. Start the conversation!")
                                    message_df = pd.DataFrame(columns=['Roll_no', 'Message'])
                                    message_df.to_csv(MESSAGE_FILE, index=False)
                                else:
                                    message_df = pd.read_csv(MESSAGE_FILE)
                                
                                issue = st.chat_input("Enter your issue: ")
                                if issue:
                                    sanitized_issue = html.escape(issue)
                                    new_msg = pd.DataFrame({"Roll_no": [roll_no_tab3], "Message": [sanitized_issue]})
                                    message_df = pd.concat([message_df, new_msg], ignore_index=True)
                                    message_df.to_csv(MESSAGE_FILE, index=False)
                                
                                message_df = message_df.sort_index()
                                
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
                                if st.button("🗑️ Clear chat"):
                                    message_df = pd.DataFrame(columns=message_df.columns)
                                    message_df.to_csv(MESSAGE_FILE, index=False)
                                # st.rerun()
                            with chat2:
                                import ast                                 
                                roll = st.text_input("Enter your Rollno: ", value = roll_no_tab3, disabled=True) 
                                with st.expander("🔊 Create a New Poll"):
                                    question = st.text_input("Poll question")
                                    option_cols = st.columns(4)
                                    options = []
                                    
                                    for i in range(4):
                                        opt = option_cols[i].text_input(f"Option {i+1}", key=f"option_{i}")
                                        if opt:
                                            options.append(opt)
                                    

                                    if st.button("➕ Create Poll"):
                                        if question and len(options) >= 2:
                                            df = pd.DataFrame({'question': question,'options': options, 'votes': [0,0,0,0], 'voted': [[] for _ in options], 'created_by': [roll_no_tab3 for _ in options]})
                                            df.to_csv(POLLS)
                                            st.success("Poll created successfully!")
                                            st.rerun()
                                        else:
                                            st.warning("Please enter a question and at least two options.") 

                                st.write("---")

                                try: 
                                    df = pd.read_csv(POLLS) 
                                    options = df['options']
                                    st.header(df['question'][0]) 
                                    st.write(f"Created by: {df['created_by'][0]}") 
                                    choosed = st.radio("Choose any one: ", options=options)
                                    row_index=0
                                    if st.button("Submit"):
                                        if roll in df['voted'][0]:
                                            st.warning("You've aldready entered!!") 
                                        elif roll != "":
                                            df.loc[df['options'] == choosed, 'votes'] += 1

                                            df['voted'] = df['voted'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)


                                            df.at[row_index, 'voted'].append(roll)

                                            df.to_csv(POLLS, index=False)
                                            # st.write(df) 

                                        elif roll == "":
                                            st.warning("Enter Roll NO")
                                    # st.write(df['voted'][0]) 
                                except:
                                    st.info("No Poll created yet!!")

                                st.write("---")

                                try:
                                    df = pd.read_csv(POLLS) 
                                    total = 0
                                    for i in df['votes']:
                                        total += i 
                                    st.header("Results Section: ")
                                    for i,j in enumerate(df['votes']):
                                        print(f"Option {i}: {j/total * 100}") 
                                        st.progress(value = j/total, text = f"Option {i+1}: {j/total * 100}%") 
                                    st.rerun()
                                except:
                                    pass 


                                if st.button("Delete Poll", type='primary'):
                                    if roll == df['created_by'][0]:
                                        df = pd.DataFrame(columns=['question','options','votes','voted', 'created_by'])
                                        df.to_csv(POLLS, index=False) 
                                        # st.rerun()
                                    else:
                                        st.error("You cannot do it as your roll no not matching!") 

                            with chat3:
                                st.file_uploader('Drop files here: ',type=["jpg", "jpeg", "png", "csv", "png"],accept_multiple_files=True)

                           
                    else:
                        st.error("Please enter a valid roll number.")

#   ======================= ASK PERMISSION TAB =========================

                with tab3:
                    no_of_days = 0
                    try:
                        Roll_no = saved_roll
                    except:
                        Roll_no = None
                    if Roll_no and Roll_no in CLASS_ROLL_NUMBERS:

                        if (is_bound_to_another_device(Roll_no) and checking(Roll_no)):
                                st.error(f"ERROR: Roll number {Roll_no} is enrolled with another device. Access denied.")
                        else:
                                if st.session_state['user'] is not None and roll_no_tab3 != st.session_state['user']:
                                    st.error("Provide the Valid Roll NO first!")
                                else:
                                    with st.form("permission_form", clear_on_submit=True):
                                        st.subheader("New Permission request")
                                        no_of_days = st.slider("Number of days: ", min_value=1, max_value=10)
                                        if not os.path.exists(PERMISSIONS_FILE):
                                                per_df = pd.DataFrame(columns=['Roll_no', 'Reason', 'Granted', "No_of_days"])
                                                per_df.to_csv(PERMISSIONS_FILE, index=False)
                                        else:
                                                per_df = pd.read_csv(PERMISSIONS_FILE)
                                            
                                        issue = st.text_area("Reason for leave",placeholder="Explain your reason briefly...", key="permission_input")
                                        if st.form_submit_button("Send Request"):
                                                sanitized_issue = html.escape(str(issue))
                                                sanitized_days = html.escape(str(no_of_days))
                                                new_msg = pd.DataFrame({"Roll_no": [roll_no_tab3], "Reason": [sanitized_issue], "No_of_days": [sanitized_days], "Granted": ['Pending']})
                                                per_df = pd.concat([per_df, new_msg], ignore_index=True)
                                                per_df.to_csv(PERMISSIONS_FILE, index=False)
                                            
                                        per_df = per_df.sort_index()
                                    st.write("---")
                                    st.subheader("📑 Requested Permissions report")
                                    if Roll_no in per_df['Roll_no'].values:
                                        if (per_df.loc[per_df['Roll_no'] == Roll_no, 'Granted'] == 'Pending').any():
                                            # st.toast("⌛Your request is pending...")
                                            st.warning(f"😥😥Your case is still in **PENDING**")
                                        elif per_df.loc[per_df['Roll_no'] == Roll_no, 'Granted'].any():
                                    
                                            st.toast("🎉 Your leave has been approved!", icon="✅", duration='short')
                                            st.markdown(
                                                "<audio autoplay><source src='https://www.soundjay.com/buttons/button-3.mp3' type='audio/mpeg'></audio>",
                                                unsafe_allow_html=True
                                                )
                                            st.success(f'✅ Your permissions for {per_df.loc[per_df['Roll_no'] == Roll_no, 'No_of_days'][0]} days has been granted!!')
                                            
                                        else:
                                            st.toast("Your leave might be rejected!", icon="❌")
                                            st.markdown(
                                                "<audio autoplay><source src='https://www.soundjay.com/buttons/button-3.mp3' type='audio/mpeg'></audio>",
                                                unsafe_allow_html=True
                                            )
                                            st.error('😑😑The Mentor has **MIGHT BE REJECTED** your leave!!')
                                    else:
                                        st.write("You didn't raise any permission request!!")
                    else:
                        st.error("Please enter a valid roll number.")
                st.caption(f"Device ID: {device_id}")            

#   ======================= LEADER BOARD TAB ============================

                with tab4:
                    st.subheader("🏆 Attendance Leaderboard")
                    tab4_df=pd.read_csv(ATTENDANCE_FILE)
                    month=datetime.today().month
                    date_series=tab4_df['Date']
                    student_list = []
                    for i in date_series:
                        if datetime.strptime(i, "%Y-%m-%d").date().month == month:
                            student_list.append(tab4_df.loc[tab4_df['Date'] == i, 'Name'].values) 
                    df=pd.DataFrame(student_list)
                    df=df.drop_duplicates()
                    final_list = []
                    for i in df.columns:
                        for j in df[i]:
                            final_list.append(j)
                    leader_df=pd.DataFrame(columns=['Roll_NO', 'Present']) 
                    for i in final_list:
                        single_df=pd.DataFrame({'Roll_NO': [i], 'Present': [final_list.count(i)]})
                        leader_df=pd.concat([leader_df, single_df], ignore_index=True)
                    leader_df=leader_df.dropna()
                    leader_df=leader_df.drop_duplicates()
                    st.write(leader_df)
                    leader_df=leader_df.to_csv(index=False).encode('utf-8')
                    _,butt,_= st.columns([1,1,1])
                    with butt:
                        st.download_button(label='📤 Download Leaderboard', file_name=f"{month}Leaderboard.csv", data=leader_df,mime='text/csv', key=f"{month}Leaderboard")
    

                with tab5:
                    st.title("Previous Attendance Records")
                    user = st.session_state['user']
                    from io import StringIO
                    july = """
                    0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22
                    X1,SANAPATHIYAMUNA,P,P,P,AB,P,P,P,P,P,P,AB,P,AB,P,P,P,P,AB,P,AB,P
                    X2,SANKURABOTHUMANITEJ,P,P,P,P,P,P,AB,P,P,AB,P,P,P,P,P,P,P,P,P,P,P
                    X3,SARIKAAASWITHA,P,P,P,P,P,AB,P,P,P,P,P,P,P,P,P,P,AB,P,P,P,P
                    X4,SARIKAJASMINE,P,P,P,P,AB,AB,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
                    X5,SATTALARAMAKRISHNA,AB,AB,P,P,P,P,AB,P,P,P,P,P,P,P,P,P,P,P,P,P,AB
                    X6,SEEMAKURTHISAHITHI,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
                    X7,SEERAPUARYANREDDY,AB,AB,AB,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
                    X8,SEERAPUMEGHANA,AB,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,AB,P,P
                    X9,SEERAPUSHIVADHEERAJ,P,P,P,P,P,AB,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
                    Y0,SHAIKSHAHID,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
                    Y1,SHAIKSHAZID,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
                    Y2,SHEIKARIF,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
                    Y3,SHEIKNOORJAHAN,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,AB,P,P
                    Y4,SHETTITEJASWARI,AB,AB,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,AB,P,P
                    Y5,SIDAGAMRAJESH,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
                    Y6,SIDDAANITHA,P,P,P,P,P,P,AB,P,P,P,P,P,P,P,P,P,P,P,P,P,P
                    Y7,SIGALAPELLIPAVANKUMAR,P,P,P,P,P,P,P,P,AB,AB,AB,AB,AB,P,P,AB,P,P,P,P,P
                    Y8,SIRIPURAPURAGHU,P,AB,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
                    Y9,SIRIPURAPUTRINADHA,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
                    Z0,SIVVITIKIRANMAYEE,P,P,P,P,P,AB,P,P,P,P,AB,P,P,P,P,P,P,P,P,P,P
                    Z2,SURUAKSHAYA,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
                    Z3,TAKARLARONITHREDDY,P,P,P,P,P,P,P,P,P,P,AB,AB,AB,P,P,P,P,AB,P,P,P
                    Z4,TALACHUTLAHASINI,P,P,P,P,P,P,P,P,P,P,P,AB,P,P,P,P,P,P,AB,P,P
                    Z5,TALADAKAVYAJAHNAVI,P,P,P,P,P,P,P,P,AB,P,AB,P,P,P,P,P,P,P,P,P,P
                    Z6,TALADASREEVENKATESH,P,P,P,P,P,P,P,P,P,P,P,AB,P,P,P,P,P,P,P,P,P
                    Z7,TALEBHANUTEJA,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
                    Z8,TEDLAPUSAIREESHNIKA,AB,AB,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
                    Z9,TEDLAPUSHANMUKHESWAR,P,P,P,P,P,P,P,P,P,P,AB,AB,P,P,P,P,P,P,P,P,P
                    AA,TEEDAJENYA,AB,AB,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
                    AB,TEEDASRILAKSHMI,P,P,P,P,AB,P,P,P,P,AB,P,P,P,P,P,P,P,P,P,P,P
                    AC,TELUKALAKEERTHANA,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
                    AD,THADDIVINAY,AB,AB,P,AB,P,P,P,P,P,P,AB,P,P,P,P,P,P,AB,P,P,P
                    AE,THAMMINATEJASWI,P,P,P,P,P,P,P,P,P,P,AB,P,P,P,P,P,P,P,P,P,P
                    AF,THOTAGAYATHRISRUJANA,P,P,P,P,AB,P,AB,P,P,P,P,P,P,P,P,P,P,P,P,P,P
                    AG,THUMMAGANTIGANESH,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
                    AH,TIPPANASAINIKHILESH,AB,AB,AB,P,P,AB,P,P,P,P,AB,AB,AB,P,P,AB,AB,AB,AB,AB,AB
                    AI,TRIPURAGIRIAKHILA,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
                    AJ,TULUGUGAYATHRI,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
                    AK,UPPALAPATIYOGENDRAVARMA,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
                    AL,VADAPALLILIKHITHMANOHAR,P,P,P,P,P,P,P,P,P,P,AB,P,P,P,P,P,P,P,P,AB,P
                    AM,VADDADINAGESHKUMAR,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,AB,P,P,P
                    AN,VADUGURUSRINIDHI,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
                    AO,VAKAMULLULAKSHMINARAYANA,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,AB,AB
                    AP,VALLURIRANADHEERNAIDU,P,P,P,P,P,P,P,P,AB,P,P,P,P,P,P,P,P,P,P,P,P
                    AQ,VANKAYASWANTHESWAR,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
                    AR,VARREJAGADEESH,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
                    AS,VARRILEELAKRISHNA,P,P,P,P,P,AB,P,P,P,P,AB,P,P,P,P,P,P,P,P,P,P
                    AT,VARRINEELIMA,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
                    AU,VEMPADAPUMOHINI,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
                    AV,VEMPADAPUUMAJYOTHSNA,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
                    AW,YADLASAIDEEKSHITHA,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
                    AX,YAJJALAKISHOR,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
                    AY,YALAANUSH,P,P,P,P,P,AB,P,P,P,P,AB,P,P,P,P,P,P,P,P,AB,AB
                    AZ,YALLASAMUELSATHVIK,P,P,P,P,P,P,P,P,P,AB,P,P,P,P,P,P,P,P,P,P,P
                    BA,YANDRAPUVAMSI,AB,P,P,AB,AB,P,P,P,AB,P,P,P,P,P,P,P,P,P,P,P,P
                    BB,YARRAMADHUSUDHANARAO,P,P,P,P,P,P,P,AB,P,AB,P,P,P,P,P,P,P,P,P,P,AB
                    BD,YARRARAPUPUNYAVATHI,P,P,P,P,P,AB,AB,P,P,P,P,P,P,P,P,P,AB,AB,AB,P,P
                    BE,YEGIREDDYTEJA,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,AB
                    BF,YELAMANCHILIRAKESH,P,P,P,P,P,P,P,P,P,P,AB,P,P,P,P,P,P,P,P,P,P
                    BG,YELUSOORIVIJAY,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
                    BH,YERRARUPESH,P,P,P,P,P,P,P,P,P,P,P,AB,AB,P,P,AB,AB,AB,P,AB,AB
                    BI,YERRASHYAMCHANDU,P,P,AB,P,P,P,P,P,P,P,AB,P,P,P,P,P,P,P,P,P,P
                    BJ,YERRASIRICHANDANA,P,P,P,P,AB,AB,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
                    BK,YETURISURESH,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,AB,P
                    """

                    august = """
                    0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22
                    X1,SANAPATHIYAMUNA,P,P,P,AB,P,P,P,P,P,P,AB,P,AB,P,P,P,P,AB,P,AB,P
                    X2,SANKURABOTHUMANITEJ,P,P,P,P,P,P,AB,P,P,AB,P,P,P,P,P,P,P,P,P,P,P
                    X3,SARIKAAASWITHA,P,P,P,P,P,AB,P,P,P,P,P,P,P,P,P,P,AB,P,P,P,P
                    X4,SARIKAJASMINE,P,P,P,P,AB,AB,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
                    X5,SATTALARAMAKRISHNA,AB,AB,P,P,P,P,AB,P,P,P,P,P,P,P,P,P,P,P,P,P,AB
                    X6,SEEMAKURTHISAHITHI,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
                    X7,SEERAPUARYANREDDY,AB,AB,AB,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
                    X8,SEERAPUMEGHANA,AB,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,AB,P,P
                    X9,SEERAPUSHIVADHEERAJ,P,P,P,P,P,AB,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
                    Y0,SHAIKSHAHID,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
                    Y1,SHAIKSHAZID,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
                    Y2,SHEIKARIF,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
                    Y3,SHEIKNOORJAHAN,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,AB,P,P
                    Y4,SHETTITEJASWARI,AB,AB,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,AB,P,P
                    Y5,SIDAGAMRAJESH,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
                    Y6,SIDDAANITHA,P,P,P,P,P,P,AB,P,P,P,P,P,P,P,P,P,P,P,P,P,P
                    Y7,SIGALAPELLIPAVANKUMAR,P,P,P,P,P,P,P,P,AB,AB,AB,AB,AB,P,P,AB,P,P,P,P,P
                    Y8,SIRIPURAPURAGHU,P,AB,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
                    Y9,SIRIPURAPUTRINADHA,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
                    Z0,SIVVITIKIRANMAYEE,P,P,P,P,P,AB,P,P,P,P,AB,P,P,P,P,P,P,P,P,P,P
                    Z2,SURUAKSHAYA,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
                    Z3,TAKARLARONITHREDDY,P,P,P,P,P,P,P,P,P,P,AB,AB,AB,P,P,P,P,AB,P,P,P
                    Z4,TALACHUTLAHASINI,P,P,P,P,P,P,P,P,P,P,P,AB,P,P,P,P,P,P,AB,P,P
                    Z5,TALADAKAVYAJAHNAVI,P,P,P,P,P,P,P,P,AB,P,AB,P,P,P,P,P,P,P,P,P,P
                    Z6,TALADASREEVENKATESH,P,P,P,P,P,P,P,P,P,P,P,AB,P,P,P,P,P,P,P,P,P
                    Z7,TALEBHANUTEJA,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
                    Z8,TEDLAPUSAIREESHNIKA,AB,AB,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
                    Z9,TEDLAPUSHANMUKHESWAR,P,P,P,P,P,P,P,P,P,P,AB,AB,P,P,P,P,P,P,P,P,P
                    AA,TEEDAJENYA,AB,AB,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
                    AB,TEEDASRILAKSHMI,P,P,P,P,AB,P,P,P,P,AB,P,P,P,P,P,P,P,P,P,P,P
                    AC,TELUKALAKEERTHANA,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
                    AD,THADDIVINAY,AB,AB,P,AB,P,P,P,P,P,P,AB,P,P,P,P,P,P,AB,P,P,P
                    AE,THAMMINATEJASWI,P,P,P,P,P,P,P,P,P,P,AB,P,P,P,P,P,P,P,P,P,P
                    AF,THOTAGAYATHRISRUJANA,P,P,P,AB,P,AB,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
                    AG,THUMMAGANTIGANESH,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
                    AH,TIPPANASAINIKHILESH,AB,AB,AB,P,P,AB,P,P,P,P,AB,AB,AB,P,P,AB,AB,AB,AB,AB,AB
                    AI,TRIPURAGIRIAKHILA,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
                    AJ,TULUGUGAYATHRI,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
                    AK,UPPALAPATIYOGENDRAVARMA,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
                    AL,VADAPALLILIKHITHMANOHAR,P,P,P,P,P,P,P,P,P,P,AB,P,P,P,P,P,P,P,P,AB,P
                    AM,VADDADINAGESHKUMAR,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,AB,P,P,P
                    AN,VADUGURUSRINIDHI,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
                    AO,VAKAMULLULAKSHMINARAYANA,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,AB,AB
                    AP,VALLURIRANADHEERNAIDU,P,P,P,P,P,P,P,P,AB,P,P,P,P,P,P,P,P,P,P,P,P
                    AQ,VANKAYASWANTHESWAR,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
                    AR,VARREJAGADEESH,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
                    AS,VARRILEELAKRISHNA,P,P,P,P,P,AB,P,P,P,P,AB,P,P,P,P,P,P,P,P,P,P
                    AT,VARRINEELIMA,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
                    AU,VEMPADAPUMOHINI,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
                    AV,VEMPADAPUUMAJYOTHSNA,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
                    AW,YADLASAIDEEKSHITHA,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
                    AX,YAJJALAKISHOR,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
                    AY,YALAANUSH,P,P,P,P,P,AB,P,P,P,P,AB,P,P,P,P,P,P,P,P,AB,AB
                    AZ,YALLASAMUELSATHVIK,P,P,P,P,P,P,P,P,P,AB,P,P,P,P,P,P,P,P,P,P,P
                    BA,YANDRAPUVAMSI,AB,P,P,AB,AB,P,P,P,AB,P,P,P,P,P,P,P,P,P,P,P,P
                    BB,YARRAMADHUSUDHANARAO,P,P,P,P,P,P,P,AB,P,AB,P,P,P,P,P,P,P,P,P,P,AB
                    BD,YARRARAPUPUNYAVATHI,P,P,P,P,P,AB,AB,P,P,P,P,P,P,P,P,P,AB,AB,AB,P,P
                    BE,YEGIREDDYTEJA,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,AB
                    BF,YELAMANCHILIRAKESH,P,P,P,P,P,P,P,P,P,P,AB,P,P,P,P,P,P,P,P,P,P
                    BG,YELUSOORIVIJAY,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
                    BH,YERRARUPESH,P,P,P,P,P,P,P,P,P,P,P,AB,AB,P,P,AB,AB,AB,P,AB,AB
                    BI,YERRASHYAMCHANDU,P,P,AB,P,P,P,P,P,P,P,AB,P,P,P,P,P,P,P,P,P,P
                    BJ,YERRASIRICHANDANA,P,P,P,P,AB,AB,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
                    BK,YETURISURESH,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,AB,P
                    """
                    sept = """
                    0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18
                    X1,SANAPATHIYAMUNA,AB,P,AB,AB,AB,P,P,P,P,P,P,P,P,AB,P,P,P
                    X2,SANKURABOTHUMANITEJ,P,P,P,P,P,P,P,P,P,P,P,AB,AB,P,P,AB,AB
                    X3,SARIKAAASWITHA,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
                    X4,SARIKAJASMINE,P,AB,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
                    X5,SATTALARAMAKRISHNA,AB,P,P,P,P,P,P,P,P,P,P,AB,AB,P,P,P,P
                    X6,SEEMAKURTHISAHITHI,P,P,P,P,AB,P,P,P,P,P,P,P,P,P,P,P,P
                    X7,SEERAPUARYANREDDY,AB,AB,P,P,P,AB,P,P,P,P,P,P,P,P,P,P,P
                    X8,SEERAPUMEGHANA,P,P,AB,P,P,P,P,AB,P,P,P,P,P,P,P,P,P
                    X9,SEERAPUSHIVADHEERAJ,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
                    Y0,SHAIKSHAHID,P,P,P,P,AB,P,P,P,P,P,P,P,P,P,P,AB,P
                    Y1,SHAIKSHAZID,P,P,P,P,AB,P,AB,P,AB,P,P,P,P,AB,P,P,P
                    Y2,SHEIKARIF,P,P,P,P,AB,P,P,P,P,P,P,P,P,P,P,P,P
                    Y3,SHEIKNOORJAHAN,P,P,AB,P,AB,P,P,P,P,P,P,AB,P,AB,P,P,P
                    Y4,SHETTITEJASWARI,P,P,AB,P,P,P,P,P,P,P,AB,P,AB,P,P,P,P
                    Y5,SIDAGAMRAJESH,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
                    Y6,SIDDAANITHA,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
                    Y7,SIGALAPELLIPAVANKUMAR,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
                    Y8,SIRIPURAPURAGHU,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
                    Y9,SIRIPURAPUTRINADHA,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
                    Z0,SIVVITIKIRANMAYEE,AB,AB,P,P,P,P,AB,AB,P,AB,AB,P,P,AB,AB,AB,AB
                    Z2,SURUAKSHAYA,P,P,P,P,P,P,P,P,P,P,P,P,P,AB,P,P,P
                    Z3,TAKARLARONITHREDDY,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
                    Z4,TALACHUTLAHASINI,P,P,P,P,AB,P,AB,P,P,P,P,P,P,AB,P,P,P
                    Z5,TALADAKAVYAJAHNAVI,P,P,AB,P,AB,P,P,P,P,P,P,P,P,P,P,P,P
                    Z6,TALADASREEVENKATESH,P,P,P,P,AB,P,P,AB,P,P,P,P,P,P,P,P,P
                    Z7,TALEBHANUTEJA,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
                    Z8,TEDLAPUSAIREESHNIKA,P,P,P,P,P,AB,AB,P,P,P,P,P,P,P,P,AB,P
                    Z9,TEDLAPUSHANMUKHESWAR,P,P,P,P,P,P,P,AB,P,P,P,P,P,P,P,P,P
                    AA,TEEDAJENYA,P,P,P,P,P,P,P,P,AB,P,P,P,P,P,P,P,P
                    AB,TEEDASRILAKSHMI,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
                    AC,TELUKALAKEERTHANA,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
                    AD,THADDIVINAY,P,P,P,P,P,AB,AB,P,P,P,P,P,AB,AB,AB,P,P
                    AE,THAMMINATEJASWI,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
                    AF,THOTAGAYATHRISRUJANA,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
                    AG,THUMMAGANTIGANESH,P,P,P,P,P,P,AB,P,P,P,P,P,AB,P,P,P,P
                    AH,TIPPANASAINIKHILESH,P,P,P,AB,AB,AB,P,P,P,P,P,P,P,P,P,P,P
                    AI,TRIPURAGIRIAKHILA,P,P,P,AB,P,P,AB,P,P,P,P,P,P,P,P,P,P
                    AJ,TULUGUGAYATHRI,P,P,P,P,AB,P,P,P,AB,P,P,P,P,P,P,P,P
                    AK,UPPALAPATIYOGENDRAVARMA,P,P,AB,P,P,P,P,P,P,P,P,P,P,P,P,AB,P
                    AL,VADAPALLILIKHITHMANOHAR,P,P,P,P,P,AB,P,P,P,P,P,P,P,P,P,P,P
                    AM,VADDADINAGESHKUMAR,P,P,P,P,P,AB,P,P,P,P,P,AB,AB,P,P,P,P
                    AN,VADUGURUSRINIDHI,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
                    AO,VAKAMULLULAKSHMINARAYANA,P,P,P,P,P,P,P,P,P,P,P,P,P,AB,P,P,P
                    AP,VALLURIRANADHEERNAIDU,AB,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
                    AQ,VANKAYASWANTHESWAR,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,AB,P
                    AR,VARREJAGADEESH,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
                    AS,VARRILEELAKRISHNA,P,P,P,AB,P,P,P,P,AB,P,AB,P,P,AB,P,P,P
                    AT,VARRINEELIMA,P,P,P,P,P,P,P,P,P,P,P,P,P,AB,P,P,P
                    AU,VEMPADAPUMOHINI,P,P,P,P,P,P,P,P,P,P,P,P,P,AB,P,P,P
                    AV,VEMPADAPUUMAJYOTHSNA,P,P,P,P,AB,P,P,P,P,P,P,P,P,AB,P,P,P
                    AW,YADLASAIDEEKSHITHA,P,P,P,P,P,P,P,P,P,P,P,P,P,,P,P,P
                    AX,YAJJALAKISHOR,P,P,P,P,P,P,P,P,P,P,P,P,P,AB,P,P,P
                    AY,YALAANUSH,P,P,P,P,P,AB,P,P,P,P,P,P,P,AB,P,P,P
                    AZ,YALLASAMUELSATHVIK,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
                    BA,YANDRAPUVAMSI,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
                    BB,YARRAMADHUSUDHANARAO,P,P,P,P,AB,P,P,P,P,P,P,P,P,P,P,P,P
                    BD,YARRARAPUPUNYAVATHI,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
                    BE,YEGIREDDYTEJA,P,P,P,P,P,P,P,P,P,P,P,P,P,AB,P,P,P
                    BF,YELAMANCHILIRAKESH,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
                    BG,YELUSOORIVIJAY,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
                    BH,YERRARUPESH,P,AB,AB,AB,AB,AB,P,P,P,AB,AB,AB,AB,P,P,AB,P
                    BI,YERRASHYAMCHANDU,P,AB,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
                    BJ,YERRASIRICHANDANA,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
                    BK,YETURISURESH,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
                    """
                    
                    july_df = pd.read_csv(StringIO(july), header=0, index_col=0)
                    july_df.index = july_df.index.str.strip()
                    july_df = july_df[july_df.index == user]


                    august_df = pd.read_csv(StringIO(august), header=0, index_col=0)
                    august_df.index = august_df.index.str.strip()
                    august_df = august_df[august_df.index == user]


                    sept_df = pd.read_csv(StringIO(sept), header=0, index_col=0)
                    sept_df.index = sept_df.index.str.strip()
                    sept_df = sept_df[sept_df.index == user]


                    # Show dataframes in columns
                    j, a, s = st.columns([1, 1, 1])
                    with j:
                        st.dataframe(july_df.T)
                        st.download_button(
                            label="Download July Report",
                            data=july_df.to_csv(index=False).encode('utf-8'),
                            file_name=f"{user}_julyattendance.csv",
                            mime='text/csv',
                            key=f"july_{user}_download"
                        )

                    with a:
                        st.dataframe(august_df.T)
                        st.download_button(
                            label="Download August Report",
                            data=august_df.to_csv(index=False).encode('utf-8'),
                            file_name=f"{user}_augustattendance.csv",
                            mime='text/csv',
                            key=f"august_{user}_download"
                        )

                    with s:
                        st.dataframe(sept_df.T)
                        st.download_button(
                            label="Download Sept Report",
                            data=sept_df.to_csv(index=False).encode('utf-8'),
                            file_name=f"{user}_septattendance.csv",
                            mime='text/csv',
                            key=f"sept_{user}_download"
                        )
#   ======================= ADMIN( RAAMANAND: ME ) TAB ============================

    elif page == "👨‍🔬 Admin":
        st.title("👨‍🔬 Admin Panel")
        def write(msg):
            with open(GOOD_NEWS, mode='w', encoding='utf-8') as f:
                f.write(msg) 

        if st.session_state.get("device_id", None) in ['a9513efb32968fd6881b89f36f221a254578ba203239086a6d39e2a72b5eb847','ae13c33d3dadf2fce93466719f317f193a866f82785e41159b5ac6e09cc23901','45c71d8124d5773d2afc93d2716451a4be8cfcb955bf6d8acdca26066cacc755', '0ef9971b655434bcc90d4be635d49525a96e83b6843d22922e5eb0a3ec7d0939', '924bbb24123b5c091969aac6db8d0bcd17ca4966064cbfe21e017d345e58bf90', '1f755f8ba87ca0d627d2f73c3fbfd2f6d5deda9e18cf4ec81226ab77c77cc10d']:
            st.header("📢 Announcement Management")
            message = st.text_input(label = "New Announcement:", placeholder='Enter your messsage...')
            if st.button("🔊 Publish Announcement"):
                write(message)
        
            if st.button("🔇 Clear Announcement"):
                write("")
            st.write("---")
            st.header("📊 System Statistics")
            try:
                x,y,z=st.columns(3)
                with x:
                    st.metric(f"Total Students",len(CLASS_ROLL_NUMBERS))  
                with y:
                    st.metric(f"Registered Students",len(pd.read_csv(MARKED_FILE)['Roll_no'].tolist()))
                with z:
                    st.metric(f"Today's Attendance", len(pd.read_csv(ATTENDANCE_FILE)[pd.read_csv(ATTENDANCE_FILE)['Date'] == datetime.today().strftime("%Y-%m-%d")]))
            except:
                st.error("Files not created yet!!")
            st.write("---")  
            try:
                st.header("User Feedbacks: ")
                feedback_df = pd.read_csv(FEEDBACK_FILE) 
                for i,j in feedback_df.iterrows():
                    st.write(f"{j[0]}: {j[1]}")    
            except:
                st.info("No one has yet given the feedback!!")           
            st.write("---")
            st.header("🔧 System Maintenance")
            if st.button("🔄 Clear All Data", type="secondary"):
                for file in [ATTENDANCE_FILE, MESSAGE_FILE, PERMISSIONS_FILE, POLLS, FEEDBACK_FILE]:
                    if os.path.exists(file):
                        os.remove(file)
                st.success("All data cleared!") 
        else:
            st.error("🚫 Access denied. Admin privileges required.")

#   ======================= ABOUT TAB ===========================

    elif page == "ℹ️ About":
            from datetime import datetime

            APP_NAME = "GeoMark Attendance"
            VERSION = "v2.0"
            DEVELOPER = "Raamanand"
            LAST_UPDATE = datetime(2025, 10, 27)

            about_header = f"""
            # {APP_NAME}
            
            ---
            Updated Recently on: {LAST_UPDATE}\n
            Welcome to my advanced, location-based attendance management platform—engineered to deliver reliable, secure, and automated attendance for educational institutions and organizations.
            """

            st.markdown(about_header)
            st.subheader("Advanced Features")
            st.markdown(
            """
            - **Smart Location Validation:** Ensures users are at authorized physical locations before marking attendance (uses HTML5 Geolocation API).
            - **Role-Based Security:** Custom access control for students, admins, and supervisors with encrypted session tokens.
            - **Real-Time Analytics:** Visual dashboards, attendance statistics, and downloadable reports.
            - **Proxy Prevention:** Strict geolocation and session checks to block fraudulent or duplicate entries.
            """
            )
            st.error("⚠️⚠️**One Time Registration:** This feature will not allow any user to use another user's details. And once registered to a device, that very device owner could only use those details.")
            

            st.write("---")
            st.info("Driven by a passion for building robust, real-world solutions for education and organizations.")

            st.metric(label="App Version", value="v2.0", delta="+1 new feature")
            st.metric(label="Active Users", value="000", delta="+2 this week")

            tab1, tab2 = st.tabs(["Overview", "Technical Details"])
            with tab1:
                st.markdown("""
                Welcome to our advanced, location-based attendance platform.
                - **Location Validation**
                - **Security & Analytics**
                - Role-based access
                """)
            with tab2:
                st.subheader("Technology Stack")
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(
                        """
                        - Python 3.13+
                        - Streamlit
                        - SQLite (Data Storage)
                        - HTML5 Geolocation
                        """
                    )
                with col2:
                    st.markdown(
                        """
                        - Pandas (Data Handling)
                        - Secure Session Management
                        - Responsive Web UI
                        - Real-time Data Analytics
                        """
                    )

            with st.expander("Meet the Developer"):
                st.write("Created by Raamanand, a student developer passionate about practical AI solutions.")

            st.download_button("Download App Manual", """~ A Website made by Raamanand.""", file_name="manual.txt")

#   ======================= SETTINGS TAB ========================

    elif page == "⚙️ Settings":
            st.header("🛠️ Account Settings")
            with st.form("Settings_form"):
                st.subheader("🔒 Change Password")
                prev_name=st.text_input("Enter Current Username: ", placeholder=f"E.g: YAKSHRAJ").strip()
                prev_pass=st.text_input("Enter Current password: ", placeholder='******', type='password').strip()
                curr_pass=st.text_input("Enter New password: ", placeholder="******", type='password').strip()
                if st.form_submit_button("Update Password"):
                    if prev_name == "" or prev_pass == "" or curr_pass == "":
                        st.warning("All fields are required!!")
                    elif not password_df.loc[password_df['user_name'] == prev_name, 'pass'].empty and prev_pass == password_df.loc[password_df['user_name'] == prev_name, 'pass'].values[0]:
                        password_df.loc[password_df['user_name']==prev_name, 'pass'] = curr_pass 
                        password_df.to_csv(PASS_FILE, index=False)
                        st.success(f"Password has changed to {password_df.loc[password_df['user_name'] == prev_name, 'pass'].values[0]}")
        
                    elif password_df.loc[password_df['user_name'] == prev_name].empty or prev_name not in password_df['user_name'].to_list():
                        st.error("User Name is incorrect!")
                    elif prev_pass != password_df.loc[password_df['user_name'] == prev_name, 'pass'].values[0]:
                        st.error("The password is incorrect!!")
        
                    else:
                        st.error("❌❌ Error Occured!!")
            st.write("---")
            st.subheader("📱 Device Information")
            st.write(f"**Device ID:** {st.session_state['device_id']}")
            st.write(f"**Session ID:** {get_script_run_ctx().session_id if get_script_run_ctx() else 'N/A'}")
        
            st.write("---")
        
            if st.button("🚪 Logout", type="primary"):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun() 
    
    
    elif page == "🪧 NoticeBoard":
        st.title("🪧 NoticeBoard")
        st.info("No significant highlights are available!!") 
        
    elif page == "🧑‍🍼 Feedback":
        st.title("Drop your feedback here (if any) !")
        st.write("---")
        with st.form("FeedbackForm"):
            feed_name = st.text_input("Kindly enter your name:") 
            feedback = st.text_area("Feedback form: ", placeholder = 'Type your feedback here!!')
            if st.form_submit_button("Submit!"):
                if feedback != "" and feed_name != "":
                    if not os.path.exists(FEEDBACK_FILE):
                        feedback_df = pd.DataFrame({'name':[feed_name], 'feedback': [feedback]})
                        feedback_df.to_csv(FEEDBACK_FILE, index=False) 
                    st.success("🙏 Thank you for giving your feedback!!")
                    import time
                    time.sleep(2)
                elif feed_name == "":
                    st.warning("Kindly enter the name you wanted to be appeleated with!")
        st.write("---")
         









