import streamlit as st

st.set_page_config(page_title="Protocol Visualizer", layout="wide")

protocols = {
    "Browse URL": [
        {"dir": "Client -> Server", "proto": "DNS", "msg": "DNS Query: A record for example.com"},
        {"dir": "Server -> Client", "proto": "DNS", "msg": "DNS Response: example.com -> 93.184.216.34"},
        {"dir": "Client -> Server", "proto": "HTTP", "msg": "GET / HTTP/1.1\nHost: example.com\nUser-Agent: Mozilla/5.0\nAccept: text/html\nConnection: close"},
        {"dir": "Server -> Client", "proto": "HTTP", "msg": "HTTP/1.1 200 OK\nContent-Type: text/html\nContent-Length: 1256\n\n<html><body>Hello World</body></html>"},
    ],
    "Send Mail": [
        {"dir": "Client -> Server", "proto": "SMTP", "msg": "EHLO client.example.com"},
        {"dir": "Server -> Client", "proto": "SMTP", "msg": "250 mail.example.com Hello client.example.com"},
        {"dir": "Client -> Server", "proto": "SMTP", "msg": "MAIL FROM: <alice@example.com>"},
        {"dir": "Server -> Client", "proto": "SMTP", "msg": "250 OK"},
        {"dir": "Client -> Server", "proto": "SMTP", "msg": "RCPT TO: <bob@other.com>"},
        {"dir": "Server -> Client", "proto": "SMTP", "msg": "250 OK"},
        {"dir": "Client -> Server", "proto": "SMTP", "msg": "DATA"},
        {"dir": "Server -> Client", "proto": "SMTP", "msg": "354 End data with <CR><LF>.<CR><LF>"},
        {"dir": "Client -> Server", "proto": "SMTP", "msg": "Subject: Hello\n\nHi Bob, this is a test.\n."},
        {"dir": "Server -> Client", "proto": "SMTP", "msg": "250 OK: queued as ABC123"},
        {"dir": "Client -> Server", "proto": "SMTP", "msg": "QUIT"},
        {"dir": "Server -> Client", "proto": "SMTP", "msg": "221 Bye"},
    ],
    "Stream Video": [
        {"dir": "Client -> Server", "proto": "DNS", "msg": "DNS Query: A record for cdn.example.com"},
        {"dir": "Server -> Client", "proto": "DNS", "msg": "DNS Response: cdn.example.com -> 151.101.1.140"},
        {"dir": "Client -> Server", "proto": "HTTP", "msg": "GET /video/playlist.m3u8 HTTP/1.1\nHost: cdn.example.com\nAccept: application/vnd.apple.mpegurl"},
        {"dir": "Server -> Client", "proto": "HTTP", "msg": "HTTP/1.1 200 OK\nContent-Type: application/vnd.apple.mpegurl\n\n#EXTM3U\n#EXT-X-TARGETDURATION:10\n#EXTINF:10.0,\nsegment-0.ts\n#EXTINF:10.0,\nsegment-1.ts"},
        {"dir": "Client -> Server", "proto": "HTTP", "msg": "GET /video/segment-0.ts HTTP/1.1\nHost: cdn.example.com"},
        {"dir": "Server -> Client", "proto": "HTTP", "msg": "HTTP/1.1 200 OK\nContent-Type: video/mp2t\nContent-Length: 512000"},
        {"dir": "Client -> Server", "proto": "HTTP", "msg": "GET /video/segment-1.ts HTTP/1.1\nHost: cdn.example.com"},
        {"dir": "Server -> Client", "proto": "HTTP", "msg": "HTTP/1.1 200 OK\nContent-Type: video/mp2t\nContent-Length: 498000"},
    ],
}

if "current_mode" not in st.session_state:
    st.session_state.current_mode = None
if "step" not in st.session_state:
    st.session_state.step = 0
if "playing" not in st.session_state:
    st.session_state.playing = False

st.sidebar.title("Application Layer Visualizer")
st.sidebar.markdown("---")

mode = st.sidebar.radio("Choose Activity:", ["Browse URL", "Send Mail", "Stream Video"])

if mode == "Browse URL":
    url = st.sidebar.text_input("Enter URL:", value="http://example.com")
    if st.sidebar.button("Visit"):
        st.session_state.current_mode = "Browse URL"
        st.session_state.step = 0
        st.session_state.playing = True
        st.rerun()

elif mode == "Send Mail":
    st.sidebar.markdown("**Compose Email**")
    to = st.sidebar.text_input("To:", value="bob@other.com")
    subj = st.sidebar.text_input("Subject:", value="Hello")
    body = st.sidebar.text_area("Body:", value="Hi Bob, this is a test.")
    if st.sidebar.button("Send"):
        st.session_state.current_mode = "Send Mail"
        st.session_state.step = 0
        st.session_state.playing = True
        st.rerun()

elif mode == "Stream Video":
    quality = st.sidebar.selectbox("Quality:", ["720p", "1080p", "4K"])
    if st.sidebar.button("Play"):
        st.session_state.current_mode = "Stream Video"
        st.session_state.step = 0
        st.session_state.playing = True
        st.rerun()

st.sidebar.markdown("---")
st.sidebar.caption("CS501 - Application Layer Protocols")

st.title("Live Protocol Visualizer")

if st.session_state.current_mode is None:
    st.info("Select an activity on the left and click the action button to start.")
else:
    msgs = protocols[st.session_state.current_mode]
    total = len(msgs)
    st.progress(st.session_state.step / total, text="Step " + str(st.session_state.step) + "/" + str(total))

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("Replay"):
            st.session_state.step = 0
            st.session_state.playing = True
            st.rerun()
    with col2:
        if st.button("Pause" if st.session_state.playing else "Resume"):
            st.session_state.playing = not st.session_state.playing
            st.rerun()
    with col3:
        if st.button("Next", disabled=st.session_state.step >= total):
            st.session_state.step += 1
            st.session_state.playing = False
            st.rerun()
    with col4:
        if st.button("Prev", disabled=st.session_state.step <= 0):
            st.session_state.step -= 1
            st.session_state.playing = False
            st.rerun()

    st.markdown("---")
    for i in range(min(st.session_state.step, total)):
        m = msgs[i]
        if m["dir"].startswith("Client"):
            st.markdown("**[C->S]** `" + m["proto"] + "`")
        else:
            st.markdown("**[S->C]** `" + m["proto"] + "`")
        st.code(m["msg"])

    if st.session_state.playing and st.session_state.step < total:
        import time
        time.sleep(1.5)
        st.session_state.step += 1
        st.rerun()
    elif st.session_state.playing and st.session_state.step >= total:
        st.session_state.playing = False
        st.success("Sequence complete!")   