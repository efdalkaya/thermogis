import streamlit as st
import streamlit.components.v1 as components


APP_NAME = "ThermoGIS"
APP_VERSION = "v1.0"

st.set_page_config(
    page_title="Thermal Comfort App 1.0",
    page_icon="🌡️",
    layout="wide"
)

# ---- Sidebar Logo ----
st.sidebar.image(
    "assets/logo.png",
    use_container_width=True
)

st.sidebar.markdown(
    f"""
    <div id="sidebar-logo-container">
        <div style="text-align:center; font-weight:600; margin-top:6px;">
            Dr. Efdal KAYA
        </div>
        <div style="text-align:center; font-size:12px; color:#6b7280;">
            efdal.kaya@iste.edu.tr
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown(
    f"""
    <div id="sidebar-logo-container">
        <div style="text-align:center; font-size:12px; color:#6b7280;">
            Version: {APP_VERSION}
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
    /* Start Analysis Button Style */
    div.stButton > button {
        background: linear-gradient(135deg, #38bdf8, #0284c7);
        color: white;
        font-size: 18px;
        font-weight: 600;
        padding: 14px 24px;
        border-radius: 12px;
        border: none;
        transition: all 0.25s ease-in-out;
        box-shadow: 0 6px 15px rgba(0, 0, 0, 0.3);
    }

    /* Hover Effect */
    div.stButton > button:hover {
        background: linear-gradient(135deg, #0ea5e9, #0369a1);
        transform: scale(1.04);
        box-shadow: 0 10px 25px rgba(14, 165, 233, 0.6);
        cursor: pointer;
    }

    /* Active (Click) Effect */
    div.stButton > button:active {
        transform: scale(0.98);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------- HERO SECTION ----------
st.markdown(
    """
    <style>
    .hero {
        padding: 60px 40px;
        background: linear-gradient(135deg, #0f172a, #020617);
        border-radius: 20px;
        color: white;
    }
    .stat-box {
        padding: 20px;
        border-radius: 15px;
        background: rgba(255,255,255,0.05);
        text-align: center;
    }
    .stat-number {
        font-size: 32px;
        font-weight: bold;
        color: #38bdf8;
    }
    .stat-label {
        font-size: 14px;
        color: #cbd5f5;
    }
    </style>
    """,
    unsafe_allow_html=True
)

components.html(
    """
    <style>
        .hero {
            padding: 60px 40px;
            background: linear-gradient(135deg, #0f172a, #020617);
            border-radius: 20px;
            color: white;
            font-family: sans-serif;
            animation: heroFade 1.2s ease-out forwards;
            opacity: 0;
        }

        .hero h1 {
            animation: slideUp 1s ease-out forwards;
            animation-delay: 0.4s;
            opacity: 0;
        }

        .hero .subtitle {
            animation: fadeIn 1s ease-out forwards;
            animation-delay: 0.9s;
            opacity: 0;
        }

        .hero .description {
            animation: fadeIn 1s ease-out forwards;
            animation-delay: 1.3s;
            opacity: 0;
        }

        @keyframes heroFade {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        @keyframes slideUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        @keyframes fadeIn {
            from {
                opacity: 0;
            }
            to {
                opacity: 1;
            }
        }
    </style>

    <div class="hero">
        <h1>🌡️ Thermal Comfort App 1.0</h1>

        <div class="subtitle" style="font-size:16px; max-width:800px; margin-top:12px;">
            A scientific platform for evaluating thermal comfort conditions based on
            <strong>ISO 7730</strong> and <strong>ASHRAE 55</strong> standards.
        </div>

        <div class="description" style="
            font-size:16px;
            max-width:800px;
            margin-top:10px;
            line-height:1.6;
            color:#cbd5f5;
        ">
            Upload your climate data, compute advanced thermal comfort indices,
            and generate outputs ready for spatial interpolation and environmental analysis.
        </div>
    </div>
    """,
    height=320
)

st.markdown("<br>", unsafe_allow_html=True)

col_left, col_center, col_right = st.columns([3, 2, 3])

with col_center:
    if st.button(
        "🚀 Start Analysis",
        use_container_width=True
    ):
        st.switch_page("pages/1_Thermal Comfort Analysis.py")

# ---------- STATISTICS ----------
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(
        """
        <div class="stat-box">
            <div class="stat-number">5+</div>
            <div class="stat-label">Comfort Indices</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        """
        <div class="stat-box">
            <div class="stat-number">ISO</div>
            <div class="stat-label">Standards Based</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        """
        <div class="stat-box">
            <div class="stat-number">CSV / XLSX</div>
            <div class="stat-label">Data Input</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col4:
    st.markdown(
        """
        <div class="stat-box">
            <div class="stat-number">Ready</div>
            <div class="stat-label">For Interpolation</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col5:
    st.markdown(
        """
        <div class="stat-box">
            <div class="stat-number">Open</div>
            <div class="stat-label">Scientific Workflow</div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("<br>", unsafe_allow_html=True)

# ---------- FOOTER TEXT ----------
st.info(
    "👈 Use the navigation menu to start your analysis or perform spatial interpolation."
)
