import os
import streamlit as st

def master_password_gen(new_pass):
    with open("master_password.txt","w") as file:
        file.write(new_pass)

def access(password):
    with open("master_password.txt",'r') as file:
        code = file.readline().strip()
    if password == code:
        return True
    else: 
        return False

def add_pass(platform, password):
    with open("passwords.txt", "a") as file:
        file.write(f"{platform},{password}\n")

def view_pass():
    password = []
    try:
        with open("passwords.txt", "r") as file:
            for line in file:
                platform, pw = line.strip().split(',')
                password.append((platform,pw))
        
    except FileNotFoundError:
        return 
    
    return password


st.title("Password Manager <3")

#FIRST TIME SETUP
if not os.path.exists("master_password.txt"):
    st.subheader("Set Master Password:")
    new_pass = st.text_input("Enter new master password:", type="password")
    if st.button("Save Master Password"):
        if new_pass == "":
            st.write("Master Password cannot be empty...")

        else:
            master_password_gen(new_pass)
            st.success("Master Password Set! (Refresh to continue)")
    st.stop()

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

#LOGIN
if not st.session_state.authenticated:
    st.subheader("Login")
    password = st.text_input("Enter master password:", type = "password")
    
    if st.button("Login"):
        if access(password):
            st.session_state.authenticated = True
            st.success("Access Granted!")
            st.rerun()
        else:
            st.error("Access Denied...")

    st.stop()

#Menu

st.subheader("Add Password")
new_pass = st.text_input("Enter Password", type = "password")
platform = st.text_input("Enter Platform")

if st.button("Save Password"):
    if new_pass == "" or platform == "":
        st.error("All fields must be filled...")
    
    else:
        add_pass(platform, new_pass)
        st.success("Password Added!")

st.subheader("Passwords:")

passwords = view_pass()

if passwords:
    if "reveal" not in st.session_state:
        st.session_state.reveal = {}
    for idx, (platform, passw) in enumerate(passwords):
        if idx not in st.session_state.reveal:
            st.session_state.reveal[idx] = False

        col1, col2, col3 = st.columns([2,1,1])
        col1.write(platform)
        
        if st.session_state.reveal[idx]:
            col2.write(passw)
        else:
            col2.write("******")

        if col3.button("👁", key = f"btn_{idx}"):
            st.session_state.reveal[idx] = not st.session_state.reveal[idx]
            st.rerun()

else:
    st.info("No passwords stored yet..")




        
        

        



