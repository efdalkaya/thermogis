import streamlit as st
from datetime import datetime

def render_footer():
    year = datetime.now().year

    st.markdown(
        f"""
        <style>
        .footer {{
            position: relative;
            bottom: 0;
            width: 100%;
            text-align: center;
            font-size: 12px;
            color: #6b7280;
            padding: 10px 0;
        }}
        </style>

        <div class="footer">
            © {year} <strong>ThermoGIS</strong> — Developed by Dr. Efdal KAYA
        </div>
        """,
        unsafe_allow_html=True
    )