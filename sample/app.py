import streamlit as st
import pandas as pd
from datetime import datetime
import os
# from kivymd.app import MDApp
# from kivymd.uix.label import MDLabel 

# class Mainapp(MDApp):
# File to store attendance data
ATTENDANCE_FILE = 'attendance.csv'

# Initialize CSV if it doesn't exist
if not os.path.exists(ATTENDANCE_FILE):
    df = pd.DataFrame(columns=['Name', 'Date'])
    df.to_csv(ATTENDANCE_FILE, index=False)
#'X1', 'X2', 'X3', 'X4', 'X5', 'X6', 'X7', 'X8', 'X9',
# Load existing attendance data
attendance_df = pd.read_csv(ATTENDANCE_FILE)

st.title('CSE Attendance Checker!!')
st.header('Enter the following details:')

options = ['X1', 'X2', 'X3', 'X4', 'X5', 'X6', 'X7', 'X8', 'X9','Y1', 'Y2', 'Y3', 'Y4', 'Y5', 'Y6', 'Y7', 'Y8', 'Y9','Z1', 'Z2', 'Z3', 'Z4', 'Z5', 'Z6', 'Z7', 'Z8', 'Z9', 'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'AG', 'AH', 'AI', 'AJ', 'AK', 'AL', 'AM',
 'AN', 'AO', 'AP', 'AQ', 'AR', 'AS', 'AT', 'AU', 'AV', 'AW', 'AX', 'AY', 'AZ', 'BA', 'BB', 'BC', 'BD', 'BE', 'BF', 'BG', 'BH', 'BI', 'BJ', 'BK', 'BL',
 'BM', 'BN', 'BO', 'BP', 'BQ', 'BR', 'BS', 'BT', 'BU', 'BV', 'BW', 'BX', 'BY', 'BZ']
passwords = {rn: 'In' + rn + '@123' for rn in options}
rep_password = 'REP123'  # Special password for class reps to view attendance

# Role selection
role = st.radio('Select Your Role:', ['Student', 'Class Representative'])

if role == 'Student':
    selected = st.selectbox('Who are You?', options)
    password = st.text_input("Enter Secret Password:", type='password')
    
    if st.button('Mark Present?'):
        today = datetime.today().strftime('%Y-%m-%d')
        if selected not in attendance_df[(attendance_df['Name'] == selected) & (attendance_df['Date'] == today)]['Name'].values:
            if passwords[selected] == password:
                # Add to DataFrame and save
                new_entry = pd.DataFrame({'Name': [selected], 'Date': [today]})
                attendance_df = pd.concat([attendance_df, new_entry], ignore_index=True)
                attendance_df.to_csv(ATTENDANCE_FILE, index=False)
                st.success(f"You ({selected}) are now marked as present for {today}!")
            else:
                st.error('WRONG PASSWORD!!')
        else:
            st.warning(f"{selected} is already marked present for {today}.")

elif role == 'Class Representative':
    rep_pass = st.text_input("Enter Rep Password:", type='password')
    selected_date = st.date_input("Select Date to View Attendance:", value=datetime.today())
    selected_date_str = selected_date.strftime('%Y-%m-%d')
    
    if st.button('View Attendance'):
        if rep_pass == rep_password:
            # Filter attendance for the selected date
            daily_attendance = attendance_df[attendance_df['Date'] == selected_date_str]
            present_list = daily_attendance['Name'].tolist()
            absent_list = [name for name in options if name not in present_list]
            
            st.subheader(f'Attendance for {selected_date_str}:')
            
            # Centered columns for Present and Absent
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
    
    # Optional: Reset attendance for a date (for reps)
    if st.button('Reset Attendance for Selected Date') and rep_pass == rep_password:
        attendance_df = attendance_df[attendance_df['Date'] != selected_date_str]
        attendance_df.to_csv(ATTENDANCE_FILE, index=False)
        st.info(f"Attendance reset for {selected_date_str}!")








