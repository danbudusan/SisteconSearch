import streamlit as st
import requests
from bs4 import BeautifulSoup
import time

# --- Web Interface Layout ---
st.title("Sistecon Search Tool")
st.write("Enter the details below to scan pages.")

start_id = st.number_input("Starting ID", value=100642)
end_id = st.number_input("Ending ID", value=101840)
target_word = st.text_input("Word to find", value="MARIA SOLANGE MONTESANO")

if st.button("Start Search"):
    found_pages = []
    base_url = "https://www.sistecon.com.ar/gastos-qr.php?liquidacion="
    
    # Progress bar for the website
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    session = requests.Session()
    total_steps = end_id - start_id + 1

    for idx, i in enumerate(range(start_id, end_id + 1)):
        url = f"{base_url}{i}"
        
        # Update progress bar
        percent = (idx + 1) / total_steps
        progress_bar.progress(percent)
        status_text.text(f"Checking ID: {i}...")

        try:
            response = session.get(url, timeout=5)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                if target_word.lower() in soup.get_text().lower():
                    st.success(f"Match found at ID {i}!")
                    st.write(url)
                    found_pages.append(url)
        except:
            pass
            
        time.sleep(0.2)
    
    st.balloons() # Visual celebration when finished!
    st.write(f"Search complete. Found {len(found_pages)} matches.")