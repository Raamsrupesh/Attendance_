import streamlit as st 
import pandas as pd 
import numpy as np 
import hashlib 
import sqlite3 
import uuid 
import os 
from datetime import datetime as datime
import csv
from random import choice
import html

MENT_PASSWORD = 'mentor_password.csv'  # 🔐
ROLL_DEVICE_STU_DB = 'studentrolldevice.db'  # 📱
ATTENDANCE_DB = 'attendance.db'  # 📊 
REP_PASS = 'rep_password.csv'  # 👑
PERMISSIONS_DB = 'permissions.db'  # 📜
GOOD_NEWS = 'good_new.txt'  # 📢
FEEDBACK_FILE = 'feedback.csv'  # 💬
NAME_PASS_DB = 'name_pass.db'  # 👤
TODO_DB = 'todo.db'
MESSAGE_FILE = 'messages.csv'
MARKED_FILE = 'marked.csv'

np_co = sqlite3.connect(NAME_PASS_DB)
np_cr = np_co.cursor()
np_cr.execute("CREATE TABLE IF NOT EXISTS name_pass(id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR(100) NOT NULL, password VARCHAR(100) NOT NULL);")
np_co.commit()


def read():
    if os.path.exists(GOOD_NEWS):
        with open(GOOD_NEWS, mode='r', encoding='utf-8') as f:
            return f.read()
    return ""  # 📄

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
                📢 {read()}
            </marquee>
            </div>
            """,
            unsafe_allow_html=True
    )
        st.markdown("<br><br>", unsafe_allow_html=True)

if "user_auth" not in st.session_state:
    st.session_state['user_auth'] = False 

if not st.session_state['user_auth']:
    st.title("🔐  SignIn/Register")  # 🔐
    action = st.radio("🎯 Select Action", ['SignIn', 'Register'], index=0)
    user_name = st.text_input("👤 Enter User Name: ")
    user_pass = st.text_input("🔑 Enter Password", type='password')
    if st.button("🚀 PROCEED"):
        if action == "SignIn":
            np_cr.execute("SELECT password FROM name_pass WHERE name = ?", (user_name,))
            act_pd = np_cr.fetchone()
            if act_pd is None:
                st.error("❌ User NOT FOUND")
            elif act_pd[0] == user_pass:
                st.session_state.user_auth = True 
                st.session_state.user_name = user_name
                st.success("✅ Login Successful!")
            else:
                st.error("❌ WRONG ENTRY!")
        elif action == "Register":
            np_cr.execute("SELECT name FROM name_pass;")
            all_names = [row[0] for row in np_cr.fetchall()]
            if user_name in all_names:
                st.warning("⚠️ This username already exists!")
            else:
                if user_pass != "":
                    np_cr.execute("INSERT INTO name_pass(name, password) VALUES(?,?);", (user_name, user_pass))
                    np_co.commit()
                    st.success("🎉 Now continue by changing the mode into **SignIn**")
                else:
                    st.warning("⚠️ Please enter valid password")

else:
    st.logo("https://user-gen-media-assets.s3.amazonaws.com/seedream_images/8b141d02-3bc5-4dbe-a05a-bd37908dafe6.png", size="medium")     
    st.sidebar.image("https://user-gen-media-assets.s3.amazonaws.com/seedream_images/b2c7b8bb-bca9-47d4-be77-c5c11c3378dd.png")

    CLASS_ROLL_NUMBERS = [
                    'X1', 'X2', 'X3', 'X4', 'X5', 'X6', 'X7', 'X8', 'X9', 'Y0', 'Y1', 'Y2', 'Y3',
                    'Y4', 'Y5', 'Y6', 'Y7', 'Y8', 'Y9', 'Z0', 'Z1', 'Z2', 'Z3', 'Z4', 'Z5', 'Z6',
                    'Z7', 'Z8', 'Z9', 'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'AG', 'AH', 'AI', 'AJ',
                    'AK', 'AL', 'AM', 'AN', 'AO', 'AP', 'AQ', 'AR', 'AS', 'AT', 'AU', 'AV', 'AW',
                    'AX', 'AY', 'AZ', 'BA', 'BB', 'BC', 'BD', 'BE', 'BF', 'BG', 'BH', 'BI', 'BJ',
                    'BK'
    ]

    conn = sqlite3.connect(ROLL_DEVICE_STU_DB)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS studentrolldevice(id INTEGER PRIMARY KEY AUTOINCREMENT, rollno VARCHAR(2) NOT NULL, device_id VARCHAR(200) NOT NULL);")
    conn.commit()

    at_con = sqlite3.connect(ATTENDANCE_DB)
    at_cur = at_con.cursor()
    at_cur.execute("CREATE TABLE IF NOT EXISTS attendance(id INTEGER PRIMARY KEY AUTOINCREMENT, rollno VARCHAR(2) NOT NULL, date_pre date NOT NULL, time_pre time NOT NULL);")
    at_con.commit()

    per_con = sqlite3.connect(PERMISSIONS_DB)
    per_cur = per_con.cursor()
    per_cur.execute("CREATE TABLE IF NOT EXISTS permissions(id INTEGER PRIMARY KEY AUTOINCREMENT, date_per date NOT NULL, rollno VARCHAR(2) NOT NULL, cause VARCHAR(700) NOT NULL, no_of_days INTEGER NOT NULL, granted VARCHAR(3) NOT NULL);")
    per_con.commit()

    if not os.path.exists(MENT_PASSWORD):
        with open (MENT_PASSWORD , mode='w', newline="") as f:
            f.write(hashlib.sha256(f'{chr(84)+chr(69)+chr(65)+chr(67)+chr(82)}'.encode()).hexdigest())
    if not os.path.exists(REP_PASS):
        with open (REP_PASS, mode='w', newline="") as f:
            f.write(hashlib.sha256(f'{chr(82)+chr(69)}P{chr(ord("1"))+chr(ord("2"))+chr(ord("3"))}'.encode()).hexdigest())
    if not os.path.exists(FEEDBACK_FILE):
        feedback_df = pd.DataFrame(columns=['feed', 'gb', 'appleation'])
        feedback_df.to_csv(FEEDBACK_FILE, index=False)
    feedback_df = pd.read_csv(FEEDBACK_FILE)
    with open (MENT_PASSWORD, mode="r", newline="") as f:
        teach_pass = f.read()


    if "student_logged_in" not in st.session_state:
        st.session_state.student_logged_in = False
    if "student_roll" not in st.session_state:
        st.session_state.student_roll = None

    who = st.sidebar.radio("🧭 Navigate to: ", ['👨‍🏫 Mentor', '🧑‍🎓 Student', '👨‍🔬 Admin', '📢 NoticeBoard', '💬 Feedback', 'ℹ️ About', '🔧Settings', '📃ToDoList'], index = 1)
    
    if who == '👨‍🏫 Mentor':  
        st.header(f"👨‍🏫 Mentor Portal: ")
        ment_password = st.text_input("🔐 Enter Mentor Password: ", type='password')
        if hashlib.sha256(ment_password.encode()).hexdigest() == teach_pass:
            st.subheader(f"🙏 Welcome : {st.session_state.user_name}🙏")
            st.write("─" * 75)
            today_per_df = pd.read_sql(sql="SELECT date_per ,rollno , cause, no_of_days, granted  FROM permissions WHERE date_per LIKE ?",con=per_con ,params=(datime.now().strftime("%Y-%m-%d"),))
            if today_per_df[today_per_df['granted'] == 'NOT YET'].shape[0] != 0:
                st.toast(f"{today_per_df[today_per_df['granted'] == 'NOT YET'].shape[0]} permissions/Leave letters unseen!")
            st.subheader("Today's requests:")
            with st.form(f"Permissions updates{today_per_df.shape[0]}"):
                for j,i in today_per_df.iterrows():
                    if (i['granted'] == 'NOT YET') or (i['granted'] == '👁️ SEEN'):
                        val = st.radio(f"{i['rollno']}: {i['cause']}.Therfore I need leave for {i['no_of_days']}.", options=['👁️ SEEN', '✅ ACCEPTED', '❌ REJECTED'], index=0, horizontal=True, key=f"r_{i['rollno']}_{i['date_per']}",)
                    elif i['granted'] == '✅ ACCEPTED':
                        val = st.radio(f"{i['rollno']}: {i['cause']}.Therfore I need leave for {i['no_of_days']}.", options=['👁️ SEEN', '✅ ACCEPTED', '❌ REJECTED'], index=1, horizontal=True, key=f"r_{i['rollno']}_{i['date_per']}",)
                    elif i['granted'] == '❌ REJECTED':
                        val = st.radio(f"{i['rollno']}: {i['cause']}.Therfore I need leave for {i['no_of_days']}.", options=['👁️ SEEN', '✅ ACCEPTED', '❌ REJECTED'], index=2, horizontal=True, key=f"r_{i['rollno']}_{i['date_per']}",)
                    if st.form_submit_button("UPDATE"):
                        if val != i['granted']:
                            per_cur.execute("UPDATE permissions SET granted = ? WHERE rollno = ? AND date_per = ?;", (val, i['rollno'], i['date_per']))
                            per_con.commit()
            st.download_button(icon=':material/download:',label=f"Today's permissions", file_name=f"{datime.now().strftime('%Y-%m-%d')}", key = f"Mentor downloading {datime.now().strftime('%Y-%m-%d')}", data = pd.read_sql(sql="SELECT * FROM permissions WHERE date_per LIKE ?",con=per_con ,params=(datime.now().strftime("%Y-%m-%d"),)).to_csv(index=False), mime='text/csv')    
                # if i[5] == 'NOT YET':
                #     val = st.checkbox(f"{i[2]}: {i[3]}. Therfore I need leave for {i[4]} days.", value=False)
                #     if val == True:
                #         per_cur.execute("UPDATE permissions SET granted = 'Accepted' WHERE rollno = ?;", (i[2],))
                #         per_con.commit()
                #     if val == False:
                #         per_cur.execute("UPDATE permissions SET granted = 'REJECTED' WHERE rollno = ?;", (i[2],))
                #         per_con.commit()
                # elif i[5] == 'Accepted':
                #     val = st.checkbox(f"{i[2]}: {i[3]}. Therfore I need leave for {i[4]} days.", value=True)
                #     if val == False:
                #         per_cur.execute("UPDATE permissions SET granted = 'REJECTED' WHERE rollno = ?;", (i[2],))
                #         per_con.commit()
                # elif i[5] == 'REJECTED':
                #     val = st.checkbox(f"{i[2]}: {i[3]}. Therfore I need leave for {i[4]} days.", value=False)
                #     if val == True:
                #         per_cur.execute("UPDATE permissions SET granted = 'Accepted' WHERE rollno = ?;", (i[2],))
                #         per_con.commit()

            if st.button("🗑️ CLEAR PERMISSIONS"):
                per_cur.execute("DELETE FROM permissions;")
                per_con.commit()
                per_con.close()
            
            st.write("─" * 75)

            st.subheader("📊 Today's Attendance:")
            tea_pre, tea_abs = st.columns([2, 1])
            with tea_pre:
                tea_pre_df = pd.read_sql("SELECT rollno, time_pre FROM attendance WHERE date_pre = ?;", con = at_con, params=(datime.now().strftime("%Y-%m-%d"),))
                st.write(tea_pre_df)
            with tea_abs:
                tea_abs_df = []
                for i in CLASS_ROLL_NUMBERS:
                    if i not in tea_pre_df['rollno'].to_list():
                        tea_abs_df.append(i)
                tea_abs_df = pd.DataFrame(tea_abs_df, columns=['rollno'])
                t_abs = tea_abs_df['rollno'].isin(today_per_df.loc[today_per_df['granted'] == "✅ ACCEPTED"]['rollno'])
                def green_style(row):
                    if t_abs[row.name]:
                        return ['background-color: lightblue'] * len(row)
                    return [''] * len(row)
                styled_df = tea_abs_df.style.apply(green_style, axis=1)
                st.dataframe(styled_df, use_container_width=True)
        
            st.write("─" * 75)
            # Date, Roll NO, Time, P/A
            teach_date_ip = st.date_input("Enter the date to check attendance: ", value='today', help="Enter the date to Access the Attendance of that day", format="YYYY-MM-DD")
            teach_date_df = pd.read_sql("SELECT rollno, time_pre FROM attendance WHERE date_pre LIKE ?", con=at_con, params=(teach_date_ip,))
            down_data = pd.concat([pd.Series([teach_date_ip]).repeat(max(len(teach_date_df), len(tea_abs_df))).reset_index(drop=True).rename("Date"), teach_date_df['rollno'].rename("Presenties"), teach_date_df['time_pre'].rename("timeOfPresence"), tea_abs_df['rollno'].rename("Absenties")], axis=1)
            st.write(down_data)
            st.download_button("Download Attendance", data = down_data.to_csv(index=False), file_name=f"{datime.now().strftime('%Y-%m-%d')}Attendance", mime="text/csv", key="teacher_download", icon='📩')

        elif ment_password != "":
            st.error("Wrong Password! Contact **ADMIN**")
        elif ment_password == "":
            st.warning("Fill the password to access the portal!!")


    elif who == '🧑‍🎓 Student':
        # ================= STUDENT PORTAL MAIN =================
        from streamlit_cookies_controller import CookieController 
        controller = CookieController()

        # 1) Ensure cookies are initialized
        if not controller.getAll():
            st.warning("Waiting for cookies to initialize. Please reload the page once.")
            st.stop()

        # 2) Read or create device_id cookie
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

        # ================ MARKED CSV loading and saving =================
        if not os.path.exists(MARKED_FILE):
            pd.DataFrame(columns=["Roll_no", "device_id"]).to_csv(MARKED_FILE, index=False)
        marked_df = pd.read_csv(MARKED_FILE)

        # ================ Registration / Login UI =================
        registered_entry = marked_df.loc[marked_df["device_id"] == device_id]

        if not registered_entry.empty:
            # already bound device → auto login
            saved_roll = registered_entry.iloc[0]["Roll_no"]
            st.session_state['user'] = saved_roll
            st.success(
                f"🪪 {saved_roll} is permanently bound with this device."
            )
            st.text_input("🆔 Roll Number", value=saved_roll, disabled=True)
            # st.write(f"Device ID: {device_id}")
        else:
            # first time on this device → registration
            roll_no = st.selectbox("Enter your Roll Number:", CLASS_ROLL_NUMBERS)
            if st.button("**🔗 BIND PERMANENTLY**", type = 'primary'):
                if not roll_no:
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

        # If still no user in session_state, stop here
        if 'user' not in st.session_state or st.session_state['user'] is None:
            st.stop()

        # From here onwards, we have a valid logged-in student on this device
        user_roll = st.session_state['user']

        # ================= REST OF YOUR STUDENT PAGE =================
        # NOTE: from here, NEVER ask roll again; always use user_roll.

        st.subheader(f"🙏 Welcome {st.session_state.get('user_name', user_roll)} 🙏")
        # st.selectbox("🎫 Roll NO:", options=[user_roll], disabled=True)

        # Permission toast for today (your original logic adjusted to use user_roll)
        student_per_df = pd.read_sql(
            sql="SELECT granted, date_per, no_of_days FROM permissions "
                "WHERE date_per LIKE ? AND rollno = ? ORDER BY date_per DESC;",
            con=per_con,
            params=(f"{datime.now().strftime('%Y-%m-%d')}", user_roll)
        )
        if not student_per_df.empty and (student_per_df['granted'] == "✅ ACCEPTED").any():
            st.toast(
                f"✅ ACCEPTED on {student_per_df['date_per'].iloc[0]} "
                f"for {student_per_df['no_of_days'].iloc[0]} days.",
                icon="🧑‍🎓"
            )
        elif not student_per_df.empty and (student_per_df['granted'] == "❌ REJECTED").any():
            st.toast(
                f"❌ REJECTED on {student_per_df['date_per'].iloc[0]} "
                f"for {student_per_df['no_of_days'].iloc[0]} days.",
                icon="🧑‍🎓"
            )

        st1, st2, st3, st4, st5 = st.tabs(
            ['👤 Student/CR', '📜 AskPermission', '🏆 LeaderBoard','💬 Chat' ,'📈 PrevRecords']
        )

        # ------------ TAB 1: STUDENT / CR ------------
        with st1:
            st.header("🎯 Select the mode of entry ")
            a = st.radio("⚙️ options available: ", ['🧑 STUDENT', '👑 CR'])

            if a == "🧑 STUDENT":
                st.write("---")
                st.header("✅ Mark Your Presence")
                from streamlit_geolocation import streamlit_geolocation 
                location = streamlit_geolocation()
                st.write(f'📍 You are at {location["latitude"]} N and {location["longitude"]} S')
                try:
                    if (location['latitude'] > 18 and location['latitude'] < 19) and \
                    (location['longitude'] > 83 and location['longitude'] < 84):
                        at_cur.execute(
                            "SELECT rollno FROM attendance WHERE rollno = ? AND date_pre = ?",
                            (user_roll, datime.now().date())
                        )
                        if not at_cur.fetchone():
                            if st.button("✅ Mark Present"):
                                st.balloons()
                                at_cur.execute(
                                    "INSERT INTO attendance(rollno, date_pre, time_pre) VALUES (?,?,?);",
                                    (
                                        user_roll,
                                        datime.now().strftime("%Y-%m-%d"),
                                        datime.now().strftime("%H:%M:%S")
                                    )
                                )
                                at_con.commit()
                                st.success("🎉 Attendance Marked Successfully!")
                        else:
                            st.warning("⚠️ You have already marked the attendance today!!")
                    else:
                        st.error("❌ The location is not matching!!")
                except TypeError:
                    st.warning("📍 Click on the above location button")

                try:
                    with st.expander("📊 GET MONTHLY REPORT:", icon='📥'):
                        mon = st.radio(
                            "📅 SELECT MONTH: ",
                            ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN',
                            'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'],
                            index=datime.now().date().month-1
                        )
                        if mon == 'JAN':
                            mon = '01'
                            total_days = 31
                        elif mon == 'FEB':
                            mon = '02'
                            total_days = 29 if (datime.now().year % 4 == 0 and datime.now().year % 100 != 0) or (datime.now().year % 400 == 0) else 28
                        elif mon == 'MAR':
                            mon = '03'
                            total_days = 31
                        elif mon == 'APR':
                            mon = '04'
                            total_days = 30
                        elif mon == 'MAY':
                            mon = '05'
                            total_days = 31
                        elif mon == 'JUN':
                            mon = '06'
                            total_days = 30
                        elif mon == 'JUL':
                            mon = '07'
                            total_days = 31
                        elif mon == 'AUG':
                            mon = '08'
                            total_days = 31
                        elif mon == 'SEP':
                            mon = '09'
                            total_days = 30
                        elif mon == 'OCT':
                            mon = '10'
                            total_days = 31
                        elif mon == 'NOV':
                            mon = '11'
                            total_days = 30
                        elif mon == 'DEC':
                            mon = '12'
                            total_days = 31          

                        csv_data = pd.read_sql(
                            sql='''SELECT rollno as RollNo, date_pre as Date, time_pre as Time FROM attendance WHERE rollno = ? AND date_pre LIKE ?''',
                            con=at_con,
                            params=(user_roll, f"{datime.now().strftime('%Y-%m')}-%")
                        )
                        st.download_button(
                                label="Download Report",
                                data=csv_data.to_csv(index=False),
                                file_name=f'{user_roll}{mon}attendance.csv',
                                mime="text/csv",
                                icon="📥",
                                key=f"{user_roll}{mon}attendance"
                        )
                except:
                    st.error("Contact ADMIN")

                at_cur.execute(
                    '''SELECT COUNT(DISTINCT date_pre) FROM attendance WHERE (rollno = ?) AND (date_pre LIKE ?);''',
                    (user_roll, f"{datime.now().date().year}-{datime.now().date().month}-%")
                )
                total_present_days = at_cur.fetchall()
                # total_days from above expander scope; you may want to move this calculation earlier safely
                try:
                    percentage = (len(total_present_days) / (total_days - 4)) * 100
                    if percentage < 62:
                        st.error(f"📉 The attendance percentage is: {percentage}%")
                    elif percentage >= 63 and percentage < 75:
                        st.warning(f"📊 The attendance percentage is: {percentage}%")
                    else:
                        st.success(f"📈 The attendance percentage is: {percentage}%")
                except Exception:
                    st.error("Contact Admin")

            elif a == "👑 CR":
                with open(REP_PASS, 'r', newline="") as f:
                    act_cr = f.read()
                CR_pass = st.text_input(
                    "🔐 Enter CR Password: ",
                    placeholder='*******',
                    type='password'
                )
                if st.button("CHECK"):
                    if CR_pass == "":
                        st.warning("⚠️ Enter the CR password!")
                    elif hashlib.sha256(CR_pass.encode()).hexdigest() == act_cr:
                        st.write("---")
                        st.header(f"{datime.now().date()} Attendance: ")
                        pre, abs_col = st.columns([2, 1])
                        with pre:
                            st.subheader("Presenties: ")
                            pre_df = pd.read_sql(
                                sql="SELECT rollno as RollNO, time_pre as Time FROM attendance WHERE date_pre = ?;",
                                con=at_con,
                                params=(datime.now().strftime("%Y-%m-%d"),)
                            )
                            st.write(pre_df)

                        with abs_col:
                            st.subheader("Absenties: ")
                            absenties = []
                            for i in CLASS_ROLL_NUMBERS:
                                if i not in pre_df['RollNO'].to_list():
                                    absenties.append(i)
                            absenties = pd.DataFrame(absenties, columns=['rollno'])
                            abse = absenties['rollno'].isin(
                                pd.read_sql(
                                    'SELECT rollno FROM permissions WHERE date_per = ? AND granted = ?',
                                    per_con,
                                    params=(datime.now().strftime("%Y-%m-%d"),"✅ ACCEPTED")
                                )
                            )
                            abse = pd.concat([absenties, abse], axis=1, ignore_index=True)
                            st.write(abse)
                        csv_data_cr = pd.concat([pre_df, abse], axis=1, ignore_index=True)
                        st.download_button(
                            label="Download Today's Attendance",
                            data=csv_data_cr.to_csv(index=False),
                            file_name=f"{datime.now().strftime('%Y-%m-%d')}-Attendance.csv",
                            mime="text/csv",
                            key=f"{datime.now().strftime('%Y-%m-%d')}cr_present_download",
                            icon="⏬"
                        )
                    else:
                        st.error("❌ Wrong CR Password!!")         

        # ------------ TAB 2: ASK PERMISSION ------------
        with st2:
            st.write("─" * 50)
            st.header("📜 New Permission Letter")
            with st.form(
                key=f"{user_roll}{datime.now().date().day} Permission form",
                clear_on_submit=True
            ):
                no_of_days = st.slider(
                    "📅 Number of Days",
                    min_value=1/2,
                    max_value=20.0,
                    step=1.0
                )
                cause = st.text_area("📝 Enter the Reason: ")
                if st.form_submit_button(
                    "📤 SUBMIT",
                    help="After this you can't able to modify the number of days and cause"
                ):
                    per_cur.execute(
                        "INSERT INTO permissions(rollno, date_per, cause, no_of_days, granted) "
                        "VALUES (?,?,?,?,?);",
                        (
                            user_roll,
                            datime.now().strftime("%Y-%m-%d"),
                            cause,
                            no_of_days,
                            'NOT YET'
                        )
                    )
                    per_con.commit()
                    st.success("📤 Permission Request Submitted!")
            st.write("─" * 50)
            try:
                var = pd.read_sql(
                    "SELECT * FROM permissions WHERE rollno = ? ORDER BY date_per DESC",
                    per_con,
                    params=(user_roll,)
                )
                st.header("📊 Status:")
                if var.iloc[0]['granted'] == "REJECTED":
                    st.error(f"❌ The latest request of permission was: **{var.iloc[0]['granted']}**")
                elif var.iloc[0]['granted'] == "ACCEPTED":
                    st.success(f"✅ The latest request of permission was: **{var.iloc[0]['granted']}**")
                else:
                    st.info(f"⏳ The latest request of permission was: **{var.iloc[0]['granted']}**")
                st.write("─" * 50)
                st.header("📜 Your previous requests:")
                if not var.empty:
                    st.write(var)
                    st.download_button(
                        "Download Leave Letter",
                        key=f"{datime.now().strftime('%Y-%m-%d')}-{user_roll}-LL",
                        file_name=f"{datime.now().strftime('%Y-%m-%d')}-{user_roll}-LL.csv",
                        data=var.to_csv(index=False),
                        mime='text/csv',
                        icon='✉️'
                    )
                else:
                    st.write("📭 You didn't raise any permission request yet!!")
            except IndexError:
                st.info("No permissions asked yet!!")

        # ------------ TAB 3: LEADERBOARD ------------
        with st3:
            st.subheader(f"{datime.now().strftime('%B')} Leaderboard: ")
            leader_board_df = pd.read_sql(
                "SELECT rollno, COUNT(*) AS noOfPresenties, avg(time_pre) AS avgTime "
                "FROM attendance WHERE date_pre LIKE ? "
                "GROUP BY rollno ORDER BY noOfPresenties DESC, avgTime",
                con=at_con,
                params=(f'{datime.now().strftime("%Y-%m")}-%',)
            )
            st.dataframe(leader_board_df)
            st.download_button(
                label="Download Leader Board",
                file_name=f"{datime.now().month}monthLeaderboard.csv",
                data=leader_board_df.to_csv(index=False),
                mime='text/csv',
                key=f"{datime.now().month}{user_roll}LeaderboardDownload",
                icon=':material/download:'
            )

        # ------------ TAB 4: CHAT ------------
        with st4:
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
            background-color: #dcf8c6;
            color: black;
            border-top-left-radius: 0;
            text-align: left;
        }

        .right-bubble {
            align-self: flex-end;
            background-color: #add8e6;
            color: black;
            border-top-right-radius: 0;
            text-align: right;
        }
        </style>
        """, unsafe_allow_html=True)
            st.subheader("🗨️ Group chat")

            roll_no_tab3 = user_roll
            if roll_no_tab3 and roll_no_tab3 in CLASS_ROLL_NUMBERS:
                chat1, chat2, chat3 = st.tabs(['Messages', 'Polls', 'Files'])
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
            else:
                st.error("Please enter a valid roll number.")

        # ------------ TAB 5: PREV RECORDS ------------
        with st5:
            st.info("This will be certainly added after a period of time.....")
    
     
    elif who == '👨‍🔬 Admin':
            st.title("👨‍🔬 Admin Panel")
            def write(msg):
                with open(GOOD_NEWS, mode='w', encoding='utf-8') as f:
                    f.write(msg) 

            if st.session_state['device_id'] == '1f399fbb313d1aaabbfcf8265f53cca63aa13c9c3cbc4203b5a4791276d7ee3b':
                st.header("📢 Announcement Management")
                message = st.text_input(label = "📝 New Announcement:", placeholder='Enter your message...')
                if st.button("🔊 Publish Announcement"):
                    write(message)
                    st.success("✅ Announcement Published!")
                
                if st.button("🔇 Clear Announcement"):
                    write("")
                    st.success("✅ Announcement Cleared!")
                st.write("─" * 50)
                st.caption(f"Currently the representative password is:{None}")
                st.caption(f"Currently the Mentor password is:{None}")
                st.write("─" * 50)
                st.header("📊 System Statistics")
                try:
                    x,y,z=st.columns(3)
                    with x:
                        st.metric(f"👥 Total Students",len(CLASS_ROLL_NUMBERS))  
                    with y:
                        st.metric(f"✅ Registered Students",len(pd.read_sql(sql="SELECT count(DISTINCT rollno) FROM studentrolldevice;", con=conn)))
                    with z:
                        st.metric(f"📊 Today's Attendance", len(pd.read_sql("SELECT COUNT(rollno) FROM attendance WHERE date_pre = ?;", con = at_con, params=(datime.now().strftime("%Y-%m-%d"),))))
                except:
                    st.error("❌ Files not created yet!!")
                st.write("─" * 50)  
                try:
                    st.header("💬 User Feedbacks:")
                    feedback_df = pd.read_csv(FEEDBACK_FILE) 
                    for i,j in feedback_df.iterrows():
                        st.write(f"👤 {j[2]}: {j[0]}. Finally he gave: {j[1]}")
                except:
                    st.info("📭 No one has yet given the feedback!!")           
                st.write("─" * 50)
                st.header("🔧 System Maintenance")
                st.markdown("<br>", unsafe_allow_html=True)
                a_, b_, c_ = st.columns([4,4, 10])
                with a_:
                    if st.button("🗑️ Clear All Data", type='primary'):
                        per_cur.execute("DELETE FROM permissions;")
                        per_con.commit()
                        per_con.close()
                        pd.read_csv(FEEDBACK_FILE).iloc[0:0].to_csv(FEEDBACK_FILE,index=False)
                with b_:
                    if st.button("🧹 Clear cache"):
                        st.cache_data.clear()
                        st.rerun()
                st.write("---------------------------"*20)
                changed_rep = st.text_input("Change REP Password: ", type='password', placeholder="******")
                if st.button("Change REP"):
                    with open (REP_PASS, mode="w", newline="") as rep:
                        rep.write(hashlib.sha256(changed_rep.encode()).hexdigest())
                        st.success("Successfully changed representative password")

                changed_ment = st.text_input("Change Mentor Password: ", type='password', placeholder="******")
                if st.button("Change MENT"):
                    with open(MENT_PASSWORD, mode="w", newline="") as ment:
                        ment.write(hashlib.sha256(changed_ment.encode()).hexdigest())
                        st.success("Successfully changed Mentor password")
                st.write("─" * 50)
                _1, _2 = st.columns(2)
                with _1:
                    min_latrange = st.number_input("🌐 Enter latitude min range")
                    maxlatrange = st.number_input("🌐 Enter latitude max range")
                with _2:
                    min_lonrange = st.number_input("🌐 Enter longitude min range")
                    maxlonrange = st.number_input("🌐 Enter longitude max range")
                st.write("---")
                sql_admin_db = st.selectbox("Enter on which you want to perform queries: ", options=[f"{ATTENDANCE_DB} → attendance", f"{NAME_PASS_DB} → name_pass", f"{PERMISSIONS_DB} → permissions", f"{ROLL_DEVICE_STU_DB} → studentrolldevice", f"{TODO_DB} → todo(todo_pswd)"])
                query = st.text_area('Enter the query here: ', placeholder=f"SELECT * FROM attendance WHERE Roll NO = '{st.session_state.get('user')}';")
                oneormany = st.selectbox("One or Many outputs in output: ", options=['one', 'many'])
                
                if st.button("Execute", type='primary'):
                    st.write("---")
                    st.subheader("Output Console: ")
                    try:
                            if sql_admin_db == f"{ATTENDANCE_DB} → attendance":
                                at_con = sqlite3.connect(ATTENDANCE_DB)
                                at_cur = at_con.cursor()
                                at_cur.execute(query.lower())
                                
                                if oneormany == 'many':
                                        st.write(at_cur.fetchall())
                                elif oneormany == "one":
                                        st.write(at_cur.fetchone())
                                if 'insert' in query or 'update' in query or 'delete' in query:
                                        at_con.commit()
                                        at_con.close()
                            elif sql_admin_db == f"{NAME_PASS_DB} → name_pass":
                                np_co = sqlite3.connect(NAME_PASS_DB)
                                np_cr = np_co.cursor()
                                np_cr.execute(query.lower())
                                
                                if oneormany == 'many':
                                        st.write(np_cr.fetchall())
                                elif oneormany == "one":
                                        st.write(np_cr.fetchone())
                                if 'insert' in query or 'update' in query or 'delete' in query:
                                        np_co.commit()
                                        np_co.close()
                            elif sql_admin_db == f"{PERMISSIONS_DB} → permissions":
                                per_con = sqlite3.connect(PERMISSIONS_DB)
                                per_cur = per_con.cursor()
                                per_cur.execute(query.lower())
                                
                                if oneormany == 'many':
                                        st.write(per_cur.fetchall())
                                elif oneormany == "one":
                                        st.write(per_cur.fetchone())
                                if 'insert' in query or 'update' in query or 'delete' in query:
                                        per_con.commit()
                                        per_con.close()
                            elif sql_admin_db == f"{ROLL_DEVICE_STU_DB} → studentrolldevice":
                                conn = sqlite3.connect(ROLL_DEVICE_STU_DB)
                                cur = conn.cursor()
                                cur.execute(query.lower())
                                
                                if oneormany == 'many':
                                        st.write(cur.fetchall())
                                elif oneormany == "one":
                                        st.write(cur.fetchone())
                                if 'insert' in query or 'update' in query or 'delete' in query:
                                        conn.commit()
                                        conn.close()
                            elif sql_admin_db == f"{TODO_DB} → todo(todo_pswd)":
                                todo_cn = sqlite3.connect(TODO_DB)
                                todo_cr = todo_cn.cursor()
                                todo_cr.execute(query.lower())
                                
                                if oneormany == 'many':
                                        st.write(todo_cr.fetchall())
                                elif oneormany == "one":
                                        st.write(todo_cr.fetchone())
                                if 'insert' in query or 'update' in query or 'delete' in query:
                                        todo_cn.commit()
                                        todo_cn.close()
                    except:
                        st.error("WRONG QUERY!!")
                st.write("---")



            else:
                st.error("🚫 Access denied. Admin privileges required.")

    elif who == "📢 NoticeBoard":
        try:
            st.title("🪧 NOTICE BOARD")
            this_month = datime.now().date().month 
            leader_board_df = pd.read_sql(f"SELECT rollno, COUNT(*) AS noOfPresenties, avg(time_pre) AS avgTime FROM attendance WHERE date_pre LIKE '{datime.now().date().year}-{this_month}-%' GROUP BY rollno ORDER BY noOfPresenties DESC, avgTime", con=at_con)
            st.subheader('🏆 This month the lead was:', leader_board_df.iloc[0])
            st.dataframe(leader_board_df)
        except:
            st.info("📭 No significant highlights are available!!")

    elif who == "💬 Feedback":
        st.title("💬 Feedback Form")
        st.write("─" * 50)
        st.subheader("Drop your valuable feedback here (if any)!")
        with st.form(key=f"{st.session_state['user']}Feedbackform"):
            appleation = st.text_input("👤 How are you liked to be appeleated as: ")
            feed = st.text_area("💭 Drop your feedback here")
            gb = st.radio("⭐ How was this?", options=['🔧 Need Improvement','🆗 OK', '😊 Satisfied', '🥳 Best'], horizontal=True, index = 2)

            if st.form_submit_button("📤 SUBMIT"):
                if appleation == "":
                    appleation = None 
                if feed == "" or gb == "" :
                    st.warning("⚠️ **Kindly fill feedback!!**")
                else:
                    new_row = pd.DataFrame(data={"feed": [feed], "gb": [gb], "appleation": [appleation]})
                    feedback_df = pd.concat([feedback_df, new_row], ignore_index=True, axis=0)
                    feedback_df.to_csv(FEEDBACK_FILE, index=False)
                    st.toast("🙏 Thank you, Your feedback is too much valuable for us!!", icon="⭐", duration='long')

        st.write("─" * 50)

    elif who == "ℹ️ About":
                from datetime import datetime

                APP_NAME = "Presaloc Pro"
                VERSION = "v2.0"
                DEVELOPER = "Saketh (Rupesh)"
                LAST_UPDATE = datetime(2025, 10, 27)

                about_header = f"""
                # 🎉 Welcome to **{APP_NAME}** app!

                🔒 A professional system designed to verify and secure attendance across classes (students, CRs, mentors, admin), all with advanced, modern technology and strict validation.
                
                ---
                🆕 Updated Recently on: {LAST_UPDATE}\n
                Welcome to my advanced, location-based attendance management platform—engineered to deliver reliable, secure, and automated attendance for educational institutions and organizations.
                """

                st.markdown(about_header)
                st.subheader("✨ Advanced Features")
                st.markdown(
                """
                - **📍 Smart Location Validation:** Ensures users are at authorized physical locations before marking attendance (uses HTML5 Geolocation API).
                - **🔐 Role-Based Security:** Custom access control for students, admins, and supervisors with encrypted session tokens.
                - **📊 Real-Time Analytics:** Visual dashboards, attendance statistics, and downloadable reports.
                - **🛡️ Proxy Prevention:** Strict geolocation and session checks to block fraudulent or duplicate entries.
                """
                )
                st.error("⚠️ **One Time Registration:** This feature will not allow any user to use another user's details. And once registered to a device, that very device owner could only use those details.")
                

                st.write("─" * 50)
                st.info("💡 Driven by a passion for building robust, real-world solutions for education and organizations.")

                st.metric(label="📱 App Version", value="v2.0", delta="+1 new feature")
                st.metric(label="👥 Active Users", value="000", delta="+2 this week")

                tab1, tab2 = st.tabs(["📋 Overview", "⚙️ Technical Details"])
                with tab1:
                    st.markdown("""
                    Welcome to our advanced, location-based attendance platform.
                    - **📍 Location Validation**
                    - **📊 Security & Analytics**
                    - **🔐 Role-based access**
                    """)
                with tab2:
                    st.subheader("🛠️ Technology Stack")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(
                            """
                            - 🐍 Python 3.13+
                            - 🌊 Streamlit
                            - 🗄️ SQLite (Data Storage)
                            - 🌐 HTML5 Geolocation
                            """
                            )
                    with col2:
                        st.markdown(
                            """
                            - 📈 Pandas (Data Handling)
                            - 🔐 Secure Session Management
                            - 📱 Responsive Web UI
                            - ⚡ Real-time Data Analytics
                            """
                            )

                with st.expander("👨‍💻 Meet the Developer"):
                    st.write("✨ Created by Saketh (Rupesh), a student developer passionate about practical AI solutions.")

                st.download_button("📖 Download App Manual", """~ A Website made by Saketh (Rupesh).""", file_name="manual.txt")


    elif who == "🔧Settings":
        st.title("Settings Panel: ")
        st.write("---")
        st.header("Change password: ")
        with st.form(key = "Changing and modifying pswd"):
            name = st.text_input("Enter your name: ", placeholder='E.g: GARUD')
            pre_pswd = st.text_input("Enter the Previous password:", placeholder="******", type='password')
            mod_pswd = st.text_input("Enter the modified password:", placeholder="******", type='password')
            np_cr.execute("SELECT * FROM name_pass WHERE name = ? AND password = ?", (name, pre_pswd))
            if st.form_submit_button("CHANGE PASSWORD", type='primary'):
                if np_cr.fetchone() is not None:
                    np_cr.execute("UPDATE name_pass SET password = ? WHERE name = ?", (mod_pswd, name))
                    np_co.commit()
                    st.success("Password has successfully changed!")
                else:
                    st.error("No user **EXISTS**!!")
        st.write("---")
        st.write(f"Device ID: {st.session_state.get('device_id')}")
    
    elif who == "📃ToDoList":
        todo_pswd = st.text_input(type='password', label='Name your TodoList: ', placeholder="******")
        todo_cn = sqlite3.connect(TODO_DB)
        todo_cr = todo_cn.cursor()
        if todo_pswd == "":
                st.warning("First name your TodoList ")
        elif('todo'+todo_pswd in todo_cr.fetchall()):
                st.error("Name is aldready taken, try another one!")
        else:
                todo_cr.execute(f"CREATE TABLE IF NOT EXISTS todo{todo_pswd}(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, status VARCHAR(12) NOT NULL, tasks VARCHAR(2000));")
                todo_cn.commit() 
                st.write("---")
                todo_df = pd.read_sql(f"SELECT * FROM todo{todo_pswd};", con=todo_cn)
                st.subheader("To Do List:")

                for i,j in todo_df.iterrows():
                    tododis, tododel = st.columns([10,1])
                    with tododis:
                        if j[1] == "❌":
                            c = st.checkbox(f"{j[2]}", value=False, key = str(j['id']))
                        elif j[1] == '✅':
                            c = st.checkbox(f"{j[2]}", value=True, key = str(j['id']))
                        if c:
                            todo_cr.execute(f"UPDATE todo{todo_pswd} SET status = '✅' WHERE tasks = ?;", (j[2],))
                            todo_cn.commit()
                        else:
                            todo_cr.execute(f"UPDATE todo{todo_pswd} SET status = '❌' WHERE tasks = ?;", (j[2],))
                            todo_cn.commit()
                    with tododel:
                        if st.button("🗑️", key=f"del_{j['id']}"):  # Unique key with 'del_' prefix + ID
                            todo_cr.execute(f"DELETE FROM todo{todo_pswd} WHERE id = ?", (j['id'],))
                            todo_cn.commit()
                            st.rerun()
                            # todo_cn.close()
                if st.button("🗑️ Clear ALL"):
                    todo_cr.execute(f"DELETE FROM todo{todo_pswd};")
                    todo_cn.commit()


                st.write("---")

                with st.form("To do add task element", clear_on_submit=True):
                    task = st.text_input("Add Task: ", placeholder='E.g: Do Homechores')
                    if st.form_submit_button("ADD"):
                        if task != "":
                            todo_cr.execute(f"INSERT INTO todo{todo_pswd}(status, tasks) VALUES(?,?);", ('❌', task))
                            todo_cn.commit()
                            st.rerun()
                        else:
                            st.warning("Enter a valid chore!!")
                st.write("---")

    st.caption("✨ ~An app by Saketh (Rupesh), accomplished in 5-6 days & completed prior to 27th October 2025.")



