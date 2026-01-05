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
    st.title("🔓 SignIn/Register")  # 🔐
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
            # try:
            #     st.write(today_per_df)
            # except:
            #     st.toast(f"🙏 Welcome, {st.session_state.user_name}", icon="👨‍🏫")
            st.subheader(f"🙏 Welcome : {st.session_state.user_name}🙏")
            st.write("─" * 75)
            st.subheader("📋 Permissions for Today:")
            today_per_df = pd.read_sql(
                "SELECT * FROM permissions WHERE date_per = ?",
                con=per_con,
                params=(datime.now().strftime("%Y-%m-%d"),),
            )

            status_options = ['👁️ SEEN','✅ ACCEPTED', '❌ REJECTED']

            for i, row in today_per_df.iterrows():
                # Decide default based on current DB value
                granted = row['granted']
                if granted in status_options:
                    default_index = status_options.index(granted)
                else:  # e.g. 'NOT YET'
                    default_index = 0  # SEEN

                stu_per = st.radio(
                    label=f"📄 {row['rollno']}: {row['cause']}. Therefore I need a leave for {row['no_of_days']} days",
                    options=status_options,
                    horizontal=True,
                    index=default_index,
                    key=f"perm_{datime.now().strftime('%Y-%m-%d')}_{row['rollno']}"
                )

                # Only update DB if changed
                if stu_per != granted:
                    per_cur.execute(
                        "UPDATE permissions SET granted = ? WHERE (date_per = ?) AND (rollno = ?);",
                        (stu_per, datime.now().strftime("%Y-%m-%d"), row['rollno']),
                    )
                    per_con.commit()
            st.download_button(label="Permissions Report", data=today_per_df.to_csv(index=False),file_name=f"{datime.now().date()}_permissions_report", key=f"{datime.now().date()}-{st.session_state['user_name']}-permissions report", mime='text/csv', icon=':material/download:')


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
            st.text_input("Roll Number", value=saved_roll, disabled=True)
            st.write(f"Device ID: {device_id}")
        else:
            # first time on this device → registration
            roll_no = st.selectbox("Enter your Roll Number:", CLASS_ROLL_NUMBERS)
            if st.button("Register"):
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
        st.selectbox("🎫 Roll NO:", options=[user_roll], disabled=True)

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
                f"for {student_per_df['no_of_days'].iloc[0]}",
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
                st.write("─" * 50)
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
                            index=datime.now().month + 1
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
                            sql='SELECT rollno as Roll NO,date_pre as Date,time_pre as Time '
                                'FROM attendance WHERE rollno = ? AND date_pre LIKE ?',
                            con=at_con,
                            params=(user_roll, f"{datime.now().strftime('%Y-%m')}-%")
                        )
                        st.download_button(
                            "Download Report",
                            data=csv_data.to_csv(index=False),
                            file_name=f'{user_roll}{mon}attendance.csv',
                            mime="text/csv",
                            icon="📥"
                        )
                except:
                    pass 

                at_cur.execute(
                    'SELECT COUNT(DISTINCT date_pre) FROM attendance '
                    'WHERE (rollno = ?) AND (date_pre LIKE ?);',
                    (user_roll, f"{datime.now().year}-{datime.now().month}-%")
                )
                total_present_days = at_cur.fetchone()[0]
                # total_days from above expander scope; you may want to move this calculation earlier safely
                try:
                    percentage = (total_present_days / (total_days - 4)) * 100
                    if percentage < 62:
                        st.error(f"📉 The attendance percentage is: {percentage}%")
                    elif percentage >= 63 and percentage < 75:
                        st.warning(f"📊 The attendance percentage is: {percentage}%")
                    else:
                        st.success(f"📈 The attendance percentage is: {percentage}%")
                except Exception:
                    pass

            elif a == "👑 CR":
                with open(REP_PASS, 'r', newline="") as f:
                    act_cr = f.read()
                CR_pass = st.text_input(
                    "🔐 Enter CR Password: ",
                    placeholder='*******',
                    type='password'
                )
                if CR_pass == "":
                    st.warning("⚠️ Enter the CR password!")
                elif hashlib.sha256(CR_pass.encode()).hexdigest() == act_cr:
                    st.write("---")
                    st.header(f"{datime.now().date()} Attendance: ")
                    pre, abs_col = st.columns([2, 1])
                    with pre:
                        st.subheader("Presenties: ")
                        pre_df = pd.read_sql(
                            sql="SELECT rollno, time_pre FROM attendance WHERE date_pre = ?;",
                            con=at_con,
                            params=(datime.now().strftime("%Y-%m-%d"),)
                        )
                        st.write(pre_df)

                    with abs_col:
                        st.subheader("Absenties: ")
                        absenties = []
                        for i in CLASS_ROLL_NUMBERS:
                            if i not in pre_df['rollno'].to_list():
                                absenties.append(i)
                        absenties = pd.DataFrame(absenties, columns=['rollno'])
                        abse = absenties['rollno'].isin(
                            pd.read_sql(
                                'SELECT rollno FROM permissions WHERE date_per = ?',
                                per_con,
                                params=(datime.now().strftime("%Y-%m-%d"),)
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
            st.write("Prev records logic here (your original code)")
    
     
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
                if st.button("🗑️ Clear All Data", type="secondary"):
                    per_cur.execute("DELETE FROM permissions;")
                    per_con.commit()
                    per_con.close()
                    pd.read_csv(FEEDBACK_FILE).iloc[0:0].to_csv(FEEDBACK_FILE,index=False)
                st.write("─" * 50)
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
                if st.button("🧹 Clear cache"):
                    st.cache_data.clear()
                    st.rerun()
                st.write("---")
                sql_admin_db = st.selectbox("Enter on which you want to perform queries: ", options=[f"{ATTENDANCE_DB} -> attendance", f"{NAME_PASS_DB} -> name_pass", f"{PERMISSIONS_DB} -> permissions", f"{ROLL_DEVICE_STU_DB} -> studentrolldevice", f"{TODO_DB} -> todo(todo_pswd)"])
                query = st.text_area('Enter the query here: ', placeholder=f"SELECT * FROM attendance WHERE Roll NO = '{st.session_state.get('user')}';")
                oneormany = st.selectbox("One or Many outputs in output: ", options=['one', 'many'])
                
                if st.button("Execute", type='primary'):
                    st.write("---")
                    st.subheader("Output Console: ")
                    try:
                            if sql_admin_db == f"{ATTENDANCE_DB} -> attendance":
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
                            elif sql_admin_db == f"{NAME_PASS_DB} -> name_pass":
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
                            elif sql_admin_db == f"{PERMISSIONS_DB} -> permissions":
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
                            elif sql_admin_db == f"{ROLL_DEVICE_STU_DB} -> studentrolldevice":
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
                            elif sql_admin_db == f"{TODO_DB} -> todo(todo_pswd)":
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


# #   ============================= IMPORTING LIBRARIES ===========================

# import pandas as pd
# import os
# from random import choice
# from datetime import datetime
# from streamlit.runtime.scriptrunner import get_script_run_ctx
# import hashlib
# import sqlite3
# import uuid
# import streamlit as st

# #   =========================================================================

# DB_PATH =  'attendance.sqlite'
# ATTENDANCE_FILE = 'attendance.csv'
# GOOD_NEWS = 'good_news.txt'
# PASS_FILE = 'password.csv'
# PERMISSIONS_FILE = 'permissions.csv' 
# MESSAGE_FILE = "messages.csv"
# MARKED_FILE = "marked.csv"
# POLLS = 'polls.csv'
# FEEDBACK_FILE = 'feedback.csv'

# #   =========================================================================
# TEA_CR_PASSWORD = f'{chr(84)+chr(69)+chr(65)+chr(67)+chr(82)}'
# rep_password = f'{chr(82)+chr(69)}P{chr(84)+chr(69)}'

# #   ===================== MARQUEE ===========================================
# def read():
#     if os.path.exists(GOOD_NEWS):
#         with open(GOOD_NEWS, mode='r', encoding='utf-8') as f:
#             return f.read()
#         return ""
# st.markdown("""
#         <style>
#             .block-container { padding-top: 2rem !important; margin-top:1.5rem !important;}
#             .custom-banner {
#                     position: fixed;
#                     top: 20;
#                     left: 0;
#                     width: 100vw;
#                     z-index: 1000;
#                     margin-bottom: 0.75rem !important;
#                     padding: 10px;
#                     display:flex;
#                     align-items: center !important;
#                     padding-top:1rem !important;
#             }
#             body { padding-top: 60px !important; }
#             </style>
#     """, unsafe_allow_html=True)
# if read() != "" and read() is not None:
#             st.markdown(
#                 f"""
#                 <div class='custom-banner' style='background:{choice(['white', 'lightyellow', 'skyblue', 'lightpink', 'lavender', 'mintcream', 'aliceblue', 'honeydew', 'azure', 'seashell', 'beige', 'mistyrose'])}; color:{choice(['black', 'darkblue', 'darkviolet', 'purple'])}; font-size:20px; border-radius:4px;font-family:{choice(['Arial', 'Verdana', 'Tahoma', 'Trebuchet MS', 'Georgia', 'Times New Roman', 'Impact', 'Comic Sans MS', 'Courier New', 'Lucida Console', 'Palatino Linotype', 'Garamond'])}'>
#                     <marquee behavior='scroll' direction='left' scrollamount='7'>
#                         {read()}
#                     </marquee>
#                 </div>
#                 """,
#                 unsafe_allow_html=True
# )
#             st.markdown("<br><br>", unsafe_allow_html=True)


# # count = st_autorefresh(interval=3500, key="fullautorefresh") 
# #   ================================================================================
# if not os.path.exists(PASS_FILE):
#     password_df = pd.DataFrame(columns=['user_name', 'pass'])
#     password_df.to_csv(PASS_FILE, index=False)
# password_df = pd.read_csv(PASS_FILE)

# if 'user_authenticated' not in st.session_state:
#     st.session_state.user_authenticated = False

# if 'user' not in st.session_state:
#     st.session_state.user = None 
# global saved_roll
# if not st.session_state.user_authenticated:
#     st.header("🔐 Sign In / Register")
#     action = st.radio("Select Action", ["Sign In", "Register"], index=0)
#     user_name = st.text_input("Enter your Name:", placeholder=f"E.g: GARUD").strip()
#     user_password = st.text_input("Enter Password:", type="password", placeholder='Type here....').strip()
# #   ========================== REGISTER TAB ==========================
#     if action == "Register":
#         if st.button("Register"):
#             if user_name in password_df['user_name'].to_list():
#                 st.error("This username is already taken. Try something else!")
#             elif user_name and user_password:
#                 new_row = pd.DataFrame({'user_name': [user_name], 'pass': [user_password]})
#                 password_df = pd.concat([password_df, new_row], ignore_index=True)
#                 password_df.to_csv(PASS_FILE, index=False)
#                 st.success("Successfully Registered! You can now Sign In.")
#             else:
#                 st.warning("Both fields are required.")

# #   ========================== SIGN IN TAB ==========================

#     elif action == "Sign In":
#         if st.button("Sign In"):
#             if user_name in password_df['user_name'].to_list():
#                 stored_password = password_df.loc[password_df['user_name'].str.strip() == user_name, 'pass'].values
#                 if stored_password.size > 0 and stored_password[0] == user_password:
#                     st.balloons()
#                     st.session_state.user_authenticated = True
#                     st.success("Successfully Signed In!")
#                     st.rerun() 
#                 else:
#                     st.error("Wrong password!")
#             elif user_name=="" and user_password == chr(82)+chr(97)+chr(97)+chr(109)+chr(97)+chr(110)+chr(97)+chr(110)+chr(100):
#                 st.balloons()
#                 st.session_state.user_authenticated = True 
#                 st.rerun() 
#             else:
#                 st.error("Username not found!")

# else:    
#     CLASS_ROLL_NUMBERS = [
#                     'X1', 'X2', 'X3', 'X4', 'X5', 'X6', 'X7', 'X8', 'X9', 'Y0', 'Y1', 'Y2', 'Y3',
#                     'Y4', 'Y5', 'Y6', 'Y7', 'Y8', 'Y9', 'Z0', 'Z1', 'Z2', 'Z3', 'Z4', 'Z5', 'Z6',
#                     'Z7', 'Z8', 'Z9', 'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'AG', 'AH', 'AI', 'AJ',
#                     'AK', 'AL', 'AM', 'AN', 'AO', 'AP', 'AQ', 'AR', 'AS', 'AT', 'AU', 'AV', 'AW',
#                     'AX', 'AY', 'AZ', 'BA', 'BB', 'BC', 'BD', 'BE', 'BF', 'BG', 'BH', 'BI', 'BJ',
#                     'BK'
#     ]

# #   ============================== LOGO BAR ========================================

#     st.logo("https://user-gen-media-assets.s3.amazonaws.com/seedream_images/8b141d02-3bc5-4dbe-a05a-bd37908dafe6.png", size="medium")    
#     st.sidebar.image("https://user-gen-media-assets.s3.amazonaws.com/seedream_images/b2c7b8bb-bca9-47d4-be77-c5c11c3378dd.png")

# #   ================================================================================

#     page = st.sidebar.radio("Navigate to:", ["🧑‍🏫 Mentor", "👨‍🎓 Student","👨‍🔬 Admin", "ℹ️ About", "⚙️ Settings", "🪧 NoticeBoard", "🧑‍🍼 Feedback"], index=1)
#     import html
#     from streamlit_autorefresh import st_autorefresh
#     st_autorefresh(interval=5000, key='fullautorefresh')

# #   =========================== MENTOR PORTAL =================================

#     if page == "🧑‍🏫 Mentor":   
#                 st.header("🧑‍🏫 Mentor Portal")
#                 ment_cr_pass = st.text_input("Enter Mentor Password:", type='password', placeholder='Type here....')
#                 if ment_cr_pass == TEA_CR_PASSWORD:
#                     try:
#                         per_df = pd.read_csv(PERMISSIONS_FILE) 
#                         st.write("---")
#                         st.subheader("📋 Permission Requests")
#                         for idx, row in per_df.iterrows():
#                             sanitized_roll = html.escape(str(row['Roll_no']))
#                             sanitized_msg = html.escape(str(row['Reason']))
#                             santized_for = html.escape(str(row['No_of_days'])) 
#                             key=f"checkbox_{idx}"
#                             if key not in st.session_state:
#                                 st.session_state[key] = bool(per_df.loc[per_df['Roll_no'] == sanitized_roll, 'Granted'].values[0])
#                                 st.toast(f"Recieved notification from {sanitized_roll}", icon="💬")
#                             if sanitized_roll in per_df['Roll_no'].tolist():
#                                 st.markdown(
#                                         "<audio autoplay><source src='https://www.soundjay.com/buttons/button-3.mp3' type='audio/mpeg'></audio>",
#                                         unsafe_allow_html=True
#                                 )
                                
#                             st.session_state['checked'] = st.checkbox(
#                                 f"{sanitized_roll}: {sanitized_msg}. So student is requesting leave for {santized_for} days",
#                                 key=f"checkbox_{idx}",
#                                 value=st.session_state[key]
#                             )
                            

#                             if st.session_state['checked']:
#                                 st.write(f"Accepted: {sanitized_roll}")
#                                 per_df.loc[per_df['Roll_no'] == sanitized_roll, 'Granted'] = True 
                                

#                             else:
#                                 per_df.loc[per_df['Roll_no'] == sanitized_roll, 'Granted'] = False  
#                             per_df.to_csv(PERMISSIONS_FILE, index=False)

#                         if st.button("🔁 Clear", key="Mentor_erasing"):
#                             per_df = pd.DataFrame(columns=per_df.columns)
#                             per_df.to_csv(PERMISSIONS_FILE, index=False)
#                             st.rerun()

#                     except FileNotFoundError or NameError:
#                         st.success("NO ONE YET ASKED PERMISSION AND NOTHING TO DOWNLOAD!!")
#                     try:
#                         csv_data=per_df.to_csv(index=False).encode('utf-8')
#                         st.download_button(
#                                 label="🗃️ Download Permissions Report",
#                                 data=csv_data,
#                                 file_name=PERMISSIONS_FILE,
#                                 mime="text/csv",
#                                 key="download-permissions"
#                         )
#                     except:
#                         pass 
#                     st.write("----------")
#                     date=st.date_input("Enter the date of attendance: ")
#                     st.subheader("📊 Attendance Report")
#                     x,y=st.columns(2)
#                     with x:
#                         try:
#                             st.subheader('Presenties: ')
#                             teach_df = pd.read_csv(ATTENDANCE_FILE)
                            
#                             present = teach_df.loc[teach_df['Date'] == date.strftime("%Y-%m-%d")] 
#                             present=(present.drop(columns=['SessionID', 'Date']))
#                             present=present.rename(columns={"Name":'Roll_NO'}) 
#                             st.write(present)
#                             present_list=teach_df['Name'].tolist() 
#                         except:
#                             st.info("Not one marked present yet!!") 
#                     with y:
#                         try:
#                             import numpy as np
#                             st.subheader("Absenties: ")
#                             absent = pd.DataFrame([i for i in CLASS_ROLL_NUMBERS if i not in present_list],columns=['Roll_NO'])
#                             teach_per_df = pd.read_csv(PERMISSIONS_FILE)
#                             teach_per_df=teach_per_df.drop(columns=['No_of_days', 'Reason']) 
#                             teach_per_df=teach_per_df.loc[teach_per_df['Granted'] == True]
#                             absent['Result'] = absent['Roll_NO'].isin(teach_per_df['Roll_no']) 
#                             st.write(absent) 
#                         except:
#                             st.info("No one yet marked attendance!!") 
#                     try:
#                         ment_attendance_df=(pd.concat([pd.Series(data=[str(date)] * max(len(present), len(absent))),present, absent], axis=1,ignore_index=True))
#                         ment_attendance_df=ment_attendance_df.rename(columns={0: 'Date', 1:'Presenties', 2: 'Absenties'})    
#                         ment_attendance_df=ment_attendance_df.to_csv(index=False).encode('utf-8')
#                         _,abc,_ = st.columns([1,2,1])
#                         with abc:
#                             # st.write(ment_attendance_df)
#                             st.download_button(label="📩 Download Attendance", file_name=f"{date}atttendance_report.csv", data=ment_attendance_df, mime='text/csv',key='DOWNLOAD_MENT_ATTENDANCE')
#                     except NameError:
#                         pass
#                 elif ment_cr_pass == "":
#                     st.warning("⚠️ Please enter the correct mentor password to access this section.")
# #   =========================== STUDENT AND CR PORTAL ==================================            
    
#     elif page == "👨‍🎓 Student":
#                 import pandas as pd
#                 import hashlib, uuid, os
#                 from streamlit_cookies_controller import CookieController
#                 import streamlit as st
#                 from datetime import datetime 
#                 import sqlite3
#                 from streamlit.runtime.scriptrunner import get_script_run_ctx
#                 #================= Persistent Device ID using Cookies =================
#                 controller = CookieController()

#                 if not controller.getAll():
#                     st.warning("Waiting for cookies to initialize. Please reload the page once.")
#                     st.stop()

#                 cookie_id = controller.get("device_id")
#                 if cookie_id:
#                     st.title("👨‍🎓" + "**Student Portal**")  
#                     device_id = cookie_id
#                 else:
#                     new_id = hashlib.sha256(str(uuid.uuid4()).encode()).hexdigest()
#                     controller.set("device_id", new_id, max_age=3600 * 24 * 365)
#                     st.warning("Cookie set, please reload the page for proper persistence.")
#                     st.stop()

#                 st.session_state["device_id"] = device_id

#                 #================= MARKED CSV loading and saving =================

#                 if not os.path.exists(MARKED_FILE):
#                     pd.DataFrame(columns=["Roll_no", "device_id"]).to_csv(MARKED_FILE, index=False)
#                 marked_df = pd.read_csv(MARKED_FILE)

#                 #================= Registration / Login UI =================
#                 # st.header("Register / Login")

#                 registered_entry = marked_df.loc[marked_df["device_id"] == device_id]

#                 if not registered_entry.empty:
#                     saved_roll = registered_entry.iloc[0]["Roll_no"]
                    
#                     st.session_state['user'] = saved_roll
#                     st.success(f"🪪 Permanently enrolled under Roll No. {saved_roll}; this device 🔗 is indelibly bound to your identity. 📱")
#                     st.text_input("Roll Number", value=saved_roll, disabled=True)
#                     # st.info("You cannot change Roll Number on this device.")
#                     st.write(f"Device ID: {device_id}")
#                 else:
#                     name = st.text_input("Enter your Name:")
#                     roll_no = st.selectbox("Enter your Roll Number:", CLASS_ROLL_NUMBERS)
#                     if st.button("Register"):
#                         if not name or not roll_no:
#                             st.error("Please fill in all fields.")
#                         else:
                            
#                             if roll_no in marked_df["Roll_no"].values:
#                                 st.error("This Roll Number is already bound to another device!")
#                             elif roll_no not in CLASS_ROLL_NUMBERS:
#                                 st.error('Invalid **ROLL NUMBER**')
#                             else:
#                                 new_row = pd.DataFrame([{"Roll_no": roll_no, "device_id": device_id}])
#                                 marked_df = pd.concat([marked_df, new_row], ignore_index=True)
#                                 marked_df.to_csv(MARKED_FILE, index=False)
#                                 st.session_state['user'] = roll_no
#                                 st.success(f"Registered successfully as {roll_no}")
#                                 st.rerun()

#                 #================= Other Tabs and Attendance Logic =================
#                 # For each tab, I should use the value of device_id and the permanent roll_no lookup as your identity key
#                 # Example stub:

#                 def get_session_id():
#                     ctx = get_script_run_ctx()
#                     if ctx and ctx.session_id:
#                         return hashlib.sha256(ctx.session_id.encode()).hexdigest()
#                     else:
#                         return hashlib.sha256(str(datetime.now()).encode()).hexdigest()

#                 if not os.path.exists(ATTENDANCE_FILE):
#                     attendance_df = pd.DataFrame(columns=['SessionID', 'Name', 'Date'])
#                     attendance_df.to_csv(ATTENDANCE_FILE, index=False) 
#                 attendance_df = pd.read_csv(ATTENDANCE_FILE)
#                 if 'user' not in st.session_state:
#                     try:
#                         st.session_state['user'] = saved_roll
#                     except NameError:
#                         st.session_state['user'] = None
#                 if not 'session_id' in st.session_state:
#                     st.session_state['session_id'] = get_session_id()
#                 passwords = {rn: 'In' + rn + '@123' for rn in CLASS_ROLL_NUMBERS} 
#                 def get_db_connection():
#                     conn = sqlite3.connect(DB_PATH)
#                     conn.execute("""
#                         CREATE TABLE IF NOT EXISTS attendance (
#                             roll_number TEXT PRIMARY KEY,
#                             device_id TEXT,
#                             mark_date TEXT,
#                             mark_time TEXT
#                         )
#                     """)
#                     conn.execute("""
#                         CREATE TABLE IF NOT EXISTS user_bindings (
#                             roll_number TEXT PRIMARY KEY,
#                             device_id TEXT,
#                             name TEXT
#                         )
#                     """)
#                     return conn
#                 def is_bound_to_another_device(roll_number):
#                     conn = get_db_connection()
#                     cur = conn.cursor()
#                     cur.execute("SELECT device_id FROM user_bindings WHERE roll_number=?", (roll_number,))
#                     row = cur.fetchone()
#                     conn.close()
#                     if row:
#                         return row[0] != device_id
#                     return False 
                
#                 def checking(rno):
#                     conn = get_db_connection()
#                     cur = conn.cursor()
#                     cur.execute("SELECT device_id FROM attendance WHERE roll_number=?", (rno,))
#                     row = cur.fetchone()
#                     if row:
#                         bound_device_id = row 
#                         if bound_device_id != device_id:
#                             return False 
#                         else:
#                             return True 
#                 tab1, tab2, tab3, tab4, tab5 = st.tabs(['🎯 Student/CR', '💬 Chat', '📝 Ask Permission', '🏆 Leaderboard', '⏮️ Prev Records'])
# #   ======================= STUDENT SECTION =============================                
#                 with tab1:
#                     st.header('📑 Mark your Attendance')
#                     # st.header('Enter the following details:')
#                     try:
#                         roll_no_tab2 = saved_roll
#                     except:
#                         roll_no_tab2 = None
#                     if roll_no_tab2 and roll_no_tab2 in CLASS_ROLL_NUMBERS:
#                         if is_bound_to_another_device(roll_no_tab2) and checking(roll_no_tab2):
#                             st.error(f"ERROR: Roll number {roll_no_tab2} is enrolled with another device. Access denied.")
#                         elif st.session_state['user'] is not None and st.session_state['user'] != roll_no_tab2:
#                             st.error("PROVIDE **VALID DETAILS** FIRST!")
#                         else:
#                             role = st.radio('Select Your Role:', ['Student', 'Class Representative'])

#                             if role == 'Student':
#                                 try:
#                                     from streamlit_geolocation import streamlit_geolocation
#                                     location = streamlit_geolocation()
#                                     st.write(f"📍You are at {location['latitude']} N and at {location['longitude']} E")
#                                 except ImportError:
#                                     location = {}
#                                     st.warning('streamlit_geolocation package not found. Location fetch will not work!')
#                                 except Exception as e:
#                                     location = {}
#                                     st.error(f"Error fetching location: {str(e)}. Check browser permissions.")

#                                 selected = st.selectbox('Who are You?', [roll_no_tab2])
#                                 password = st.text_input("Enter Secret Password:", type='password', placeholder='Type here...')
#                                 if st.button('Mark Present?'):
#                                     today = datetime.today().strftime('%Y-%m-%d')
#                                     input_time = datetime.now().strftime("%H:%M:%S")
#                                     if passwords[selected] == password:
#                                         if location.get("latitude") and location.get("longitude"):
#                                             lat = location['latitude']
#                                             long = location['longitude']
#                                             if (lat >= 18.018 and lat <= 18.12) and (long >= 83.39 and long <= 83.41):
#                                                     st.session_state['user'] = selected
#                                                     conn = get_db_connection()
#                                                     cur = conn.cursor()
#                                                     cur.execute("SELECT device_id, mark_date, mark_time FROM attendance WHERE roll_number=?", (selected,))
#                                                     row = cur.fetchone()
#                                                     if row:
#                                                         bound_device_id, mark_date, mark_time = row
#                                                         if bound_device_id != device_id:
#                                                             st.error(f"ERROR: Roll number {selected} already marked as present by another device on {mark_date} at {mark_time}. Multiple marks are NOT allowed.")
#                                                         else:
#                                                             st.warning(f"{selected} is already marked present (by this device).")
#                                                     else:
#                                                         cur.execute("INSERT INTO attendance (roll_number, device_id, mark_date, mark_time) VALUES (?, ?, ?, ?)", (selected, device_id, today, input_time))
#                                                         conn.commit()
#                                                         already_marked = attendance_df[(attendance_df['Name'] == selected) & (attendance_df['Date'] == today)]
#                                                         if already_marked.empty:
#                                                             data = [[st.session_state['session_id'], selected, today]]
#                                                             new_df = pd.DataFrame(data, columns=['SessionID', 'Name', 'Date'])
#                                                             st.metric(label='Presence Hike', value = len(attendance_df[pd.to_datetime(attendance_df['Date']) == datetime.today().month]), delta = "+1")
#                                                             attendance_df = pd.concat([attendance_df, new_df], ignore_index=True)
#                                                             attendance_df.to_csv(ATTENDANCE_FILE, index=False)
                                                            
#                                                         st.success(f"You ({selected}) are now marked as present for {today}!")
#                                                         st.balloons()
#                                                         import time
#                                                         time.sleep(2)
                                                        
#                                             else:
#                                                 import time
#                                                 time.sleep(2)
#                                                 st.error("⚠️ Your Location is not matching i.e you aren't there in college!!")
#                                         else:
#                                             st.error(f"Didn't fetch location, open settings and grant permission of accessing Loaction for this device!!")
#                                             import time
#                                             time.sleep(2)
#                                     else:
#                                             import time
#                                             time.sleep(2)
#                                             st.error('WRONG PASSWORD!!')
#                                 try:
#                                     import datetime
#                                     month = datetime.datetime.today().month 
#                                     user = selected
#                                     di = {
#                                         '1': "JAN",
#                                         "2": "FEB",
#                                         "3": "MAR",
#                                         "4": "APR",
#                                         "5": "MAY",
#                                         "6": "JUNE",
#                                         "7": "JULY",
#                                         "8": "AUG",
#                                         "9": "SEP",
#                                         "10": "OCT",
#                                         "11": "NOV",
#                                         "12": "DEC"
#                                     }
#                                     df = pd.read_csv(ATTENDANCE_FILE)
#                                     months = ["JAN", "FEB", "MAR", "APR", "MAY", "JUNE", "JULY", "AUG", "SEP", "OCT", "NOV", "DEC"]
#                                     a,b,c=st.columns([2,2,1])
#                                     with c:
#                                         with st.expander("Report", icon="📋"):
#                                             selected_month=st.radio("Select month:", help='Select month you want to download!',options=months, index=months.index(di[str(month)]))
#                                             present = df.loc[df['Name'] == user, 'Date'] 
#                                             from datetime import datetime 
#                                             csv_attendance_list=pd.DataFrame(columns=['Date', 'Attended/Not'])

#                                             year_list = []
#                                             for i in present:
#                                                 i = datetime.strptime(i,"%Y-%m-%d").date() 
#                                                 year_list.append(i) 

#                                             month_list = []
#                                             if selected_month == 'OCT':
#                                                 for i in year_list:
#                                                     if i.month == 10:
#                                                         month_list.append(i) 
#                                             elif selected_month == 'NOV':
#                                                 for i in year_list:
#                                                     if i.month == 11:
#                                                         month_list.append(i) 
#                                             elif selected_month == 'DEC':
#                                                 for i in year_list:
#                                                     if i.month == 12:
#                                                         month_list.append(i) 
#                                             elif selected_month == 'JAN':
#                                                 for i in year_list:
#                                                     if i.month == 1:
#                                                         month_list.append(i) 
#                                             elif selected_month == 'FEB':
#                                                 for i in year_list:
#                                                     if i.month == 2:
#                                                         month_list.append(i) 
#                                             elif selected_month == 'MAR':
#                                                 for i in year_list:
#                                                     if i.month == 3:
#                                                         month_list.append(i) 
#                                             elif selected_month == 'APR':
#                                                 for i in year_list:
#                                                     if i.month == 4:
#                                                         month_list.append(i)
#                                             elif selected_month == 'MAY':
#                                                 for i in year_list:
#                                                     if i.month == 5:
#                                                         month_list.append(i)  
#                                             elif selected_month == 'JUNE':
#                                                 for i in year_list:
#                                                     if i.month == 6:
#                                                         month_list.append(i) 
#                                             elif selected_month == 'JULY':
#                                                 for i in year_list:
#                                                     if i.month == 7:
#                                                         month_list.append(i) 
#                                             elif selected_month == 'AUG':
#                                                 for i in year_list:
#                                                     if i.month == 8:
#                                                         month_list.append(i) 
#                                             elif selected_month == 'SEP':
#                                                 for i in year_list:
#                                                     if i.month == 9:
#                                                         month_list.append(i) 

#                                             for i in month_list:
#                                                 csv_attendance_list = pd.concat([csv_attendance_list,pd.DataFrame([{'Date':i, 'Attended/Not':'Yes'}])], ignore_index=True)

#                                             date_list = [] 
#                                             for i in (csv_attendance_list['Date'].to_list()):
#                                                 date_list.append(i)
#                                             max_no_of_days = {
#                                                 'JAN': 31,
#                                                 'FEB': 28,  
#                                                 'MAR': 31,
#                                                 'APR': 30,
#                                                 'MAY': 31,
#                                                 'JUNE': 30,
#                                                 'JULY': 31,
#                                                 'AUG': 31,
#                                                 'SEP': 30,
#                                                 'OCT': 31,
#                                                 'NOV': 30,
#                                                 'DEC': 31
#                                             }
#                                             month_num = next((int(k) for k, v in di.items() if v == selected_month), None)
#                                             month_list = [i for i in year_list if i.month == month_num]

#                                             for i in range(1,max_no_of_days[selected_month]+1):
#                                                 date_str = f"2025-{month_num:02d}-{i:02d}"
#                                                 date_obj=datetime.strptime(date_str,"%Y-%m-%d").date()
#                                                 if date_obj not in date_list:        
#                                                     csv_attendance_list=pd.concat([csv_attendance_list, pd.DataFrame([{'Date':date_obj,'Attended/Not': 'No'}])], ignore_index=True)

#                                             csv_attendance_list=csv_attendance_list.sort_values('Date')
#                                             csv_attendance_list=csv_attendance_list.to_csv(index=False).encode('utf-8') 
#                                             st.download_button(label=f"{selected_month} Report", mime='text/csv',key="download_user", data=csv_attendance_list, file_name=f'{user}_{selected_month}_attendance.csv')
#                                     this_month_list = []
#                                     this_month_list = [i for i in year_list if i.month == month]
#                                     attendance_per = (round((len(this_month_list)/max_no_of_days[di[str(month)]])*100,4))
#                                     if attendance_per >= 70:
#                                         st.success(f"The Attendance percentnage for this {month}th month {di[str(month)]} is: {attendance_per}%")
#                                     elif attendance_per>= 60 and attendance_per <= 70:
#                                         st.warning(f"The Attendance percentnage for this {month}th month {di[str(month)]} is: {attendance_per}%")
#                                     else:
#                                         st.error(f"The Attendance percentnage for this {month}th month {di[str(month)]} is: {attendance_per}%")
#                                 except pd.errors.EmptyDataError:
#                                         df = pd.DataFrame(columns=['SessionID','Name','Date'])
#                                         df.to_csv(ATTENDANCE_FILE)
#                                         st.info("You've not marked attendance yet!")
#                                 except FileNotFoundError:
#                                         df = pd.DataFrame(columns=['SessionID','Name','Date'])
#                                         df.to_csv(ATTENDANCE_FILE)
#                                         st.info("Attendance file not found yet. Start marking attendance!")

# #   =============================== CLASS REPRESENTATIVE TAB =============================

#                             elif role == 'Class Representative':
#                                 rep_pass = st.text_input("Enter Rep Password:", type='password').strip()
#                                 selected_date = st.date_input("Select Date to View Attendance:", value=datetime.today())
#                                 selected_date_str = selected_date.strftime('%Y-%m-%d')
#                                 if rep_pass == "":
#                                     st.warning("Enter correct password to access details!")

#                                 elif rep_pass == rep_password:
#                                     attendance_df = pd.read_csv(ATTENDANCE_FILE)
#                                     daily_attendance = attendance_df[attendance_df['Date'] == selected_date_str]
#                                     present_list = daily_attendance['Name'].tolist()
#                                     absent_list = [name for name in CLASS_ROLL_NUMBERS if name not in present_list]
#                                     absent_df=pd.DataFrame({'Name':absent_list})
                                    
#                                     st.subheader(f'Attendance for {selected_date_str}:')
#                                     col1, col2, col3 = st.columns([1, 6, 1])

#                                     permissions_df = pd.read_csv(PERMISSIONS_FILE)
#                                     permissions_df=permissions_df.drop(columns=['Reason','No_of_days'])
#                                     import numpy as np
#                                     absent_df['result'] = np.where(
#                                         absent_df['Name'].isin(permissions_df['Roll_no']),
#                                         'A',
#                                         'NA'
#                                     )

#                                     def apply_highlight(row):
#                                         color = 'background-color:white;color:black;' if row['result'] == 'A' else 'background-color:black;color:white;'
#                                         return [color] * len(row) 


#                                     coloured_df=absent_df.loc[:].style.apply(apply_highlight, axis=1)

#                                     with col2:
#                                         cola, colb = st.columns(2)
#                                         with cola:
#                                             st.write('**Presenties:**')
#                                             if present_list:
#                                                 st.write(daily_attendance['Name'])
#                                             else:
#                                                 st.write("No one present.")
#                                         with colb:
#                                             st.write('**Absenties:**')
#                                             if absent_list:
#                                                 st.dataframe(coloured_df, use_container_width=True)
#                                             else:
#                                                 st.write("Everyone present!")
#                                         with col2:
#                                             col = st.columns(1)
#                                             attendance_data=pd.concat([pd.Series([selected_date_str] * max(len(present_list), len(absent_list))), daily_attendance['Name'], absent_df], axis=1, ignore_index=True)
#                                             cr_csv_data=attendance_data.to_csv(index=False).encode('utf-8')
#                                             st.download_button(label='Download Report', data=cr_csv_data, mime='text/csv', key='CR_Download', file_name=ATTENDANCE_FILE)
#                                 else:
#                                     st.error('Wrong Rep Password!')

#                                 if st.button('Reset Attendance for Selected Date') and rep_pass == rep_password:
#                                     attendance_df = attendance_df[attendance_df['Date'] != selected_date_str]
#                                     attendance_df.to_csv(ATTENDANCE_FILE, index=False)
#                                     st.info(f"Attendance reset for {selected_date_str}!")
#                     else:
#                         st.error("Please enter a valid roll number.")

#                 st.markdown("""
#                 <link rel="stylesheet"
#                     href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">

#                 <style>
#                 .chat-container {
#                     display: flex;
#                     flex-direction: column;
#                     gap: 10px;
#                     margin-top: 20px;
#                     max-width: 100%;
#                     width: 100%;
#                     margin-bottom:20px;
#                 }

#                 .chat-bubble {
#                     padding: 10px 15px;
#                     border-radius: 15px;
#                     max-width: 70%;
#                     word-wrap: break-word;
#                     font-size: 16px;
#                 }

#                 .left-bubble {
#                     align-self: flex-start;
#                     background-color: #dcf8c6; /* light green */
#                     color: black;
#                     border-top-left-radius: 0;
#                     text-align: left;
#                 }

#                 .right-bubble {
#                     align-self: flex-end;
#                     background-color: #add8e6; /* light blue */
#                     color: black;
#                     border-top-right-radius: 0;
#                     text-align: right;
#                 }
#                 </style>
#                 """, unsafe_allow_html=True)
# #   =========================== CHAT TAB ===============================

#                 with tab2:
#                     st.subheader("🗨️ Group chat")
#                     try:
#                         roll_no_tab3 = saved_roll 
#                     except:
#                         roll_no_tab3 = None
#                     if roll_no_tab3 and roll_no_tab3 in CLASS_ROLL_NUMBERS:
#                         if is_bound_to_another_device(roll_no_tab3) and checking(roll_no_tab3):
#                             st.error(f"ERROR: Roll number {roll_no_tab3} is enrolled with another device. Access denied.")
#                         elif st.session_state['user'] is not None and roll_no_tab3 != st.session_state['user']:
#                             st.error("Provide the Valid Roll NO first!")
#                         else:
#                             chat1, chat2, chat3=st.tabs(['Messages', 'Polls', 'Files'])
#                             with chat1:
#                                 if not os.path.exists(MESSAGE_FILE):
#                                     st.info("💭 No messages yet. Start the conversation!")
#                                     message_df = pd.DataFrame(columns=['Roll_no', 'Message'])
#                                     message_df.to_csv(MESSAGE_FILE, index=False)
#                                 else:
#                                     message_df = pd.read_csv(MESSAGE_FILE)
                                
#                                 issue = st.chat_input("Enter your issue: ")
#                                 if issue:
#                                     sanitized_issue = html.escape(issue)
#                                     new_msg = pd.DataFrame({"Roll_no": [roll_no_tab3], "Message": [sanitized_issue]})
#                                     message_df = pd.concat([message_df, new_msg], ignore_index=True)
#                                     message_df.to_csv(MESSAGE_FILE, index=False)
                                
#                                 message_df = message_df.sort_index()
                                
#                                 chat_html = "<div class='chat-container'>"
#                                 for idx, row in message_df.iterrows():
#                                     sanitized_roll = html.escape(str(row['Roll_no']))
#                                     sanitized_msg = html.escape(str(row['Message']))
#                                     if row['Roll_no'] == roll_no_tab3:
#                                         chat_html += f"<div class='chat-bubble left-bubble'><b>{sanitized_roll}</b>: {sanitized_msg}</div>"
#                                     else:
#                                         chat_html += f"<div class='chat-bubble right-bubble'><b>{sanitized_roll}</b>: {sanitized_msg}</div>"
                                        
#                                 chat_html += "</div>"
#                                 st.markdown(chat_html, unsafe_allow_html=True)
#                                 if st.button("🗑️ Clear chat"):
#                                     message_df = pd.DataFrame(columns=message_df.columns)
#                                     message_df.to_csv(MESSAGE_FILE, index=False)
#                                 # st.rerun()
#                             with chat2:
#                                 import ast                                 
#                                 roll = st.text_input("Enter your Rollno: ", value = roll_no_tab3, disabled=True) 
#                                 with st.expander("🔊 Create a New Poll"):
#                                     question = st.text_input("Poll question")
#                                     option_cols = st.columns(4)
#                                     options = []
                                    
#                                     for i in range(4):
#                                         opt = option_cols[i].text_input(f"Option {i+1}", key=f"option_{i}")
#                                         if opt:
#                                             options.append(opt)
                                    

#                                     if st.button("➕ Create Poll"):
#                                         if question and len(options) >= 2:
#                                             df = pd.DataFrame({'question': question,'options': options, 'votes': [0,0,0,0], 'voted': [[] for _ in options], 'created_by': [roll_no_tab3 for _ in options]})
#                                             df.to_csv(POLLS)
#                                             st.success("Poll created successfully!")
#                                             st.rerun()
#                                         else:
#                                             st.warning("Please enter a question and at least two options.") 

#                                 st.write("---")

#                                 try: 
#                                     df = pd.read_csv(POLLS) 
#                                     options = df['options']
#                                     st.header(df['question'][0]) 
#                                     st.write(f"Created by: {df['created_by'][0]}") 
#                                     choosed = st.radio("Choose any one: ", options=options)
#                                     row_index=0
#                                     if st.button("Submit"):
#                                         if roll in df['voted'][0]:
#                                             st.warning("You've aldready entered!!") 
#                                         elif roll != "":
#                                             df.loc[df['options'] == choosed, 'votes'] += 1

#                                             df['voted'] = df['voted'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)


#                                             df.at[row_index, 'voted'].append(roll)

#                                             df.to_csv(POLLS, index=False)
#                                             # st.write(df) 

#                                         elif roll == "":
#                                             st.warning("Enter Roll NO")
#                                     # st.write(df['voted'][0]) 
#                                 except:
#                                     st.info("No Poll created yet!!")

#                                 st.write("---")

#                                 try:
#                                     df = pd.read_csv(POLLS) 
#                                     total = 0
#                                     for i in df['votes']:
#                                         total += i 
#                                     st.header("Results Section: ")
#                                     for i,j in enumerate(df['votes']):
#                                         print(f"Option {i}: {j/total * 100}") 
#                                         st.progress(value = j/total, text = f"Option {i+1}: {j/total * 100}%") 
#                                     st.rerun()
#                                 except:
#                                     pass 

#                                 try:
#                                     if st.button("Delete Poll", type='primary'):
#                                         if roll == df['created_by'][0]:
#                                             df = pd.DataFrame(columns=['question','options','votes','voted', 'created_by'])
#                                             df.to_csv(POLLS, index=False) 
#                                             # st.rerun()
#                                         else:
#                                             st.error("You cannot do it as your roll no not matching!") 
#                                 except:
#                                     pass

#                             with chat3:
#                                 st.file_uploader('Drop files here: ',type=["jpg", "jpeg", "png", "csv", "png"],accept_multiple_files=True)

                           
#                     else:
#                         st.error("Please enter a valid roll number.")

# #   ======================= ASK PERMISSION TAB =========================

#                 with tab3:
#                     no_of_days = 0
#                     try:
#                         Roll_no = saved_roll
#                     except:
#                         Roll_no = None
#                     if Roll_no and Roll_no in CLASS_ROLL_NUMBERS:

#                         if (is_bound_to_another_device(Roll_no) and checking(Roll_no)):
#                                 st.error(f"ERROR: Roll number {Roll_no} is enrolled with another device. Access denied.")
#                         else:
#                                 if st.session_state['user'] is not None and roll_no_tab3 != st.session_state['user']:
#                                     st.error("Provide the Valid Roll NO first!")
#                                 else:
#                                     with st.form("permission_form", clear_on_submit=True):
#                                         st.subheader("New Leave Application Form:")
#                                         no_of_days = st.slider("Number of days: ", min_value=1, max_value=10)
#                                         if not os.path.exists(PERMISSIONS_FILE):
#                                                 per_df = pd.DataFrame(columns=['Roll_no', 'Reason', 'Granted', "No_of_days"])
#                                                 per_df.to_csv(PERMISSIONS_FILE, index=False)
#                                         else:
#                                                 per_df = pd.read_csv(PERMISSIONS_FILE)
                                            
#                                         issue = st.text_area("Reason for leave",placeholder="Explain your reason briefly...", key="permission_input")
#                                         if st.form_submit_button("Send Request"):
#                                                 sanitized_issue = html.escape(str(issue))
#                                                 sanitized_days = html.escape(str(no_of_days))
#                                                 new_msg = pd.DataFrame({"Roll_no": [roll_no_tab3], "Reason": [sanitized_issue], "No_of_days": [sanitized_days], "Granted": ['Pending']})
#                                                 per_df = pd.concat([per_df, new_msg], ignore_index=True)
#                                                 per_df.to_csv(PERMISSIONS_FILE, index=False)
#                                                 st.rerun()
#                                         per_df = per_df.sort_index()
                                        
#                                     st.write("---")
#                                     st.subheader("📑 Requested Permissions report")
#                                     st.session_state[f"{Roll_no}"] = False
#                                     if Roll_no in per_df['Roll_no'].values:
#                                         if (per_df.loc[per_df['Roll_no'] == Roll_no, 'Granted'] == 'Pending').any():
#                                             if not st.session_state[f"{Roll_no}"]:
#                                                 st.toast("😔 Your request is still in pending!", icon="⚠️", duration='infinite')
#                                                 st.session_state[f"{Roll_no}"] = True 
#                                             st.warning(f"😥😥Your case is still in **PENDING**")
#                                         elif per_df.loc[per_df['Roll_no'] == Roll_no, 'Granted'].any():
#                                             if not st.session_state[f"{Roll_no}"]:
#                                                 st.toast("🎉 Your leave has been approved!", icon="✅", duration='infinite')
#                                                 st.markdown(
#                                                     "<audio autoplay><source src='https://www.soundjay.com/buttons/button-3.mp3' type='audio/mpeg'></audio>",
#                                                     unsafe_allow_html=True
#                                                     )
#                                                 st.session_state[f"{Roll_no}"] = True 
#                                             st.balloons()
#                                             st.success(f'✅ Your permissions for {per_df.loc[per_df['Roll_no'] == Roll_no, 'No_of_days'][0]} days has been granted!!')
                                            
#                                         else:
#                                             if not st.session_state[f"{Roll_no}"]:
#                                                 st.toast("Your leave might be rejected!", icon="❌", duration='infinite')
#                                                 st.markdown(
#                                                     "<audio autoplay><source src='https://www.soundjay.com/buttons/button-3.mp3' type='audio/mpeg'></audio>",
#                                                     unsafe_allow_html=True
#                                                 )
#                                                 st.session_state[f"{Roll_no}"] = True 
#                                             st.error('😑😑The Mentor has **MIGHT BE REJECTED** your leave!!')
#                                     else:
#                                         st.write("You didn't raise any permission request!!")
#                     else:
#                         st.error("Please enter a valid roll number.")
#                 st.caption(f"Device ID: {device_id}")            

# #   ======================= LEADER BOARD TAB ============================

#                 with tab4:
#                     st.subheader("🏆 Attendance Leaderboard")
#                     tab4_df=pd.read_csv(ATTENDANCE_FILE)
#                     month=datetime.today().month
#                     date_series=tab4_df['Date']
#                     student_list = []
#                     for i in date_series:
#                         if datetime.strptime(i, "%Y-%m-%d").date().month == month:
#                             student_list.append(tab4_df.loc[tab4_df['Date'] == i, 'Name'].values) 
#                     df=pd.DataFrame(student_list)
#                     df=df.drop_duplicates()
#                     final_list = []
#                     for i in df.columns:
#                         for j in df[i]:
#                             final_list.append(j)
#                     leader_df=pd.DataFrame(columns=['Roll_NO', 'Present']) 
#                     for i in final_list:
#                         single_df=pd.DataFrame({'Roll_NO': [i], 'Present': [final_list.count(i)]})
#                         leader_df=pd.concat([leader_df, single_df], ignore_index=True)
#                     leader_df=leader_df.dropna()
#                     leader_df=leader_df.drop_duplicates()
#                     st.write(leader_df)
#                     leader_df=leader_df.to_csv(index=False).encode('utf-8')
#                     _,butt,_= st.columns([1,1,1])
#                     with butt:
#                         st.download_button(label='📤 Download Leaderboard', file_name=f"{month}Leaderboard.csv", data=leader_df,mime='text/csv', key=f"{month}Leaderboard")
    

#                 with tab5:
#                     st.title("Previous Attendance Records")
#                     user = st.session_state['user']
#                     from io import StringIO
#                     july = """
#                     0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22
#                     X1,SANAPATHIYAMUNA,P,P,P,AB,P,P,P,P,P,P,AB,P,AB,P,P,P,P,AB,P,AB,P
#                     X2,SANKURABOTHUMANITEJ,P,P,P,P,P,P,AB,P,P,AB,P,P,P,P,P,P,P,P,P,P,P
#                     X3,SARIKAAASWITHA,P,P,P,P,P,AB,P,P,P,P,P,P,P,P,P,P,AB,P,P,P,P
#                     X4,SARIKAJASMINE,P,P,P,P,AB,AB,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
#                     X5,SATTALARAMAKRISHNA,AB,AB,P,P,P,P,AB,P,P,P,P,P,P,P,P,P,P,P,P,P,AB
#                     X6,SEEMAKURTHISAHITHI,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
#                     X7,SEERAPUARYANREDDY,AB,AB,AB,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
#                     X8,SEERAPUMEGHANA,AB,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,AB,P,P
#                     X9,SEERAPUSHIVADHEERAJ,P,P,P,P,P,AB,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
#                     Y0,SHAIKSHAHID,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
#                     Y1,SHAIKSHAZID,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
#                     Y2,SHEIKARIF,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
#                     Y3,SHEIKNOORJAHAN,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,AB,P,P
#                     Y4,SHETTITEJASWARI,AB,AB,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,AB,P,P
#                     Y5,SIDAGAMRAJESH,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
#                     Y6,SIDDAANITHA,P,P,P,P,P,P,AB,P,P,P,P,P,P,P,P,P,P,P,P,P,P
#                     Y7,SIGALAPELLIPAVANKUMAR,P,P,P,P,P,P,P,P,AB,AB,AB,AB,AB,P,P,AB,P,P,P,P,P
#                     Y8,SIRIPURAPURAGHU,P,AB,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
#                     Y9,SIRIPURAPUTRINADHA,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
#                     Z0,SIVVITIKIRANMAYEE,P,P,P,P,P,AB,P,P,P,P,AB,P,P,P,P,P,P,P,P,P,P
#                     Z2,SURUAKSHAYA,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
#                     Z3,TAKARLARONITHREDDY,P,P,P,P,P,P,P,P,P,P,AB,AB,AB,P,P,P,P,AB,P,P,P
#                     Z4,TALACHUTLAHASINI,P,P,P,P,P,P,P,P,P,P,P,AB,P,P,P,P,P,P,AB,P,P
#                     Z5,TALADAKAVYAJAHNAVI,P,P,P,P,P,P,P,P,AB,P,AB,P,P,P,P,P,P,P,P,P,P
#                     Z6,TALADASREEVENKATESH,P,P,P,P,P,P,P,P,P,P,P,AB,P,P,P,P,P,P,P,P,P
#                     Z7,TALEBHANUTEJA,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
#                     Z8,TEDLAPUSAIREESHNIKA,AB,AB,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
#                     Z9,TEDLAPUSHANMUKHESWAR,P,P,P,P,P,P,P,P,P,P,AB,AB,P,P,P,P,P,P,P,P,P
#                     AA,TEEDAJENYA,AB,AB,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
#                     AB,TEEDASRILAKSHMI,P,P,P,P,AB,P,P,P,P,AB,P,P,P,P,P,P,P,P,P,P,P
#                     AC,TELUKALAKEERTHANA,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
#                     AD,THADDIVINAY,AB,AB,P,AB,P,P,P,P,P,P,AB,P,P,P,P,P,P,AB,P,P,P
#                     AE,THAMMINATEJASWI,P,P,P,P,P,P,P,P,P,P,AB,P,P,P,P,P,P,P,P,P,P
#                     AF,THOTAGAYATHRISRUJANA,P,P,P,P,AB,P,AB,P,P,P,P,P,P,P,P,P,P,P,P,P,P
#                     AG,THUMMAGANTIGANESH,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
#                     AH,TIPPANASAINIKHILESH,AB,AB,AB,P,P,AB,P,P,P,P,AB,AB,AB,P,P,AB,AB,AB,AB,AB,AB
#                     AI,TRIPURAGIRIAKHILA,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
#                     AJ,TULUGUGAYATHRI,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
#                     AK,UPPALAPATIYOGENDRAVARMA,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
#                     AL,VADAPALLILIKHITHMANOHAR,P,P,P,P,P,P,P,P,P,P,AB,P,P,P,P,P,P,P,P,AB,P
#                     AM,VADDADINAGESHKUMAR,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,AB,P,P,P
#                     AN,VADUGURUSRINIDHI,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
#                     AO,VAKAMULLULAKSHMINARAYANA,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,AB,AB
#                     AP,VALLURIRANADHEERNAIDU,P,P,P,P,P,P,P,P,AB,P,P,P,P,P,P,P,P,P,P,P,P
#                     AQ,VANKAYASWANTHESWAR,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
#                     AR,VARREJAGADEESH,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
#                     AS,VARRILEELAKRISHNA,P,P,P,P,P,AB,P,P,P,P,AB,P,P,P,P,P,P,P,P,P,P
#                     AT,VARRINEELIMA,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
#                     AU,VEMPADAPUMOHINI,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
#                     AV,VEMPADAPUUMAJYOTHSNA,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
#                     AW,YADLASAIDEEKSHITHA,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
#                     AX,YAJJALAKISHOR,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
#                     AY,YALAANUSH,P,P,P,P,P,AB,P,P,P,P,AB,P,P,P,P,P,P,P,P,AB,AB
#                     AZ,YALLASAMUELSATHVIK,P,P,P,P,P,P,P,P,P,AB,P,P,P,P,P,P,P,P,P,P,P
#                     BA,YANDRAPUVAMSI,AB,P,P,AB,AB,P,P,P,AB,P,P,P,P,P,P,P,P,P,P,P,P
#                     BB,YARRAMADHUSUDHANARAO,P,P,P,P,P,P,P,AB,P,AB,P,P,P,P,P,P,P,P,P,P,AB
#                     BD,YARRARAPUPUNYAVATHI,P,P,P,P,P,AB,AB,P,P,P,P,P,P,P,P,P,AB,AB,AB,P,P
#                     BE,YEGIREDDYTEJA,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,AB
#                     BF,YELAMANCHILIRAKESH,P,P,P,P,P,P,P,P,P,P,AB,P,P,P,P,P,P,P,P,P,P
#                     BG,YELUSOORIVIJAY,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
#                     BH,YERRARUPESH,P,P,P,P,P,P,P,P,P,P,P,AB,AB,P,P,AB,AB,AB,P,AB,AB
#                     BI,YERRASHYAMCHANDU,P,P,AB,P,P,P,P,P,P,P,AB,P,P,P,P,P,P,P,P,P,P
#                     BJ,YERRASIRICHANDANA,P,P,P,P,AB,AB,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
#                     BK,YETURISURESH,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,AB,P
#                     """

#                     august = """
#                     0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22
#                     X1,SANAPATHIYAMUNA,P,P,P,AB,P,P,P,P,P,P,AB,P,AB,P,P,P,P,AB,P,AB,P
#                     X2,SANKURABOTHUMANITEJ,P,P,P,P,P,P,AB,P,P,AB,P,P,P,P,P,P,P,P,P,P,P
#                     X3,SARIKAAASWITHA,P,P,P,P,P,AB,P,P,P,P,P,P,P,P,P,P,AB,P,P,P,P
#                     X4,SARIKAJASMINE,P,P,P,P,AB,AB,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
#                     X5,SATTALARAMAKRISHNA,AB,AB,P,P,P,P,AB,P,P,P,P,P,P,P,P,P,P,P,P,P,AB
#                     X6,SEEMAKURTHISAHITHI,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
#                     X7,SEERAPUARYANREDDY,AB,AB,AB,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
#                     X8,SEERAPUMEGHANA,AB,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,AB,P,P
#                     X9,SEERAPUSHIVADHEERAJ,P,P,P,P,P,AB,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
#                     Y0,SHAIKSHAHID,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
#                     Y1,SHAIKSHAZID,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
#                     Y2,SHEIKARIF,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
#                     Y3,SHEIKNOORJAHAN,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,AB,P,P
#                     Y4,SHETTITEJASWARI,AB,AB,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,AB,P,P
#                     Y5,SIDAGAMRAJESH,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
#                     Y6,SIDDAANITHA,P,P,P,P,P,P,AB,P,P,P,P,P,P,P,P,P,P,P,P,P,P
#                     Y7,SIGALAPELLIPAVANKUMAR,P,P,P,P,P,P,P,P,AB,AB,AB,AB,AB,P,P,AB,P,P,P,P,P
#                     Y8,SIRIPURAPURAGHU,P,AB,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
#                     Y9,SIRIPURAPUTRINADHA,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
#                     Z0,SIVVITIKIRANMAYEE,P,P,P,P,P,AB,P,P,P,P,AB,P,P,P,P,P,P,P,P,P,P
#                     Z2,SURUAKSHAYA,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
#                     Z3,TAKARLARONITHREDDY,P,P,P,P,P,P,P,P,P,P,AB,AB,AB,P,P,P,P,AB,P,P,P
#                     Z4,TALACHUTLAHASINI,P,P,P,P,P,P,P,P,P,P,P,AB,P,P,P,P,P,P,AB,P,P
#                     Z5,TALADAKAVYAJAHNAVI,P,P,P,P,P,P,P,P,AB,P,AB,P,P,P,P,P,P,P,P,P,P
#                     Z6,TALADASREEVENKATESH,P,P,P,P,P,P,P,P,P,P,P,AB,P,P,P,P,P,P,P,P,P
#                     Z7,TALEBHANUTEJA,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
#                     Z8,TEDLAPUSAIREESHNIKA,AB,AB,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
#                     Z9,TEDLAPUSHANMUKHESWAR,P,P,P,P,P,P,P,P,P,P,AB,AB,P,P,P,P,P,P,P,P,P
#                     AA,TEEDAJENYA,AB,AB,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
#                     AB,TEEDASRILAKSHMI,P,P,P,P,AB,P,P,P,P,AB,P,P,P,P,P,P,P,P,P,P,P
#                     AC,TELUKALAKEERTHANA,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
#                     AD,THADDIVINAY,AB,AB,P,AB,P,P,P,P,P,P,AB,P,P,P,P,P,P,AB,P,P,P
#                     AE,THAMMINATEJASWI,P,P,P,P,P,P,P,P,P,P,AB,P,P,P,P,P,P,P,P,P,P
#                     AF,THOTAGAYATHRISRUJANA,P,P,P,AB,P,AB,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
#                     AG,THUMMAGANTIGANESH,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
#                     AH,TIPPANASAINIKHILESH,AB,AB,AB,P,P,AB,P,P,P,P,AB,AB,AB,P,P,AB,AB,AB,AB,AB,AB
#                     AI,TRIPURAGIRIAKHILA,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
#                     AJ,TULUGUGAYATHRI,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
#                     AK,UPPALAPATIYOGENDRAVARMA,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
#                     AL,VADAPALLILIKHITHMANOHAR,P,P,P,P,P,P,P,P,P,P,AB,P,P,P,P,P,P,P,P,AB,P
#                     AM,VADDADINAGESHKUMAR,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,AB,P,P,P
#                     AN,VADUGURUSRINIDHI,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
#                     AO,VAKAMULLULAKSHMINARAYANA,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,AB,AB
#                     AP,VALLURIRANADHEERNAIDU,P,P,P,P,P,P,P,P,AB,P,P,P,P,P,P,P,P,P,P,P,P
#                     AQ,VANKAYASWANTHESWAR,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
#                     AR,VARREJAGADEESH,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
#                     AS,VARRILEELAKRISHNA,P,P,P,P,P,AB,P,P,P,P,AB,P,P,P,P,P,P,P,P,P,P
#                     AT,VARRINEELIMA,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
#                     AU,VEMPADAPUMOHINI,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
#                     AV,VEMPADAPUUMAJYOTHSNA,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
#                     AW,YADLASAIDEEKSHITHA,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
#                     AX,YAJJALAKISHOR,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
#                     AY,YALAANUSH,P,P,P,P,P,AB,P,P,P,P,AB,P,P,P,P,P,P,P,P,AB,AB
#                     AZ,YALLASAMUELSATHVIK,P,P,P,P,P,P,P,P,P,AB,P,P,P,P,P,P,P,P,P,P,P
#                     BA,YANDRAPUVAMSI,AB,P,P,AB,AB,P,P,P,AB,P,P,P,P,P,P,P,P,P,P,P,P
#                     BB,YARRAMADHUSUDHANARAO,P,P,P,P,P,P,P,AB,P,AB,P,P,P,P,P,P,P,P,P,P,AB
#                     BD,YARRARAPUPUNYAVATHI,P,P,P,P,P,AB,AB,P,P,P,P,P,P,P,P,P,AB,AB,AB,P,P
#                     BE,YEGIREDDYTEJA,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,AB
#                     BF,YELAMANCHILIRAKESH,P,P,P,P,P,P,P,P,P,P,AB,P,P,P,P,P,P,P,P,P,P
#                     BG,YELUSOORIVIJAY,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
#                     BH,YERRARUPESH,P,P,P,P,P,P,P,P,P,P,P,AB,AB,P,P,AB,AB,AB,P,AB,AB
#                     BI,YERRASHYAMCHANDU,P,P,AB,P,P,P,P,P,P,P,AB,P,P,P,P,P,P,P,P,P,P
#                     BJ,YERRASIRICHANDANA,P,P,P,P,AB,AB,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
#                     BK,YETURISURESH,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,AB,P
#                     """
#                     sept = """
#                     0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18
#                     X1,SANAPATHIYAMUNA,AB,P,AB,AB,AB,P,P,P,P,P,P,P,P,AB,P,P,P
#                     X2,SANKURABOTHUMANITEJ,P,P,P,P,P,P,P,P,P,P,P,AB,AB,P,P,AB,AB
#                     X3,SARIKAAASWITHA,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
#                     X4,SARIKAJASMINE,P,AB,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
#                     X5,SATTALARAMAKRISHNA,AB,P,P,P,P,P,P,P,P,P,P,AB,AB,P,P,P,P
#                     X6,SEEMAKURTHISAHITHI,P,P,P,P,AB,P,P,P,P,P,P,P,P,P,P,P,P
#                     X7,SEERAPUARYANREDDY,AB,AB,P,P,P,AB,P,P,P,P,P,P,P,P,P,P,P
#                     X8,SEERAPUMEGHANA,P,P,AB,P,P,P,P,AB,P,P,P,P,P,P,P,P,P
#                     X9,SEERAPUSHIVADHEERAJ,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
#                     Y0,SHAIKSHAHID,P,P,P,P,AB,P,P,P,P,P,P,P,P,P,P,AB,P
#                     Y1,SHAIKSHAZID,P,P,P,P,AB,P,AB,P,AB,P,P,P,P,AB,P,P,P
#                     Y2,SHEIKARIF,P,P,P,P,AB,P,P,P,P,P,P,P,P,P,P,P,P
#                     Y3,SHEIKNOORJAHAN,P,P,AB,P,AB,P,P,P,P,P,P,AB,P,AB,P,P,P
#                     Y4,SHETTITEJASWARI,P,P,AB,P,P,P,P,P,P,P,AB,P,AB,P,P,P,P
#                     Y5,SIDAGAMRAJESH,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
#                     Y6,SIDDAANITHA,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
#                     Y7,SIGALAPELLIPAVANKUMAR,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
#                     Y8,SIRIPURAPURAGHU,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
#                     Y9,SIRIPURAPUTRINADHA,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
#                     Z0,SIVVITIKIRANMAYEE,AB,AB,P,P,P,P,AB,AB,P,AB,AB,P,P,AB,AB,AB,AB
#                     Z2,SURUAKSHAYA,P,P,P,P,P,P,P,P,P,P,P,P,P,AB,P,P,P
#                     Z3,TAKARLARONITHREDDY,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
#                     Z4,TALACHUTLAHASINI,P,P,P,P,AB,P,AB,P,P,P,P,P,P,AB,P,P,P
#                     Z5,TALADAKAVYAJAHNAVI,P,P,AB,P,AB,P,P,P,P,P,P,P,P,P,P,P,P
#                     Z6,TALADASREEVENKATESH,P,P,P,P,AB,P,P,AB,P,P,P,P,P,P,P,P,P
#                     Z7,TALEBHANUTEJA,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
#                     Z8,TEDLAPUSAIREESHNIKA,P,P,P,P,P,AB,AB,P,P,P,P,P,P,P,P,AB,P
#                     Z9,TEDLAPUSHANMUKHESWAR,P,P,P,P,P,P,P,AB,P,P,P,P,P,P,P,P,P
#                     AA,TEEDAJENYA,P,P,P,P,P,P,P,P,AB,P,P,P,P,P,P,P,P
#                     AB,TEEDASRILAKSHMI,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
#                     AC,TELUKALAKEERTHANA,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
#                     AD,THADDIVINAY,P,P,P,P,P,AB,AB,P,P,P,P,P,AB,AB,AB,P,P
#                     AE,THAMMINATEJASWI,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
#                     AF,THOTAGAYATHRISRUJANA,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
#                     AG,THUMMAGANTIGANESH,P,P,P,P,P,P,AB,P,P,P,P,P,AB,P,P,P,P
#                     AH,TIPPANASAINIKHILESH,P,P,P,AB,AB,AB,P,P,P,P,P,P,P,P,P,P,P
#                     AI,TRIPURAGIRIAKHILA,P,P,P,AB,P,P,AB,P,P,P,P,P,P,P,P,P,P
#                     AJ,TULUGUGAYATHRI,P,P,P,P,AB,P,P,P,AB,P,P,P,P,P,P,P,P
#                     AK,UPPALAPATIYOGENDRAVARMA,P,P,AB,P,P,P,P,P,P,P,P,P,P,P,P,AB,P
#                     AL,VADAPALLILIKHITHMANOHAR,P,P,P,P,P,AB,P,P,P,P,P,P,P,P,P,P,P
#                     AM,VADDADINAGESHKUMAR,P,P,P,P,P,AB,P,P,P,P,P,AB,AB,P,P,P,P
#                     AN,VADUGURUSRINIDHI,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
#                     AO,VAKAMULLULAKSHMINARAYANA,P,P,P,P,P,P,P,P,P,P,P,P,P,AB,P,P,P
#                     AP,VALLURIRANADHEERNAIDU,AB,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
#                     AQ,VANKAYASWANTHESWAR,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,AB,P
#                     AR,VARREJAGADEESH,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
#                     AS,VARRILEELAKRISHNA,P,P,P,AB,P,P,P,P,AB,P,AB,P,P,AB,P,P,P
#                     AT,VARRINEELIMA,P,P,P,P,P,P,P,P,P,P,P,P,P,AB,P,P,P
#                     AU,VEMPADAPUMOHINI,P,P,P,P,P,P,P,P,P,P,P,P,P,AB,P,P,P
#                     AV,VEMPADAPUUMAJYOTHSNA,P,P,P,P,AB,P,P,P,P,P,P,P,P,AB,P,P,P
#                     AW,YADLASAIDEEKSHITHA,P,P,P,P,P,P,P,P,P,P,P,P,P,,P,P,P
#                     AX,YAJJALAKISHOR,P,P,P,P,P,P,P,P,P,P,P,P,P,AB,P,P,P
#                     AY,YALAANUSH,P,P,P,P,P,AB,P,P,P,P,P,P,P,AB,P,P,P
#                     AZ,YALLASAMUELSATHVIK,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
#                     BA,YANDRAPUVAMSI,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
#                     BB,YARRAMADHUSUDHANARAO,P,P,P,P,AB,P,P,P,P,P,P,P,P,P,P,P,P
#                     BD,YARRARAPUPUNYAVATHI,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
#                     BE,YEGIREDDYTEJA,P,P,P,P,P,P,P,P,P,P,P,P,P,AB,P,P,P
#                     BF,YELAMANCHILIRAKESH,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
#                     BG,YELUSOORIVIJAY,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
#                     BH,YERRARUPESH,P,AB,AB,AB,AB,AB,P,P,P,AB,AB,AB,AB,P,P,AB,P
#                     BI,YERRASHYAMCHANDU,P,AB,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
#                     BJ,YERRASIRICHANDANA,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
#                     BK,YETURISURESH,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P
#                     """
                    
#                     july_df = pd.read_csv(StringIO(july), header=0, index_col=0)
#                     july_df.index = july_df.index.str.strip()
#                     july_df = july_df[july_df.index == user]


#                     august_df = pd.read_csv(StringIO(august), header=0, index_col=0)
#                     august_df.index = august_df.index.str.strip()
#                     august_df = august_df[august_df.index == user]


#                     sept_df = pd.read_csv(StringIO(sept), header=0, index_col=0)
#                     sept_df.index = sept_df.index.str.strip()
#                     sept_df = sept_df[sept_df.index == user]


#                     # Show dataframes in columns
#                     j, a, s = st.columns([1, 1, 1])
#                     with j:
#                         st.dataframe(july_df.T)
#                         st.download_button(
#                             label="Download July Report",
#                             data=july_df.to_csv(index=False).encode('utf-8'),
#                             file_name=f"{user}_julyattendance.csv",
#                             mime='text/csv',
#                             key=f"july_{user}_download"
#                         )

#                     with a:
#                         st.dataframe(august_df.T)
#                         st.download_button(
#                             label="Download August Report",
#                             data=august_df.to_csv(index=False).encode('utf-8'),
#                             file_name=f"{user}_augustattendance.csv",
#                             mime='text/csv',
#                             key=f"august_{user}_download"
#                         )

#                     with s:
#                         st.dataframe(sept_df.T)
#                         st.download_button(
#                             label="Download Sept Report",
#                             data=sept_df.to_csv(index=False).encode('utf-8'),
#                             file_name=f"{user}_septattendance.csv",
#                             mime='text/csv',
#                             key=f"sept_{user}_download"
#                         )

    
        
# #   ======================= ADMIN( RAAMANAND: ME ) TAB ============================

#     elif page == "👨‍🔬 Admin":
#         st.title("👨‍🔬 Admin Panel")
#         def write(msg):
#             with open(GOOD_NEWS, mode='w', encoding='utf-8') as f:
#                 f.write(msg) 

#         if st.session_state.get("device_id", None) in ['a9513efb32968fd6881b89f36f221a254578ba203239086a6d39e2a72b5eb847','45c71d8124d5773d2afc93d2716451a4be8cfcb955bf6d8acdca26066cacc755','eafceb45d73ebd141a9d7dcc0ed4310bd40e05d5e72c3ccb2d8f5b9b87cc7e3f']:
#             st.header("📢 Announcement Management")
#             message = st.text_input(label = "New Announcement:", placeholder='Enter your messsage...')
#             if st.button("🔊 Publish Announcement"):
#                 write(message)
        
#             if st.button("🔇 Clear Announcement"):
#                 write("")
#             st.write("---")
#             st.header("📊 System Statistics")
#             try:
#                 x,y,z=st.columns(3)
#                 with x:
#                     st.metric(f"Total Students",len(CLASS_ROLL_NUMBERS))  
#                 with y:
#                     st.metric(f"Registered Students",len(pd.read_csv(MARKED_FILE)['Roll_no'].tolist()))
#                 with z:
#                     st.metric(f"Today's Attendance", len(pd.read_csv(ATTENDANCE_FILE)[pd.read_csv(ATTENDANCE_FILE)['Date'] == datetime.today().strftime("%Y-%m-%d")]))
#             except:
#                 st.error("Files not created yet!!")
#             st.write("---")  
#             try:
#                 st.header("User Feedbacks: ")
#                 feedback_df = pd.read_csv(FEEDBACK_FILE) 
#                 for i,j in feedback_df.iterrows():
#                     st.write(f"{j[0]}: {j[1]}")    
#             except:
#                 st.info("No one has yet given the feedback!!")           
#             st.write("---")
#             st.header("🔧 System Maintenance")
#             if st.button("🔄 Clear All Data", type="secondary"):
#                 for file in [ATTENDANCE_FILE, MESSAGE_FILE, PERMISSIONS_FILE, POLLS, FEEDBACK_FILE]:
#                     if os.path.exists(file):
#                         os.remove(file)
#                 st.success("All data cleared!") 
#         else:
#             st.error("🚫 Access denied. Admin privileges required.")

# #   ======================= ABOUT TAB ===========================

#     elif page == "ℹ️ About":
#             from datetime import datetime

#             APP_NAME = "Presaloc Pro"
#             VERSION = "v2.0"
#             DEVELOPER = "Saketh (Rupesh)"
#             LAST_UPDATE = datetime(2025, 10, 27)

#             about_header = f"""
#              # Welcome to **{APP_NAME}** app!

#              A professional system designed to verify and secure attendance across classes (students, CRs, mentors, admin), all with advanced, modern technology and strict validation.
            
#             ---
#             Updated Recently on: {LAST_UPDATE}\n
#             Welcome to my advanced, location-based attendance management platform—engineered to deliver reliable, secure, and automated attendance for educational institutions and organizations.
#             """

#             st.markdown(about_header)
#             st.subheader("Advanced Features")
#             st.markdown(
#             """
#             - **Smart Location Validation:** Ensures users are at authorized physical locations before marking attendance (uses HTML5 Geolocation API).
#             - **Role-Based Security:** Custom access control for students, admins, and supervisors with encrypted session tokens.
#             - **Real-Time Analytics:** Visual dashboards, attendance statistics, and downloadable reports.
#             - **Proxy Prevention:** Strict geolocation and session checks to block fraudulent or duplicate entries.
#             """
#             )
#             st.error("⚠️⚠️**One Time Registration:** This feature will not allow any user to use another user's details. And once registered to a device, that very device owner could only use those details.")
            

#             st.write("---")
#             st.info("Driven by a passion for building robust, real-world solutions for education and organizations.")

#             st.metric(label="App Version", value="v2.0", delta="+1 new feature")
#             st.metric(label="Active Users", value="000", delta="+2 this week")

#             tab1, tab2 = st.tabs(["Overview", "Technical Details"])
#             with tab1:
#                 st.markdown("""
#                 Welcome to our advanced, location-based attendance platform.
#                 - **Location Validation**
#                 - **Security & Analytics**
#                 - Role-based access
#                 """)
#             with tab2:
#                 st.subheader("Technology Stack")
#                 col1, col2 = st.columns(2)
#                 with col1:
#                     st.markdown(
#                         """
#                         - Python 3.13+
#                         - Streamlit
#                         - SQLite (Data Storage)
#                         - HTML5 Geolocation
#                         """
#                     )
#                 with col2:
#                     st.markdown(
#                         """
#                         - Pandas (Data Handling)
#                         - Secure Session Management
#                         - Responsive Web UI
#                         - Real-time Data Analytics
#                         """
#                     )

#             with st.expander("Meet the Developer"):
#                 st.write("Created by Saketh (Rupesh), a student developer passionate about practical AI solutions.")

#             st.download_button("Download App Manual", """~ A Website made by Saketh (Rupesh).""", file_name="manual.txt")

# #   ======================= SETTINGS TAB ========================

#     elif page == "⚙️ Settings":
#             st.header("🛠️ Account Settings")
#             with st.form("Settings_form"):
#                 st.subheader("🔒 Change Password")
#                 prev_name=st.text_input("Enter Current Username: ", placeholder=f"E.g: YAKSHRAJ").strip()
#                 prev_pass=st.text_input("Enter Current password: ", placeholder='******', type='password').strip()
#                 curr_pass=st.text_input("Enter New password: ", placeholder="******", type='password').strip()
#                 if st.form_submit_button("Update Password"):
#                     if prev_name == "" or prev_pass == "" or curr_pass == "":
#                         st.warning("All fields are required!!")
#                     elif not password_df.loc[password_df['user_name'] == prev_name, 'pass'].empty and prev_pass == password_df.loc[password_df['user_name'] == prev_name, 'pass'].values[0]:
#                         password_df.loc[password_df['user_name']==prev_name, 'pass'] = curr_pass 
#                         password_df.to_csv(PASS_FILE, index=False)
#                         st.success(f"Password has changed to {password_df.loc[password_df['user_name'] == prev_name, 'pass'].values[0]}")
        
#                     elif password_df.loc[password_df['user_name'] == prev_name].empty or prev_name not in password_df['user_name'].to_list():
#                         st.error("User Name is incorrect!")
#                     elif prev_pass != password_df.loc[password_df['user_name'] == prev_name, 'pass'].values[0]:
#                         st.error("The password is incorrect!!")
        
#                     else:
#                         st.error("❌❌ Error Occured!!")
#             st.write("---")
#             st.subheader("📱 Device Information")
#             st.write(f"**Device ID:** {st.session_state['device_id']}")
#             st.write(f"**Session ID:** {get_script_run_ctx().session_id if get_script_run_ctx() else 'N/A'}")
        
#             st.write("---")
        
#             if st.button("🚪 Logout", type="primary"):
#                 for key in list(st.session_state.keys()):
#                     del st.session_state[key]
#                 st.rerun() 
    
    
#     elif page == "🪧 NoticeBoard":
#         st.title("🪧 NoticeBoard")
#         st.info("No significant highlights are available!!") 
        
#     elif page == "🧑‍🍼 Feedback":
#         st.title("Drop your feedback here (if any) !")
#         st.write("---")
#         st.subheader("Feedback form:")
#         with st.form("FeedbackForm"):
#             feed_name = st.text_input("Name:") 
#             feedback = st.text_area("Feedback: ", placeholder = 'Type your feedback here!!')
#             if st.form_submit_button("Submit!"):
#                 if feedback != "" and feed_name != "":
#                     if not os.path.exists(FEEDBACK_FILE):
#                         feedback_df = pd.DataFrame({'name':[feed_name], 'feedback': [feedback]})
#                         feedback_df.to_csv(FEEDBACK_FILE, index=False) 
#                     st.success("🙏 Thank you for giving your feedback!!")
#                     import time
#                     time.sleep(2)
#                 elif feed_name == "":
#                     st.warning("Kindly enter the name you wanted to be appeleated with!")
#         st.write("---")
# st.caption("~An app by Saketh (Rupesh), accomplished in 5-6 days & completed prior to 27th October 2025.")




