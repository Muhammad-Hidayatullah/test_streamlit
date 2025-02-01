import streamlit as st
import mysql.connector
import pandas as pd
from fpdf import FPDF
import io
import re


# Accessing secrets using the 'mysql' key
db_credentials = st.secrets["mysql"]

# Connecting to the database
def connect_to_db():
    
    db_credentials = {
        "host": st.secrets["mysql"]["host"],
        "user": st.secrets["mysql"]["username"],
        "password": st.secrets["mysql"]["password"],
        "database": st.secrets["mysql"]["database"],
        "port": st.secrets["mysql"]["port"]
    }
    
    return mysql.connector.connect(
        host=db_credentials["host"],
        user=db_credentials["user"],
        password=db_credentials["password"],
        database=db_credentials["database"],
        port=db_credentials["port"]
    )


def forward_chaining(fakta, aturan):
    # Penyakit yang mungkin didiagnosis
    kemungkinan_penyakit = {}
    
    for penyakit, gejala_penyakit in aturan.items():
        # Hitung jumlah gejala yang cocok
        gejala_cocok = fakta.intersection(gejala_penyakit)
        kemungkinan_penyakit[penyakit] = len(gejala_cocok) / len(gejala_penyakit)
    
    # Filter penyakit dengan tingkat kecocokan tinggi (contoh: > 70%)
    hasil = {penyakit: kecocokan for penyakit, kecocokan in kemungkinan_penyakit.items() if kecocokan > 0.5}
    
    return hasil

def validasi_email_regex(email):
    regex = r'^[a-zA-Z0-9_.+-]+@gmail\.com$'
    return re.match(regex, email) is not None

def validasi_password(password):
    
    return len(password) >= 7


def get_name(username, password):
    try:
        connection = connect_to_db()
        cursor = connection.cursor()

        # SQL query to check user credentials
        query = "SELECT name FROM pengguna WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))

        # Fetch one result
        name = cursor.fetchone()

        return name[0] if name else None
       

    except mysql.connector.Error as err:
        st.error(f"Database error: {err}")  # Show the error
        return False  # Indicate failure

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
            
def get_tanggal_lahir_pasien(username, password):
    try:
        connection = connect_to_db()
        cursor = connection.cursor()

        # SQL query to check user credentials
        query = "SELECT tanggal_lahir FROM pasien WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))

        # Fetch one result
        name = cursor.fetchone()

        return name[0] if name else None
       

    except mysql.connector.Error as err:
        st.error(f"Database error: {err}")  # Show the error
        return False  # Indicate failure

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def get_data_pasien(username):
    conn = connect_to_db()
    cursor = conn.cursor()
    query = "SELECT * FROM pasien WHERE username = %s"
    cursor.execute(query, (username,))
    result = cursor.fetchone()
    conn.close()
    return result if result else None
    
    
     
def fetch_faktor_risiko():
    conn = connect_to_db()
    query = "SELECT nama_risiko, deskripsi FROM faktor_risiko;"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

#UNTUK PENYAKIT
def fetch_penyakit():
    conn = connect_to_db()
    query = "SELECT * FROM komplikasi_penyakit;"
    df = pd.read_sql(query, conn)
    conn.close()
    return df


def add_komplikasi_penyakit(id_komplikasi_penyakit, nama_penyakit, penjelasan, solusi):
    conn = connect_to_db()
    cursor = conn.cursor()
    
    query = "INSERT INTO komplikasi_penyakit (id_komplikasi_penyakit, nama_penyakit, penjelasan, solusi) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (id_komplikasi_penyakit, nama_penyakit, penjelasan, solusi))
    conn.commit()
    st.success("Komplikasi Penyakit Berhasil Ditambahkan")
    conn.close()
    
    
def update_komplikasi_penyakit(id_komplikasi_penyakit, nama_penyakit, penjelasan, solusi):
    conn = connect_to_db()
    cursor = conn.cursor()
    
    query = "UPDATE komplikasi_penyakit SET nama_penyakit = %s, penjelasan = %s, solusi = %s WHERE id_komplikasi_penyakit = %s"
    
    cursor.execute(query, (nama_penyakit, penjelasan, solusi, id_komplikasi_penyakit))
    conn.commit()
    st.success("Penyakit Berhasil Diupdate")
    conn.close()
    
    
    
def hapus_komplikasi_penyakit(id_komplikasi_penyakit):
    conn = connect_to_db()
    cursor = conn.cursor()
    
    query = "DELETE FROM komplikasi_penyakit WHERE id_komplikasi_penyakit =  %s"
    
    cursor.execute(query, (id_komplikasi_penyakit,)) #harus ditambah koma ,
    conn.commit()
    st.success("Penyakit Berhasil Dihapus")
    conn.close()
    

    
    
#UNTUK GEJALA

def fetch_gejala():
    conn = connect_to_db()
    query = "SELECT * FROM `gejala` ORDER BY `id_gejala` ASC;"
    df = pd.read_sql(query, conn)
    conn.close()
    return df


def add_gejala(id_gejala, nama_gejala):
    conn = connect_to_db()
    cursor = conn.cursor()
    
    query = "INSERT INTO gejala (id_gejala, nama_gejala) VALUES (%s, %s)"
    cursor.execute(query, (id_gejala, nama_gejala))
    conn.commit()
    
    st.success("Gejala Berhasil Ditambahkan")
    conn.close()
    
    
