import os
import streamlit as st
import hashlib 
from cryptography.fernet import Fernet

#HASHING
def hash_password(password:str):
    return hashlib.sha256(password.encode()).hexdigest()

if not os.path.exists("secret.key"):
    key = Fernet.generate_key()

    with open("secret.key","wb") as file:
        file.write(key)

#KEY GENERATION
def load_key():
    return open("secret.key","rb").read()

#ENCRYPTION AND DECRYPTION
def encrypt(password:str):
    key = load_key()
    f = Fernet(key)
    return f.encrypt(password.encode()).decode()

def decrypt(encrypted_password:str):
    key = load_key()
    f = Fernet(key)
    return f.decrypt(encrypted_password.encode()).decode()

#MASTER_PASS GENERATER
def master_password_gen(new_pass):
    hashed = hash_password(new_pass)
    with open("master_password.txt","w") as file:
        file.write(hashed)

#ACCESS CHECK
def access(password):
    hashed_pass = hash_password(password)
    with open("master_password.txt",'r') as file:
        stored_hash = file.readline().strip()
    if hashed_pass == stored_hash:
        return True
    else: 
        return False

#ADDING PASSWORD
def add_pass(platform, password):
    with open("passwords.txt", "a") as file:
        file.write(f"{platform},{encrypt(password)}\n")

#VIEWING ALL PASSWORDS
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

#DELETING PASSWORD
def delete_password(index):
    passwords = view_pass()

    if 0 <= index <len(passwords):
        passwords.pop(index)
    
    with open("passwords.txt", "w") as file:
        for platform, pw in passwords:
            file.write(f"{platform},{pw}\n")

#EDIT PASSWORD
def edit_password(index, new_platform, new_password):
    passwords = view_pass()

    if not passwords:
        return

    if 0 <= index <len(passwords):
        passwords[index] = (new_platform, encrypt(new_password))

        with open("passwords.txt", "w") as file:
            for platform, pw in passwords:
                file.write(f"{platform}, {pw}\n")


#MAIN APP
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

#SESSION_STATES
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "edit_index" not in st.session_state:
    st.session_state.edit_index = None


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

with st.form("add_password_form", clear_on_submit= True):
    platform_input = st.text_input("Enter platform: ")
    password_input = st.text_input("Enter Password: ", type = "password")
    submitted = st.form_submit_button("Save Password")

if submitted:
    if platform_input == "" or password_input == "":
        st.error("All fields must be filled..")
    
    else:
        add_pass(platform_input, password_input)
        st.success("Password Saved!")

st.subheader("Passwords:")

passwords = view_pass()

if passwords:
    if "reveal" not in st.session_state:
        st.session_state.reveal = {}
    for idx, (platform, passw) in enumerate(passwords):
        if idx not in st.session_state.reveal:
            st.session_state.reveal[idx] = False

        col1, col2, col3, col4, col5 = st.columns([2,1,1,1,1])
        col1.write(platform)
        
        if st.session_state.reveal[idx]:
            col2.write(decrypt(passw))
        else:
            col2.write("******")

        if col3.button("👁", key = f"rev_{idx}"):
            st.session_state.reveal[idx] = not st.session_state.reveal[idx]
            st.rerun()
        
        if col4.button("✏️", key=f"edit_{idx}"):
            st.session_state.edit_index = idx
            st.rerun()

        if col5.button("🗑️", key= f"dlt_{idx}"):
            delete_password(idx)
            st.session_state.reveal.pop(idx, None)
            st.rerun()

        if st.session_state.edit_index == idx:
            with st.form("edit_password", clear_on_submit= True):
                new_platform = st.text_input("Enter New Platform:")
                new_password = st.text_input("Enter New Password: ", type="password")
                save = st.form_submit_button("Save Changes")
                cancel = st.form_submit_button("Cancel")

                if save:
                    if new_platform == "" or new_password == "":
                        st.error("Fields cannot be empty.")
                    
                    else:
                        edit_password(idx,new_platform, new_password)
                        st.success("Saved Changes!")

                        st.session_state.edit_index = None
                        st.rerun()
                
                if cancel:
                    st.session_state.edit_index = None
                    st.rerun()
else:
    st.info("No passwords stored yet..")


if st.button("Logout"):
    st.session_state.authenticated = False
    st.rerun()




        
        

        



