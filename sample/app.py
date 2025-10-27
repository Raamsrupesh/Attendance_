import streamlit as st
import pandas as pd
from datetime import datetime
import os
from streamlit.runtime.scriptrunner import get_script_run_ctx
import hashlib
import sqlite3
import uuid
primary_input = st.text_input("Enter your password: ", placeholder='E.g: Secret Password', type = 'password')
if primary_input == f"{chr(82)+chr(65)+chr(65)+chr(77)}":
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
    st.sidebar.title("Navigation Bar")

    page = st.sidebar.radio("Select either of these:", ["Mentor", "Student", "About", "Settings"], index=1)
    import html
    if page == "Mentor":
            TEA_CR_PASSWORD = f'{chr(84)+chr(69)+chr(65)+chr(67)+chr(82)}'
            PERMISSIONS_FILE = "permissions.csv"
            ment_cr_pass = st.text_input("Enter Mentor/Cr Password:", type='password')
            if ment_cr_pass == TEA_CR_PASSWORD:
                from streamlit_autorefresh import st_autorefresh
                st_autorefresh(interval=1500, key='mentor_refresh')
                try:
                    per_df = pd.read_csv(PERMISSIONS_FILE)
                    for idx, row in per_df.iterrows():
                        sanitized_roll = html.escape(str(row['Roll_no']))
                        sanitized_msg = html.escape(str(row['Reason']))
                        key=f"checkbox_{idx}"
                        if key not in st.session_state:
                            st.session_state[key] = False 
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
                            # per_df.loc[per_df['Roll_no'] == sanitized_roll, 'No_of_days'] = no_of_days
                        else:
                            per_df.loc[per_df['Roll_no'] == sanitized_roll, 'Granted'] = False  
                            # per_df.loc[per_df['Roll_no'] == sanitized_roll, 'No_of_days'] = no_of_days
                        per_df.to_csv(PERMISSIONS_FILE, index=False)

                    if st.button("Reset", key="Mentor_erasing"):
                        per_df = pd.DataFrame(columns=per_df.columns)
                        per_df.to_csv(PERMISSIONS_FILE, index=False)
                        st.rerun()

                except FileNotFoundError or NameError:
                    st.success("NO ONE YET ASKED PERMISSION AND NOTHING TO DOWNLOAD!!")
                try:
                    csv_data=per_df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                            label="Download Permissions Report",
                            data=csv_data,
                            file_name=PERMISSIONS_FILE,
                            mime="text/csv",
                            key="download-permissions"
                    )
                except:
                    pass 
                st.write("-------------------")
                date=st.date_input("Enter the date of attendance: ")
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
                        st.subheader("Absenties: ")
                        absent = pd.DataFrame([i for i in options if i not in present_list],columns=['Roll_NO'])
                        st.write(absent)
                    except:
                        pass 
                try:
                    ment_attendance_df=(pd.concat([pd.Series(data=[str(date)] * max(len(present), len(absent))),present, absent], axis=1,ignore_index=True))
                    ment_attendance_df=ment_attendance_df.rename(columns={0: 'Date', 1:'Presenties', 2: 'Absenties'})    
                    ment_attendance_df=ment_attendance_df.to_csv(index=False).encode('utf-8')
                    _,abc,_ = st.columns([1,2,1])
                    with abc:
                        # st.write(ment_attendance_df)
                        st.download_button(label="Download Attendance", file_name=f"{date}atttendance_report.csv", data=ment_attendance_df, mime='text/csv',key='DOWNLOAD_MENT_ATTENDANCE')
                except NameError:
                    pass
        

    elif page == "Student":
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
                st.write(f"Device Cookie Value: {cookie_id}")  # Helpful for debugging, remove in production if you want!
                device_id = cookie_id
            else:
                new_id = hashlib.sha256(str(uuid.uuid4()).encode()).hexdigest()
                controller.set("device_id", new_id, max_age=3600 * 24 * 365)
                st.warning("Cookie set, please reload the page for proper persistence.")
                st.stop()

            st.session_state["device_id"] = device_id

            #================= MARKED CSV loading and saving =================
            MARKED_FILE = "marked.csv"
            if not os.path.exists(MARKED_FILE):
                pd.DataFrame(columns=["Roll_no", "device_id"]).to_csv(MARKED_FILE, index=False)

            marked_df = pd.read_csv(MARKED_FILE)

            #================= Registration / Login UI =================
            st.title("Register / Login")

            registered_entry = marked_df.loc[marked_df["device_id"] == device_id]

            if not registered_entry.empty:
                # Already registered => Show only as view/locked mode
                saved_roll = registered_entry.iloc[0]["Roll_no"]
                st.success(f"You are permanently registered with Roll No: {saved_roll}")
                st.text_input("Roll Number", value=saved_roll, disabled=True)
                st.info("You cannot change Roll Number on this device.")
                st.caption(f"Device ID: {device_id}")
            else:
                # Not yet registered => Allow one-time registration
                name = st.text_input("Enter your Name:")
                roll_no = st.text_input("Enter your Roll Number:")
                if st.button("Register"):
                    if not name or not roll_no:
                        st.error("Please fill in all fields.")
                    else:
                        # Prevent duplicate Roll Number
                        if roll_no in marked_df["Roll_no"].values:
                            st.error("This Roll Number is already bound to another device!")
                        else:
                            new_row = pd.DataFrame([{"Roll_no": roll_no, "device_id": device_id}])
                            marked_df = pd.concat([marked_df, new_row], ignore_index=True)
                            marked_df.to_csv(MARKED_FILE, index=False)
                            st.success(f"Registered successfully as {roll_no}")
                            st.rerun()

            #================= Other Tabs and Attendance Logic =================
            # You can add the rest of your student/CR/chat/permission tabs below here
            # For each tab, use the value of device_id and the permanent roll_no lookup as your identity key
            # Example stub:
            def get_session_id():
                ctx = get_script_run_ctx()
                if ctx and ctx.session_id:
                    return hashlib.sha256(ctx.session_id.encode()).hexdigest()
                else:
                    return hashlib.sha256(str(datetime.now()).encode()).hexdigest()
            DB_PATH =  'attendance.sqlite'
            ATTENDANCE_FILE = 'attendance.csv'
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
            rep_password = 'REP123'
            passwords = {rn: 'In' + rn + '@123' for rn in options} 
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
            tab1, tab2, tab3 = st.tabs(['Student/CR', 'Chat', 'Ask Permission'])
            with tab1:
                st.title('CSE Attendance Checker!!')
                st.header('Enter the following details:')
                try:
                    roll_no_tab2 = saved_roll
                except:
                    roll_no_tab2 = None
                if roll_no_tab2 and roll_no_tab2 in options:
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
                            try:
                                import streamlit as st
                                import datetime
                                import pandas as pd
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
                                        # st.write(f"Selected {selected_month}")
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
                                    with col2:
                                        col = st.columns(1)
                                        attendance_data = pd.DataFrame({'Date':[selected_date_str], 'Presenties':[present_list], 'Absenties':[absent_list]}) 
                                        # attendance_data = pd.read_csv(attendance_data)
                                        cr_csv_data=attendance_data.to_csv(index=False).encode('utf-8')
                                        st.download_button(label='Download Report', data=cr_csv_data, mime='text/csv', key='CR_Download', file_name=ATTENDANCE_FILE)
                                else:
                                    st.error('Wrong Rep Password!')

                            if st.button('Reset Attendance for Selected Date') and rep_pass == rep_password:
                                attendance_df = attendance_df[attendance_df['Date'] != selected_date_str]
                                attendance_df.to_csv('ATTENDANCE_FILE', index=False)
                                st.info(f"Attendance reset for {selected_date_str}!")
                else:
                    st.error("Please enter a valid roll number.")

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

            with tab2:
                try:
                    roll_no_tab3 = saved_roll 
                except:
                    roll_no_tab3 = None
                if roll_no_tab3 and roll_no_tab3 in options:
                    if is_bound_to_another_device(roll_no_tab3) and checking(roll_no_tab3):
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


            with tab3:

                PERMISSIONS_FILE = "permissions.csv"
                no_of_days = 0
                try:
                    Roll_no = saved_roll
                except:
                    Roll_no = None
                
                if Roll_no and Roll_no in options:

                    if (is_bound_to_another_device(Roll_no) and checking(Roll_no)):
                            st.error(f"ERROR: Roll number {Roll_no} is enrolled with another device. Access denied.")
                    else:
                            if st.session_state['user'] is not None and roll_no_tab3 != st.session_state['user']:
                                st.error("Provide the Valid Roll NO first!")
                            else:
                                no_of_days = st.slider("Select the no of days: ", min_value=1, max_value=10)
                                if not os.path.exists(PERMISSIONS_FILE):
                                        per_df = pd.DataFrame(columns=['Roll_no', 'Reason', 'Granted', "No_of_days"])
                                        per_df.to_csv(PERMISSIONS_FILE, index=False)
                                else:
                                        per_df = pd.read_csv(PERMISSIONS_FILE)
                                    
                                issue = st.chat_input("Enter your issue: ",key="permission_input")
                                if issue:
                                        # Sanitize input to prevent HTML injection
                                        sanitized_issue = html.escape(issue)
                                        sanitized_days = html.escape(str(no_of_days))
                                        new_msg = pd.DataFrame({"Roll_no": [roll_no_tab3], "Reason": [sanitized_issue], "No_of_days": [sanitized_days], "Granted": ['Pending']})
                                        per_df = pd.concat([per_df, new_msg], ignore_index=True)
                                        per_df.to_csv(PERMISSIONS_FILE, index=False)
                                    
                                    # Sort by index for chronological order (assuming index represents time)
                                from streamlit_autorefresh import st_autorefresh
                                st_autorefresh(interval=1000, key='student_refresh')
                                per_df = per_df.sort_index()
                                if Roll_no in per_df['Roll_no'].values:
                                    if (per_df.loc[per_df['Roll_no'] == Roll_no, 'Granted'] == 'Pending').any():
                                        st.warning(f"😥😥Your case is still in **PENDING**")
                                    elif per_df.loc[per_df['Roll_no'] == Roll_no, 'Granted'].any():
                                        st.success('🎉🎉Congrats! your leave is: **APPROVED**')
                                        st.markdown(
                                            "<audio autoplay><source src='https://www.soundjay.com/buttons/button-3.mp3' type='audio/mpeg'></audio>",
                                            unsafe_allow_html=True
                                        )
                                    else:
                                        st.markdown(
                                            "<audio autoplay><source src='https://www.soundjay.com/buttons/button-3.mp3' type='audio/mpeg'></audio>",
                                            unsafe_allow_html=True
                                        )
                                        st.error('😑😑The Mentor has **MIGHT BE REJECTED** your leave!!')
                                else:
                                    st.write("You didn't raise any permission request!!")
                                # if st.button("Reset"):
                                #         per_df = pd.DataFrame(columns=per_df.columns)
                                #         per_df.to_csv(PERMISSIONS_FILE, index=False)
                                #         st.rerun()
                                # if st.button("REFRESH"):
                                #         st.rerun()
                else:
                    st.error("Please enter a valid roll number.")
            st.caption(f"Device ID: {device_id}")            


    elif page == "About":
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


    elif page == "Settings":
        st.header("Change password if you want!!")
        prev_pass=st.text_input("Enter previous password: ")
        curr_pass=st.text_input("Enter current password: ")
        if prev_pass == 'RAAM':
            if not os.path.exists("passwords.csv"):
                password_df=pd.DataFrame(columns=['device_id', 'password'])
                password_df.to_csv("passwords.csv")
            password_df = pd.read_csv("passwords.csv")
            # password_df=pd.concat([password_df, pd.DataFrame({'device_id': device_id})])
elif primary_input == "":
    st.warning("YOU STILL DIDN'T ENTER ANY THING!!")   
else:
    st.error("YOU'RE NOT ALLOWED!!")
# st.caption('~ A Website done by Raamanand.')