# import sqlite3 

# conn = sqlite3.connect("students.db")
# cur = conn.cursor()

# cur.execute("""
#     CREATE TABLE IF NOT EXISTS students_attendance(
#         id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
#         Name VARCHAR(300) NOT NULL,
#         class INT NOT NULL            
#     );
# """)

# print("WELCOME TO CLG MANAGER APP\n")
# def main():
#     while True:
#         print("""
#             1. List STUDENTS
#             2. Add STUDENTS
#             3. UPDATE STUDENTS
#             4. DELETE STUDENTS
#             5. EXIT
#         """)
#         choice = int(input("Choose any of the above: "))
#         if choice == 1:
#             cur.execute("SELECT * FROM students_attendance")
#             for i in cur.fetchall():
#                 print(i)

#         elif choice == 2:
#             name = input("Enter the Name:")
#             clas = int(input("Enter the class : "))

#             cur.execute("INSERT INTO students_attendance(name, class) VALUES(?, ?)", (name, clas))
#             conn.commit()

#         elif choice == 3:
#             id = int(input("Enter student id: "))
#             name = input("Enter the Name:")
#             clas = int(input("Enter the class: "))

#             cur.execute("UPDATE students_attendance SET name = ?, class = ? WHERE id = ?", (name, clas, id))
#             conn.commit()