def update_gejala(id_gejala, nama_gejala):
    conn = connect_to_db()
    cursor = conn.cursor()
    
    query = "UPDATE gejala SET nama_gejala = %s WHERE id_gejala = %s"
    
    cursor.execute(query, (nama_gejala, id_gejala))
    conn.commit()
    st.success("Gejala Berhasil Diupdate")
    conn.close()
    

def hapus_gejala(id_gejala):
    conn = connect_to_db()
    cursor = conn.cursor()
    
    query = "DELETE FROM gejala WHERE id_gejala =  %s"
    
    cursor.execute(query, (id_gejala,)) #harus ditambah koma ,
    conn.commit()
    st.success("Gejala Berhasil Dihapus")
    conn.close()
    
def nama_gejala(id_gejala):
    conn = connect_to_db()
    cursor = conn.cursor()
    query = "SELECT nama_gejala FROM gejala WHERE id_gejala = %s"
    cursor.execute(query, (id_gejala,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None
    
    
#UNTUK GEJALA
def fetch_relasi_penyakit_dan_gejala_full():
    conn = connect_to_db()
    query = "SELECT relasi_penyakit_gejala.id_komplikasi_penyakit, komplikasi_penyakit.nama_penyakit, relasi_penyakit_gejala.id_gejala, gejala.nama_gejala FROM relasi_penyakit_gejala JOIN komplikasi_penyakit ON relasi_penyakit_gejala.id_komplikasi_penyakit = komplikasi_penyakit.id_komplikasi_penyakit JOIN gejala ON relasi_penyakit_gejala.id_gejala = gejala.id_gejala;;"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def fetch_relasi_penyakit_dan_gejala():
    conn = connect_to_db()
    cursor = conn.cursor()
    query = "SELECT id_komplikasi_penyakit, id_gejala FROM relasi_penyakit_gejala;"
    cursor.execute(query)
    data_relasi_penyakit_dan_gejala = cursor.fetchall()
    conn.close()
    return data_relasi_penyakit_dan_gejala



def fetch_relasi_nama_penyakit_dan_nama_gejala():
    conn = connect_to_db()
    cursor = conn.cursor()
    query = "SELECT komplikasi_penyakit.nama_penyakit, gejala.nama_gejala FROM relasi_penyakit_gejala JOIN komplikasi_penyakit ON relasi_penyakit_gejala.id_komplikasi_penyakit = komplikasi_penyakit.id_komplikasi_penyakit JOIN gejala ON relasi_penyakit_gejala.id_gejala = gejala.id_gejala;"

    cursor.execute(query)
    relasi_nama_penyakit_dan_nama_gejala = cursor.fetchall()
    conn.close()
    return relasi_nama_penyakit_dan_nama_gejala
    

def get_solusi_penyakit(nama_penyakit):
    conn = connect_to_db()
    cursor = conn.cursor()
    query = "SELECT solusi FROM komplikasi_penyakit WHERE nama_penyakit = %s"
    cursor.execute(query, (nama_penyakit,))
    solusi = cursor.fetchone()
    conn.close()
    return solusi[0] if solusi else None
    

def add_relasi_penyakit_dan_gejala(id_komplikasi_penyakit, id_gejala):
    conn = connect_to_db()
    cursor = conn.cursor()
    
    query = "INSERT INTO relasi_penyakit_gejala (id_komplikasi_penyakit, id_gejala) VALUES (%s, %s)"
    cursor.execute(query, (id_komplikasi_penyakit, id_gejala))
    conn.commit()
    
    st.success("Relasi Penyakit dan Gejala Berhasil Ditambahkan")
    conn.close()
    
    
def update_relasi_penyakit_dan_gejala(id_komplikasi_penyakit, id_gejala, id_gejala_baru):
    conn = connect_to_db()
    cursor = conn.cursor()
    
    query = "UPDATE relasi_penyakit_gejala SET id_gejala = %s WHERE id_komplikasi_penyakit = %s AND id_gejala = %s"

    cursor.execute(query, (id_gejala_baru, id_komplikasi_penyakit, id_gejala))
    
    conn.commit()
    st.success("Relasi Penyakit dan Gejala Berhasil Diupdate")
    conn.close()


def hapus_relasi_penyakit_dan_gejala(id_komplikasi_penyakit, id_gejala):
    conn = connect_to_db()
    cursor = conn.cursor()
    
    query = "DELETE FROM relasi_penyakit_gejala WHERE id_komplikasi_penyakit = %s AND id_gejala = %s"
    
    cursor.execute(query, (id_komplikasi_penyakit, id_gejala)) #harus ditambah koma ,
    conn.commit()
    st.success("Relasi Penyakit dan Gejala Berhasil Dihapus")
    conn.close()



def fetch_artikel():
    conn = connect_to_db()
    query = "SELECT * FROM artikel;"
    df = pd.read_sql(query, conn)
    conn.close()
    return df



def add_artikel(nama_website, link_gambar, judul_artikel, nama_penulis, tanggal_artikel, link_artikel):
    conn = connect_to_db()
    cursor = conn.cursor()
    
    query = "INSERT INTO artikel (nama_website, link_gambar, judul_artikel, nama_penulis, tanggal_artikel, link_artikel) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.execute(query, (nama_website, link_gambar, judul_artikel, nama_penulis, tanggal_artikel, link_artikel))
    conn.commit()
    conn.close()
    

def update_artikel(nama_website, link_gambar, judul_artikel, nama_penulis, tanggal_artikel, link_artikel, id_artikel):
    conn = connect_to_db()
    cursor = conn.cursor()
    
    query = "UPDATE artikel SET nama_website = %s, link_gambar = %s, judul_artikel = %s, nama_penulis = %s, tanggal_artikel = %s, link_artikel = %s WHERE id_artikel= %s"

    cursor.execute(query, (nama_website, link_gambar, judul_artikel, nama_penulis, tanggal_artikel, link_artikel, id_artikel))
    conn.commit()
    st.success("Artikel Berhasil Diupdate")
    conn.close()

def hapus_artikel(id_artikel):
    conn = connect_to_db()
    cursor = conn.cursor()
    
    query = "DELETE FROM artikel WHERE id_artikel = %s"
    
    cursor.execute(query, (id_artikel,)) #harus ditambah koma ,
    conn.commit()
    st.success("Artikel Berhasil Dihapus")
    conn.close()


def fetch_admin():
    conn = connect_to_db()
    query = "SELECT * FROM admin;"
    df = pd.read_sql(query, conn)
    conn.close()
    return df


def fetch_pasien():
    conn = connect_to_db()
    query = "SELECT * FROM pasien;"
    df = pd.read_sql(query, conn)
    conn.close()
    
    return df


def update_pengguna(username, password, nama_pasien, jenis_kelamin, alamat, email, pekerjaan, tanggal_lahir, username_lama):
    conn = connect_to_db()
    cursor = conn.cursor()
    query = "UPDATE pasien SET username = %s, password = %s, nama_pasien = %s, jenis_kelamin = %s, alamat = %s, email = %s, pekerjaan = %s, tanggal_lahir = %s WHERE username = %s"
    cursor.execute(query, (username, password, nama_pasien, jenis_kelamin, alamat, email, pekerjaan, tanggal_lahir, username_lama))
    conn.commit()
    conn.close()
    
def hapus_data_pasien(id_pasien):
    conn = connect_to_db()
    cursor = conn.cursor()
    query = "DELETE FROM pasien WHERE id_pasien = %s"
    cursor.execute(query, (id_pasien,))
    conn.commit()
    conn.close()
    
def forward_chaining(gejala_gejala):
    conn = connect_to_db()
    cursor = conn.cursor()
    query = "SELECT id_komplikasi_penyakit FROM relasi_penyakit_gejala WHERE id_gejala = %s"
    penyakit_yang_mungkin = set()
    for gejala in gejala_gejala:
        cursor.execute(query, (gejala,))
        penyakit_penyakit = cursor.fetchall()
        for penyakit in penyakit_penyakit:
            penyakit_yang_mungkin.add(penyakit[0])
    return penyakit_yang_mungkin
        
        

def menambah_id_pasien_default():
    
    conn = connect_to_db()
    cursor = conn.cursor()
    
    # Ambil ID terakhir dari database (misalnya A0001, A0002, dst)
    cursor.execute("SELECT id_pasien FROM pasien ORDER BY id_pasien DESC LIMIT 1")
    last_id = cursor.fetchone()
    
    if last_id:
        # Ambil nomor dari ID terakhir dan increment 1
        last_number = int(last_id[0][2:])  # Mengambil angka setelah 'A'
        new_id = f"PS{last_number + 1:03d}"  # Formatkan ID seperti A0001, A0002, dst
    else:
        # Jika tidak ada data sebelumnya, mulai dengan A0001
        new_id = "PS001"
    
    conn.close()
    return new_id

def menambah_id_komplikasi_penyakit_default():
    
    conn = connect_to_db()
    cursor = conn.cursor()
    
    # Ambil ID terakhir dari database (misalnya A0001, A0002, dst)
    cursor.execute("SELECT id_komplikasi_penyakit FROM komplikasi_penyakit ORDER BY id_komplikasi_penyakit DESC LIMIT 1")
    last_id = cursor.fetchone()
    
    if last_id:
        # Ambil nomor dari ID terakhir dan increment 1
        last_number = int(last_id[0][1:])  # Mengambil angka setelah 'A'
        new_id = f"P{last_number + 1:04d}"  # Formatkan ID seperti PS001, PS002, dst
    else:
        # Jika tidak ada data sebelumnya, mulai dengan A0001
        new_id = "P0001"
    
    conn.close()
    return new_id

def menambah_id_gejala_default():
    
    conn = connect_to_db()
    cursor = conn.cursor()
    

    cursor.execute("SELECT id_gejala FROM gejala ORDER BY id_gejala DESC LIMIT 1")
    last_id = cursor.fetchone()
    
    if last_id:
        # Ambil nomor dari ID terakhir dan increment 1
        last_number = int(last_id[0][1:])  # Mengambil angka setelah 'G'
        new_id = f"G{last_number + 1:04d}"  # Formatkan ID seperti G01, G02, dst
    else:
        # Jika tidak ada data sebelumnya, mulai dengan A0001
        new_id = "G0001"
    
    conn.close()
    return new_id

def menambah_id_pemeriksaan_kesehatan_default():
    conn = connect_to_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id_pemeriksaan FROM pemeriksaan_kesehatan ORDER BY id_pemeriksaan DESC LIMIT 1")
    last_id = cursor.fetchone()
    
    if last_id:
        last_number = int(last_id[0][1:])
        new_id = f"K{last_number + 1:04}"
    else:
        new_id = "K0001"
    
    conn.close()
    return new_id
    

    

def add_pasien(id_pasien, username, password, nama_pasien, jenis_kelamin, alamat, email, pekerjaan, tanggal_lahir):
    conn = connect_to_db()
    cursor = conn.cursor()
    
    query = "INSERT INTO pasien (id_pasien, username, password, nama_pasien, jenis_kelamin, alamat, email, pekerjaan, tanggal_lahir) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);"
    cursor.execute(query, (id_pasien, username, password, nama_pasien, jenis_kelamin, alamat, email, pekerjaan, tanggal_lahir))
    conn.commit()
    
    st.success("Pasien Berhasil Didaftarkan")
    conn.close()
    
    
def get_id_pasien(username):
    try:
        connection = connect_to_db()
        cursor = connection.cursor()

        # SQL query to check user credentials
        query = "SELECT id_pasien FROM pasien WHERE username = %s"
        cursor.execute(query, (username,))

        # Fetch one result
        name = cursor.fetchone()

        return name[0] if name else None
       

    except mysql.connector.Error as err:
        st.error(f"Database error: {err}")  # Show the error
        return False  # Indicate failure

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
    
    
    
def get_id_penyakit(nama_penyakit):
    conn = connect_to_db()
    cursor = conn.cursor()
    query = "SELECT id_komplikasi_penyakit FROM komplikasi_penyakit WHERE nama_penyakit = %s"
    cursor.execute(query, (nama_penyakit,))
    id_penyakit = cursor.fetchone()
    conn.close()
    return id_penyakit[0] if id_penyakit else None
    
    
def get_jenis_kelamin(username):
    conn = connect_to_db()
    cursor = conn.cursor()
    query = "SELECT jenis_kelamin FROM pasien WHERE username = %s"
    cursor.execute(query, (username,))
    jenis_kelamin = cursor.fetchone()
    conn.close()
    return jenis_kelamin[0] if jenis_kelamin else None
    
def add_pemeriksaan_kesehatan(id_pemeriksaan, id_pasien, risiko_diabetes, tanggal_pemeriksaan):
    conn = connect_to_db()
    cursor = conn.cursor()
    query = "INSERT INTO pemeriksaan_kesehatan (id_pemeriksaan, id_pasien, risiko_diabetes, tanggal_pemeriksaan) VALUES (%s, %s, %s, %s);"
    cursor.execute(query, (id_pemeriksaan, id_pasien, risiko_diabetes, tanggal_pemeriksaan))
    conn.commit()
    conn.close()
    
    
def add_pemeriksaan_faktor_permanen(id_pemeriksaan, usia_di_atas_40_tahun, riwayat_keluarga_diabetes, riwayat_diabetes_gestasional, riwayat_penyakit_berat_badan_rendah):
    conn = connect_to_db()
    cursor = conn.cursor()
    query = "INSERT INTO pemeriksaan_faktor_permanen (id_pemeriksaan, usia_di_atas_40_tahun, riwayat_keluarga_diabetes, riwayat_diabetes_gestasional, riwayat_lahir_berat_badan_lahir_rendah) VALUES (%s, %s, %s, %s, %s);"
    cursor.execute(query, (id_pemeriksaan, usia_di_atas_40_tahun, riwayat_keluarga_diabetes, riwayat_diabetes_gestasional, riwayat_penyakit_berat_badan_rendah))
    conn.commit()
    conn.close()
    
    
def add_kebiasaan_hidup(id_pemeriksaan, konsumsi_alkohol, kurang_aktivitas, merokok, pola_makan_buruk, kurang_tidur):
    conn = connect_to_db()
    cursor = conn.cursor()
    query = "INSERT INTO kebiasaan_hidup(id_pemeriksaan, konsumsi_alkohol, kurang_aktivitas, merokok, pola_makan_buruk, kurang_tidur) VALUES (%s, %s, %s, %s, %s, %s);"
    cursor.execute(query, (id_pemeriksaan, konsumsi_alkohol, kurang_aktivitas, merokok, pola_makan_buruk, kurang_tidur))
    conn.commit()
    conn.close()
    
    
def add_pemeriksaan_fisik(id_pemeriksaan, berat_badan, tinggi_badan, lingkar_perut, indeks_massa_tubuh):
    conn = connect_to_db()
    cursor = conn.cursor()
    query = "INSERT INTO pemeriksaan_fisik(id_pemeriksaan, berat_badan, tinggi_badan, lingkar_perut, indeks_massa_tubuh) VALUES (%s, %s, %s, %s, %s);"
    cursor.execute(query, (id_pemeriksaan, berat_badan, tinggi_badan, lingkar_perut, indeks_massa_tubuh))
    conn.commit()
    conn.close()

def add_pemeriksaan_laboratorium(id_pemeriksaan, gula_darah_sewaktu, gula_darah_puasa, gula_darah_2_jam_setelah_makan, tekanan_darah, HDL, LDL, trigliserida, total_kolestrol):
    conn = connect_to_db()
    cursor = conn.cursor()
    query = "INSERT INTO pemeriksaan_laboratorium(id_pemeriksaan, gula_darah_sewaktu, gula_darah_puasa, gula_darah_2_jam_setelah_makan, tekanan_darah, HDL, LDL, trigliserida, total_kolestrol) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);"
    cursor.execute(query, (id_pemeriksaan, gula_darah_sewaktu, gula_darah_puasa, gula_darah_2_jam_setelah_makan, tekanan_darah, HDL, LDL, trigliserida, total_kolestrol))
    conn.commit()
    conn.close()


def menambah_id_diagnosis_default():
    
    conn = connect_to_db()
    cursor = conn.cursor()
    

    cursor.execute("SELECT id_diagnosis FROM diagnosis_penyakit ORDER BY id_diagnosis DESC LIMIT 1")
    last_id = cursor.fetchone()
    
    if last_id:
        # Ambil nomor dari ID terakhir dan increment 1
        last_number = int(last_id[0][1:])  # Mengambil angka setelah 'D'
        new_id = f"D{last_number + 1:04d}" 
    else:
        # Jika tidak ada data sebelumnya, mulai dengan D0001
        new_id = "D0001"
    
    conn.close()
    return new_id

def fetch_diagnosis_penyakit():
    conn = connect_to_db()
    query = """
    SELECT diagnosis_penyakit.id_diagnosis, diagnosis_penyakit.id_pasien, pasien.nama_pasien, diagnosis_penyakit.gejala_terpilih, diagnosis_penyakit.gejala_cocok, diagnosis_penyakit.persentase_kecocokan, diagnosis_penyakit.tanggal_diagnosis  
    FROM diagnosis_penyakit
    JOIN pasien ON diagnosis_penyakit.id_pasien = pasien.id_pasien;
    """
    df = pd.read_sql(query, conn)
    return df

def insert_diagnosis_penyakit(id_diagnosis, id_pasien, id_komplikasi_penyakit, gejala_terpilih, gejala_cocok, persentase_kecocokan, tanggal_diagnosis):
    conn = connect_to_db()
    cursor = conn.cursor()
    query = "INSERT INTO diagnosis_penyakit(id_diagnosis, id_pasien, id_komplikasi_penyakit, gejala_terpilih, gejala_cocok, persentase_kecocokan, tanggal_diagnosis) VALUES (%s, %s, %s, %s, %s, %s, %s);"
    cursor.execute(query, (id_diagnosis, id_pasien, id_komplikasi_penyakit, gejala_terpilih, gejala_cocok, persentase_kecocokan, tanggal_diagnosis))
    conn.commit()
    conn.close()
    
def get_last_id_pasien():
    conn = connect_to_db()
    cursor = conn.cursor()
    query = "SELECT id_pasien FROM pasien ORDER BY id_pasien DESC LIMIT 1"
    cursor.execute(query)
    
    result = cursor.fetchone()
    conn.commit()
    
    conn.close()
    
    return result[0]

def get_penjelasan_penyakit(nama_penyakit):
    conn = connect_to_db()
    cursor = conn.cursor()
    query = "SELECT penjelasan FROM komplikasi_penyakit WHERE nama_penyakit = %s"
    cursor.execute(query, (nama_penyakit,))
    result = cursor.fetchone()
    conn.close()
    return result[0]
    

def validasi_password(password):
        return len(password) >= 7

def validasi_email_regex(email):
    regex = r'^[a-zA-Z0-9_.+-]+@gmail\.com$'
    return re.match(regex, email) is not None

def check_data_registrasi_pasien(username_pengguna, email, password_pengguna, nama, alamat):
    
    validation_errors = []
                
    if cek_username(username_pengguna) == True:
        validation_errors.append("Username sudah terdaftar")

        
    if cek_email(email) == True:
        validation_errors.append("Email Sudah Terdaftar")
    # Check if username is provided
    if not username_pengguna:
        validation_errors.append("Username tidak boleh kosong.")

    # Check if password is provided and meets the length requirement
    if not password_pengguna or not validasi_password(password_pengguna):
        validation_errors.append("Password harus lebih dari 6 karakter.")

    # Check if full name is provided
    if not nama:
        validation_errors.append("Nama lengkap tidak boleh kosong.")

    # Check if email is provided and valid
    if not email or not validasi_email_regex(email):
        validation_errors.append("Email tidak valid. Pastikan menggunakan format yang benar (@gmail.com).")

    # Check if address is provided
    if not alamat:
        validation_errors.append("Alamat tidak boleh kosong.")

    # Display validation errors
    if validation_errors:
        for error in validation_errors:
            st.error(error)
        return False
    else:
        return True

def check_update_data_pasien(username_pengguna, email, password_pengguna, nama, alamat):
    validation_errors = []
                
    if cek_username(username_pengguna) == True and username_pengguna != username_pengguna:
        validation_errors.append("Username sudah terdaftar")

        
    if cek_email(email) == True and email != email:
        validation_errors.append("Email Sudah Terdaftar")
    # Check if username is provided
    if not username_pengguna:
        validation_errors.append("Username tidak boleh kosong.")

    # Check if password is provided and meets the length requirement
    if not password_pengguna or not validasi_password(password_pengguna):
        validation_errors.append("Password harus lebih dari 6 karakter.")

    # Check if full name is provided
    if not nama:
        validation_errors.append("Nama lengkap tidak boleh kosong.")

    # Check if email is provided and valid
    if not email or not validasi_email_regex(email):
        validation_errors.append("Email tidak valid. Pastikan menggunakan format yang benar (@gmail.com).")

    # Check if address is provided
    if not alamat:
        validation_errors.append("Alamat tidak boleh kosong.")

    # Display validation errors
    if validation_errors:
        for error in validation_errors:
            st.error(error)
        return False
    else:
        return True


def check_admin(username, password):
    
    try:
        connection = connect_to_db()
        cursor = connection.cursor()

        # SQL query to check user credentials
        query = "SELECT * FROM admin WHERE username_admin = %s AND password = %s"
        cursor.execute(query, (username, password))

        # Fetch one result
        result = cursor.fetchone()
        if result:
            if result[0] == username and result[2] == password:
                return True # User is found
        else:
            return False  # User not found

    except mysql.connector.Error as err:
        st.error(f"Database error: {err}")  # Show the error
        return False  # Indicate failure

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
            

def check_pengguna(username, password):
    try:
        connection = connect_to_db()
        cursor = connection.cursor()

        # SQL query to check user credential
        query = "SELECT * FROM pasien WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))

        # Fetch one result
        result = cursor.fetchone()
        if result:
            if result[1] == username and result[2] == password:
                return True # User is found
        else:
            return False  # User not found

    except mysql.connector.Error as err:
        st.error(f"Database error: {err}")  # Show the error
        return False  # Indicate failure

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
            
def cek_username(username):
    try:
        connection = connect_to_db()
        cursor = connection.cursor()

        # SQL query to check user credential
        query = "SELECT * FROM pasien WHERE username = %s"
        cursor.execute(query, (username,))

        # Fetch one result
        result = cursor.fetchone()

        if result:
            
            return True # User is found
        else:
            return False  # User not found

    except mysql.connector.Error as err:
        st.error(f"Database error: {err}")  # Show the error
        return False  # Indicate failure

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def cek_email(email):
    try:
        connection = connect_to_db()
        cursor = connection.cursor()

        # SQL query to check user credential
        query = "SELECT * FROM pasien WHERE email = %s"
        cursor.execute(query, (email,))

        # Fetch one result
        result = cursor.fetchone()

        if result[6] == email:
            
            return True # Email sudah ada
        else:
            return False  # Email belum ada

    except mysql.connector.Error as err:
        st.error(f"Database error: {err}")  # Show the error
        return False  # Indicate failure

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


        
    
# Function to insert data into the database
def insert_admin(username, name, password):
    try:
        connection = connect_to_db()
        cursor = connection.cursor()

    
        # SQL query to insert data
        query = "INSERT INTO admin (username_admin, nama_admin, password) VALUES (%s, %s, %s)"
        cursor.execute(query, (username, name, password))

        # Commit the transaction
        connection.commit()
        
        
        st.success("Admin Berhasil Ditambahkan!")
        return True



    except mysql.connector.Error as err:
        err = "Username yang anda masukkan salah atau sudah terdaftar! Gunakan yang lain"
        st.error(f"Database error: {err}")

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
            
    

def hapus_admin(username_admin):
    conn = connect_to_db()
    cursor = conn.cursor()
    
    query = "DELETE FROM admin WHERE username_admin = %s"
    
    cursor.execute(query, (username_admin,)) #harus ditambah koma ,
    conn.commit()
    st.success("Admin Berhasil Dihapus")
    conn.close()


def fetch_pemeriksaan_kesehatan():
    conn = connect_to_db()
    query = """
    SELECT pemeriksaan_kesehatan.id_pemeriksaan, pemeriksaan_kesehatan.id_pasien, pasien.nama_pasien, pemeriksaan_kesehatan.risiko_diabetes, pemeriksaan_kesehatan.tanggal_pemeriksaan, pemeriksaan_faktor_permanen.usia_di_atas_40_tahun, pemeriksaan_faktor_permanen.riwayat_keluarga_diabetes, pemeriksaan_faktor_permanen.riwayat_diabetes_gestasional, pemeriksaan_faktor_permanen.riwayat_lahir_berat_badan_lahir_rendah, pemeriksaan_fisik.berat_badan, pemeriksaan_fisik.tinggi_badan, pemeriksaan_fisik.lingkar_perut, pemeriksaan_fisik.indeks_massa_tubuh, pemeriksaan_laboratorium.gula_darah_sewaktu, pemeriksaan_laboratorium.gula_darah_puasa, pemeriksaan_laboratorium.gula_darah_2_jam_setelah_makan, pemeriksaan_laboratorium.tekanan_darah, pemeriksaan_laboratorium.HDL, pemeriksaan_laboratorium.LDL, pemeriksaan_laboratorium.trigliserida, pemeriksaan_laboratorium.total_kolestrol
    FROM pemeriksaan_kesehatan
    JOIN pemeriksaan_faktor_permanen ON pemeriksaan_kesehatan.id_pemeriksaan = pemeriksaan_faktor_permanen.id_pemeriksaan
    JOIN pasien ON pemeriksaan_kesehatan.id_pasien = pasien.id_pasien
    JOIN pemeriksaan_fisik ON pemeriksaan_kesehatan.id_pemeriksaan = pemeriksaan_fisik.id_pemeriksaan
    JOIN pemeriksaan_laboratorium ON pemeriksaan_laboratorium.id_pemeriksaan = pemeriksaan_kesehatan.id_pemeriksaan;
    
    """
    df = pd.read_sql(query, conn)
    return df

def fetch_pemeriksaan_fisik():
    conn = connect_to_db()
    query = "SELECT * FROM pemeriksaan_fisik"
    df = pd.read_sql(query, conn)
    return df

def fetch_pemeriksaan_faktor_permanen():
    conn = connect_to_db()
    query = "SELECT * FROM pemeriksaan_faktor_permanen"
    df = pd.read_sql(query, conn)
    return df


def fetch_pemeriksaan_laboratorium():

    conn = connect_to_db()
    query = "SELECT * FROM pemeriksaan_laboratorium;"
    df = pd.read_sql(query, conn)
    return df

def fetch_kebiasaan_hidup():
    conn = connect_to_db()
    query = "SELECT * FROM kebiasaan_hidup"
    df = pd.read_sql(query, conn)
    return df




def fetch_hasil_pemeriksaan():
    conn = connect_to_db()
    query = """
    SELECT pemeriksaan_kesehatan.id_pemeriksaan, pemeriksaan_kesehatan.id_pasien, pasien.nama_pasien, pemeriksaan_kesehatan.tanggal_pemeriksaan, riwayat_penyakit.hipertensi, riwayat_penyakit.penyakit_jantung, riwayat_penyakit.stroke, riwayat_penyakit.dislipidemia, riwayat_penyakit.penyakit_ginjal, riwayat_penyakit.obesitas, kebiasaan_hidup.konsumsi_alkohol, kebiasaan_hidup.kurang_aktivitas, kebiasaan_hidup.merokok, kebiasaan_hidup.kurang_buah_dan_sayur, kebiasaan_hidup.gula_berlebihan, pemeriksaan_fisik.berat_badan, pemeriksaan_fisik.tinggi_badan, pemeriksaan_fisik.lingkar_perut, hasil_laboratorium.gula_darah_sewaktu, hasil_laboratorium.gula_darah_puasa, hasil_laboratorium.gula_darah_2_jam_setelah_makan, hasil_laboratorium.tekanan_darah, hasil_laboratorium.HDL, hasil_laboratorium.LDL, hasil_laboratorium.trigliserida
    FROM pemeriksaan_kesehatan
    JOIN pasien ON pemeriksaan_kesehatan.id_pasien = pasien.id_pasien
    JOIN riwayat_penyakit ON pemeriksaan_kesehatan.id_pemeriksaan = riwayat_penyakit.id_pemeriksaan
    JOIN kebiasaan_hidup ON pemeriksaan_kesehatan.id_pemeriksaan = kebiasaan_hidup.id_pemeriksaan
    JOIN pemeriksaan_fisik ON pemeriksaan_kesehatan.id_pemeriksaan = pemeriksaan_kesehatan.id_pemeriksaan
    JOIN hasil_laboratorium ON pemeriksaan_kesehatan.id_pemeriksaan = hasil_laboratorium.id_pemeriksaan
    WHERE pemeriksaan_kesehatan.id_pasien = "PS001";
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df


def get_diagnosis_penyakit(username):
    conn = connect_to_db()
    cursor = conn.cursor()
    query = "SELECT * FROM pasien WHERE username = %s"
    cursor.execute(query, (username,))
    result = cursor.fetchone()
    conn.close()
    return result if result else None









def laporan_kesehatan_pdf(id_pasien):
    conn = connect_to_db()
    query = "SELECT pemeriksaan_kesehatan.id_pemeriksaan, pemeriksaan_kesehatan.id_pasien, pasien.nama_pasien, pemeriksaan_kesehatan.tanggal_pemeriksaan, pemeriksaan_kesehatan.riwayat_keluarga_diabetes, pemeriksaan_kesehatan.berat_badan, pemeriksaan_kesehatan.tinggi_badan, pemeriksaan_kesehatan.konsumsi_alkohol, pemeriksaan_kesehatan.kurang_aktivitas, pemeriksaan_kesehatan.lingkar_perut, pemeriksaan_kesehatan.merokok, pemeriksaan_kesehatan.kurang_buah_dan_sayur, pemeriksaan_kesehatan.gula_berlebihan, pemeriksaan_kesehatan.gula_darah_sewaktu, pemeriksaan_kesehatan.gula_darah_puasa, pemeriksaan_kesehatan.gula_darah_2_setelah_makan, pemeriksaan_kesehatan.tekanan_darah, pemeriksaan_kesehatan.HDL, pemeriksaan_kesehatan.LDL, pemeriksaan_kesehatan.trigliserida, analisa_hasil.`gejala-gejala`, penyakit.nama_penyakit FROM pemeriksaan_kesehatan JOIN pasien ON pemeriksaan_kesehatan.id_pasien = pasien.id_pasien JOIN analisa_hasil ON pemeriksaan_kesehatan.id_pasien = analisa_hasil.id_pasien JOIN penyakit ON analisa_hasil.id_penyakit = penyakit.id_penyakit WHERE pemeriksaan_kesehatan.id_pasien = %s;"
    
    query = """
    SELECT pemeriksaan_kesehatan.id_pemeriksaan, pemeriksaan_kesehatan.id_pasien, pasien.nama_pasien, pemeriksaan_kesehatan.tanggal_pemeriksaan, riwayat_penyakit.hipertensi, riwayat_penyakit.penyakit_jantung, riwayat_penyakit.stroke, riwayat_penyakit.dislipidemia, riwayat_penyakit.penyakit_ginjal, riwayat_penyakit.obesitas, kebiasaan_hidup.konsumsi_alkohol, kebiasaan_hidup.kurang_aktivitas, kebiasaan_hidup.merokok, kebiasaan_hidup.kurang_buah_dan_sayur, kebiasaan_hidup.gula_berlebihan, pemeriksaan_fisik.berat_badan, pemeriksaan_fisik.tinggi_badan, pemeriksaan_fisik.lingkar_perut, hasil_laboratorium.gula_darah_sewaktu, hasil_laboratorium.gula_darah_puasa, hasil_laboratorium.gula_darah_2_jam_setelah_makan, hasil_laboratorium.tekanan_darah, hasil_laboratorium.HDL, hasil_laboratorium.LDL, hasil_laboratorium.trigliserida
    FROM pemeriksaan_kesehatan
    JOIN pasien ON pemeriksaan_kesehatan.id_pasien = pasien.id_pasien
    JOIN riwayat_penyakit ON pemeriksaan_kesehatan.id_pemeriksaan = riwayat_penyakit.id_pemeriksaan
    JOIN kebiasaan_hidup ON pemeriksaan_kesehatan.id_pemeriksaan = kebiasaan_hidup.id_pemeriksaan
    JOIN pemeriksaan_fisik ON pemeriksaan_kesehatan.id_pemeriksaan = pemeriksaan_kesehatan.id_pemeriksaan
    JOIN hasil_laboratorium ON pemeriksaan_kesehatan.id_pemeriksaan = hasil_laboratorium.id_pemeriksaan
    WHERE pemeriksaan_kesehatan.id_pasien = %s;
    """
    df = pd.read_sql(query, conn, params=(id_pasien,))
    return df
    
    
    return df
    pdf = FPDF()
    pdf.add_page()
    
    
    pdf.image("assets/logo_diabetes.png", x=10, y=8, w=30)  # Adjust x, y, and w for logo position and size
    pdf.image("assets/puskesmas_pkc_taman_sari.jpeg", x=170, y=8, w=30)
    
    # Menambahkan judul
    pdf.set_font("Arial", size=14, style="B")
    pdf.cell(200, 15, txt="HASIL AKHIR", ln=True, align='C')
    
    # Data Pasien
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="", ln=True)
   
    pdf.cell(200, 10, txt="Data Pasien", ln=True)
    pdf.cell(200, 10, txt=f"Nama: {st.session_state.nama}", ln=True)
    pdf.cell(200, 10, txt=f"Umur: {st.session_state.umur}", ln=True)
    pdf.cell(200, 10, txt=f"Pekerjaan: {st.session_state.pekerjaan}", ln=True)
    pdf.cell(200, 10, txt=f"Berat Badan: {st.session_state.berat_badan}", ln=True)
    pdf.cell(200, 10, txt=f"Tinggi Badan: {st.session_state.tinggi_badan}", ln=True)
    pdf.cell(200, 10, txt=f"Tanggal: {st.session_state.tanggal}", ln=True)
    pdf.cell(200, 10, txt=f"Alamat: {st.session_state.alamat}", ln=True)
    pdf.cell(200, 10, txt=f"Jenis Kelamin: {st.session_state.jenis_kelamin}", ln=True)
    pdf.cell(200, 10, txt=f"Riwayat Keluarga Diabetes: {st.session_state.riwayat_keluarga_diabetes}", ln=True)
    
    # Pola Hidup
    pdf.cell(200, 10, txt="Pola Hidup", ln=True)
    pdf.cell(200, 10, txt=f"Konsumsi Alkohol: {st.session_state.konsumsi_alkohol}", ln=True)
    pdf.cell(200, 10, txt=f"Kurang Aktivitas: {st.session_state.kurang_aktivitas}", ln=True)
    pdf.cell(200, 10, txt=f"Lingkar Perut: {st.session_state.lingkar_perut}", ln=True)
    pdf.cell(200, 10, txt=f"Merokok: {st.session_state.merokok}", ln=True)
    pdf.cell(200, 10, txt=f"Kurang Buah dan Sayur: {st.session_state.kurang_buah_sayur}", ln=True)
    pdf.cell(200, 10, txt=f"Gula Berlebihan: {st.session_state.gula_berlebihan}", ln=True)
    
    # Medical Check Up
    pdf.cell(200, 10, txt="Medical Check Up", ln=True)
    pdf.cell(200, 10, txt=f"Gula Darah Sewaktu (GDS): {st.session_state.gula_darah_sewaktu}", ln=True)
    pdf.cell(200, 10, txt=f"Gula Darah Puasa (GDP): {st.session_state.gula_darah_puasa}", ln=True)
    pdf.cell(200, 10, txt=f"Gula Darah 2 Jam Setelah Makan (GD2PP): {st.session_state.gula_darah_2_jam_setelah_makan}", ln=True)
    pdf.cell(200, 10, txt=f"Tekanan Darah: {st.session_state.tekanan_darah}", ln=True)
    
    # Gejala-Gejala cari cara
    pdf.cell(200, 10, txt="Gejala-Gejala", ln=True)
    #for i in gejala_terpilih:
        #pdf.cell(200, 10, txt=f"{i}: {nama_gejala(i)}", ln=True)
    
    # Menyimpan PDF
    pdf_output = io.BytesIO()
    pdf_output.write(pdf.output(dest='S').encode('latin1 '))
    pdf_output.seek(0)  # Move to the beginning of the BytesIO buffer
    
    #return pdf_output





'''
# Streamlit interface
st.title("Memasukkan Data ke dalam Basis Data")

# User input fields
username = st.text_input("Username")
name = st.text_input("Name")
password = st.text_input("Password", type="password")

# Insert button
if st.button("Insert User"):
    if username and name and password:
        insert_user(username, name, password)
    else:
        st.warning("Please fill in all fields.")


'''

