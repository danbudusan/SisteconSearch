import streamlit as st
import requests
from bs4 import BeautifulSoup
import time

# --- Web Interface Layout ---
st.set_page_config(page_title="Sistecon Ultra-Fast Scanner", page_icon="⚡")
st.title("⚡ Sistecon High-Speed Search")
st.write("Using a 0.01s delay. Caution: High speed may lead to IP blocks.")

# Sidebar for inputs
with st.sidebar:
    st.header("Settings")
    start_id = st.number_input("Starting ID", value=100642)
    end_id = st.number_input("Ending ID", value=101840)
    target_word = st.text_input("Word to find", value="MARIA SOLANGE MONTESANO")
    # Setting the delay here
    speed_delay = 0.01 

if st.button("Launch Scan"):
    found_pages = []
    base_url = "https://www.sistecon.com.ar/gastos-qr.php?liquidacion="
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    results_area = st.container()
    
    session = requests.Session()
    # Adding a realistic header so we look less like a bot
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    })

    total_steps = end_id - start_id + 1

    try:
        for idx, i in enumerate(range(start_id, end_id + 1)):
            url = f"{base_url}{i}"
            
            # Update Progress
            percent = (idx + 1) / total_steps
            progress_bar.progress(percent)
            status_text.text(f"Currently Checking: {i}")

            try:
                response = session.get(url, timeout=3)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    # Search specifically in text
                    if target_word.lower() in soup.get_text().lower():
                        with results_area:
                            st.success(f"MATCH FOUND: ID {i}")
                            st.link_button(f"Open Page {i}", url)
                        found_pages.append(url)
                
                elif response.status_code == 403:
                    st.error(f"Access Denied (403) at ID {i}. The server blocked the connection due to speed.")
                    break

            except Exception:
                # Silently skip connection blips to keep speed up
                pass
            
            # The 0.05 second delay
            time.sleep(speed_delay)

        st.balloons()
        st.info(f"Scan Finished. Total Matches: {len(found_pages)}")

    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