#         elif choice == 4:
#             id = int(input("Enter student id: "))
#             cur.execute("DELETE FROM4 students_attendance WHERE id = ?", (id,))
#             print("SUCCESSFULLY DELETED!!")
#             conn.commit() 

#         elif choice == 5:
#             break 
#         else:
#             print("**INVALIID CHOICE**")
        
#     print("**Thank you for visiting our app**")
#     conn.close()

# if "__main__" == __name__:
#     main()


#  =====================================================================================================


# import hashlib
# import os 
# CRPASS = 'crpassword.txt'


# """if not os.path.exists(CRPASS):
#     with open (CRPASS, mode = "w", newline="") as f:
#         f.write('REPTE')"""

# with open (CRPASS, mode = "r", newline="") as f:
#     user_pass = f.read()
# hashed_password = hashlib.sha256(user_pass.encode()).hexdigest()


# # print("USER: ", user_pass)
# entered_pswd = input("Enter CR password: ")
# entered_pswd = hashlib.sha256(entered_pswd.encode()).hexdigest()
# # print("FIRST PASS:", hashed_password)
# if entered_pswd == hashed_password:
#     print("You are welcome!!")
# else:
#     print("Sorry you are not allowed since the password is not matching!!")

# =====================================================================================================================================




# import pandas as pd

# # Create first DataFrame
# df1 = pd.DataFrame({
#     'ID': [1, 2, 3, 4, 5],
#     'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
#     'Value': [10, 20, 30, 40, 50]
# })

# # Create second DataFrame
# df2 = pd.DataFrame({
#     'ID': [3, 4, 6, 7, 8],
#     'appeleation': ['Charlie', 'David', 'Frank', 'Grace', 'Henry'],
#     'Value': [30, 40, 60, 70, 80]
# })







# import streamlit as st
# st.write(pd.concat([df1, df1['Name'].isin(df2['appeleation'])], axis=1, ignore_index=True))



