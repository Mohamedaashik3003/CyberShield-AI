
import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="CyberShield AI",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ CyberShield AI")
st.caption("AI-Powered Cybersecurity Threat Detection & Intelligence")

try:
    response = requests.get(API_URL, timeout=5)
    api_status = response.status_code == 200
except requests.RequestException:
    api_status = False

st.sidebar.title("System Status")

if api_status:
    st.sidebar.success("API Connected")
else:
    st.sidebar.error("API Offline")

st.sidebar.info("ML + NLP + RAG")

st.subheader("Security Event Analysis")

event = st.text_area(
    "Security Event Description",
    "Multiple failed login attempts detected from one IP address."
)

col1, col2, col3 = st.columns(3)

with col1:
    duration = st.number_input("Duration", min_value=0, value=250)
    protocol = st.selectbox("Protocol", ["TCP", "UDP", "ICMP"])

with col2:
    src_bytes = st.number_input("Source Bytes", min_value=0, value=500)
    dst_bytes = st.number_input("Destination Bytes", min_value=0, value=200)

with col3:
    failed_logins = st.number_input("Failed Logins", min_value=0, value=9)
    connection_count = st.number_input("Connection Count", min_value=0, value=15)

if st.button("Analyze Security Event", type="primary"):

    payload = {
        "event": event,
        "duration": int(duration),
        "protocol": protocol,
        "src_bytes": int(src_bytes),
        "dst_bytes": int(dst_bytes),
        "failed_logins": int(failed_logins),
        "connection_count": int(connection_count)
    }

    try:
        with st.spinner("Analyzing security event..."):
            result = requests.post(
                f"{API_URL}/analyze",
                json=payload,
                timeout=180
            )

        if result.status_code == 200:
            analysis = result.json()["analysis"]

            st.success("Analysis completed!")

            a, b, c = st.columns(3)
            a.metric("ML Detection", analysis["ml_detection"])
            b.metric("Threat Category", analysis["nlp_classification"])
            c.metric("NLP Score", f'{analysis["nlp_score"]}%')

            st.subheader("Security Intelligence")

            for i, document in enumerate(
                analysis["security_intelligence"], 1
            ):
                st.write(f"**{i}.** {document}")

            st.caption("AI predictions require analyst verification.")

        else:
            st.error(f"API Error: {result.status_code}")
            st.write(result.text)

    except requests.RequestException as error:
        st.error(f"Connection error: {error}")

st.divider()
st.caption("CyberShield AI | AI/ML Academic Project | Simulated Events")
