import streamlit as st
from utils.footer import render_footer

st.set_page_config(
    page_title="About",
    page_icon="ℹ️"
)

st.title("ℹ️ About")

st.markdown(
    """
    <style>
    .breadcrumb {
        font-size: 15px;
        margin-bottom: 20px;
        color: #64748b;
    }
    .breadcrumb span {
        cursor: pointer;
        color: #0ea5e9;
        font-weight: 500;
    }
    .breadcrumb span:hover {
        text-decoration: underline;
    }
    .breadcrumb .current {
        color: #1e293b;
        font-weight: 600;
        cursor: default;
    }
    </style>
    """,
    unsafe_allow_html=True
)

breadcrumb_col1, breadcrumb_col2 = st.columns([1, 10])

with breadcrumb_col1:
    if st.button("🏠 Home"):
        st.switch_page("Home.py")

with breadcrumb_col2:
    st.markdown(
        """
        <div class="breadcrumb">
            <span>Home</span> &nbsp;→&nbsp;
            <span class="current">About</span>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("---")

# ✅ Centered Image
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    st.image("assets/ek.png", use_container_width=True)

st.markdown("---")

# =========================
# About Text
# =========================
st.markdown("""
I earned my **BSc** and **MSc** degrees in **Geomatic Engineering** from **Aksaray University**, and my **PhD** in **Geodesy and Geoinformation Engineering** from **Kocaeli University**, all from **Türkiye**. 
            
Currently, I am working as a **Lecturer** for the **Mapping and Cadastre Programme** at **Iskenderun Technical University**.

**Main research interests:**
- Urban Climate
- Remote Sensing
- Photogrammetry
- Applied Machine Learning
- Deep Learning Algorithms
""")

st.markdown("---")

# =========================
# Social & Academic Links
# =========================
st.subheader("🔗 Academic & Social Profiles")


c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    st.image(
        "https://cdn.jsdelivr.net/gh/simple-icons/simple-icons/icons/orcid.svg",
        width=40
    )
    st.link_button(
        "ORCID",
        "https://orcid.org/my-orcid?orcid=0000-0002-5553-0143",
        help="Visit ORCID profile"
    )

with c2:
    st.image(
        "https://cdn.jsdelivr.net/gh/simple-icons/simple-icons/icons/googlescholar.svg",
        width=40
    )
    st.link_button(
        "Scholar",
        "https://scholar.google.com/citations?user=Xa8Hzw8AAAAJ&hl=tr",
        help="Visit Google Scholar profile"
    )

with c3:
    st.image(
        "https://cdn.jsdelivr.net/gh/simple-icons/simple-icons/icons/linkedin.svg",
        width=40
    )
    st.link_button(
        "LinkedIn",
        "https://www.linkedin.com/in/efdalkaya/",
        help="Visit LinkedIn profile"
    )

with c4:
    st.image(
        "https://cdn.jsdelivr.net/gh/simple-icons/simple-icons/icons/youtube.svg",
        width=40
    )
    st.link_button(
        "YouTube",
        "https://www.youtube.com/@efdalkaya",
        help="Visit YouTube channel"
    )

with c5:
    st.image(
        "https://cdn.jsdelivr.net/gh/simple-icons/simple-icons/icons/github.svg",
        width=40
    )
    st.link_button(
        "GitHub",
        "https://github.com/efdalkaya",
        help="Visit GitHub profile"
    )

render_footer()