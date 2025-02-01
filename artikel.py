import streamlit as st

from assets import database as db

st.title("Artikel")

df_artikel = db.fetch_artikel()
# Display each article's metadata in its own box
for index, article in df_artikel.iterrows():
    with st.container():  # Create a container for each article
        # Custom HTML and CSS for the background box
        st.markdown(
            f"""
            <div style="background-color: #f0f0f5; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
                <h3>{article["judul_artikel"]}</h3>
                <img src="{article['link_gambar']}" alt="Empty" width="600" height="400">
                <p></p>
                <p><strong>Nama Website:</strong> <a href="{article['nama_website']}" target="_blank">{article['nama_website']}</a></p>
                <p><strong>Nama Penulis:</strong> {article['nama_penulis']}</p>
                <p><strong>Tahun:</strong> {article['tanggal_artikel']}</p>
                <p><a href="{article['link_artikel']}" target="_blank">Link ke Artikel</a></p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        
