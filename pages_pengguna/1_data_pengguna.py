import streamlit as st
import datetime
from assets import database as db
import time
with st.form("form-update-data-pasien"):
    st.title("Update Data Pasien")
    st.warning("Apabila ada nilai yang tidak ingin diubah, jangan diganti!")
    username = st.text_input("Masukkan username baru: ", value=st.session_state.username_pengguna)
    password = st.text_input("Masukkan password baru: ", type= "password", value=st.session_state.password_pengguna)
    nama = st.text_input("Masukkan nama lengkap baru: ", value=st.session_state.nama_lengkap)
    jenis_kelamin = st.radio("Jenis Kelamin: ", ("LAKI-LAKI", "PEREMPUAN"), horizontal=True, index=("LAKI-LAKI", "PEREMPUAN").index(st.session_state.jenis_kelamin))
    alamat = st.text_input("Masukkan alamat baru: ", value=st.session_state.alamat)
    email = st.text_input("Masukkan email baru: ", value=st.session_state.email)
    

    pekerjaan = st.selectbox("Masukkan pekerjaan baru: ", options=st.session_state.pekerjaan_pekerjaan, index=st.session_state.pekerjaan_pekerjaan.index(st.session_state.pekerjaan)) 
    tanggal_lahir = st.date_input("Masukkan tanggal lahir: (y-m-d)", min_value=datetime.date(1900, 1, 1), max_value=datetime.datetime.now(), value=st.session_state.tanggal_lahir)
    
    
    col1, col2 = st.columns(2)
    
    with col2:
        if st.form_submit_button(label="Update"):

            
            validation_errors = []
            
            if db.cek_username(username) == True and username != st.session_state.username_pengguna:
                validation_errors.append("Username sudah terdaftar")

                
            if db.cek_email(email) == True and email != st.session_state.email:
                validation_errors.append("Email Sudah Terdaftar")
            # Check if username is provided
            if not st.session_state.username_pengguna:
                validation_errors.append("Username tidak boleh kosong.")

            # Check if password is provided and meets the length requirement
            if not password or not db.validasi_password(password):
                validation_errors.append("Password harus lebih dari 6 karakter.")

            # Check if full name is provided
            if not nama:
                validation_errors.append("Nama lengkap tidak boleh kosong.")

            # Check if email is provided and valid
            if not email or not db.validasi_email_regex(email):
                validation_errors.append("Email tidak valid. Pastikan menggunakan format yang benar (@gmail.com).")

            # Check if address is provided
            if not alamat:
                validation_errors.append("Alamat tidak boleh kosong.")

            # Display validation errors
            if validation_errors:
                for error in validation_errors:
                    st.error(error)
            else:
                st.success("Update Data Anda Berhasil!.")
                db.update_pengguna(username, password, nama, jenis_kelamin, alamat, email, pekerjaan, tanggal_lahir, st.session_state.username_pengguna)
                
                st.session_state.username_pengguna = username
                st.session_state.next = 0
                st.session_state.update_data = 0
                time.sleep(2)
                st.rerun()
    with col1:
        if st.form_submit_button(label="Kembali"):
            st.session_state.next = 0
            st.rerun()