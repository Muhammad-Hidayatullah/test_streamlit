import streamlit as st
import webbrowser

# Set the title of the app
st.image("assets/research.jpg", width=140)
st.title("Cari Jurnal")

# Input field for entering search query
search_query = st.text_input("Masukkan judul jurnal yang anda inginkan", value="Diabetes tipe 2")

# Button to trigger the search
st.write("")  # Empty line
st.write("")
if st.button("Cari Jurnal di Google Scholar"):
    if search_query:
        # Create the Google Scholar search URL
        search_url = f"https://scholar.google.com/scholar?q={search_query}"
        # Open the URL in a new browser tab
        webbrowser.open_new_tab(search_url)
    else:
        st.warning("Please enter a search query!")
