
import streamlit as st
import pandas as pd
import io
import matplotlib.pyplot as plt

from utils.footer import render_footer

st.set_page_config(
    page_title="Thermal Comfort Analysis",
    page_icon="🧪",
)

st.title("🧪 Thermal Comfort Analysis")

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
            <span class="current">Thermal Comfort Analysis</span>
        </div>
        """,
        unsafe_allow_html=True
    )

# ==================================================
# SESSION STATE
# ==================================================
for key in ["result_df", "result_col", "selected_model"]:
    if key not in st.session_state:
        st.session_state[key] = None

# ==================================================
# COLOR SYSTEM (ALL INDICES)
# ==================================================
CLASS_COLORS = {
    "No Discomfort": "#16a34a",
    "Comfortable": "#16a34a",
    "No Cold Stress": "#16a34a",

    "Caution": "#eab308",
    "Slight Discomfort": "#eab308",
    "Slight Cold Stress": "#eab308",
    "Slightly Cool": "#eab308",
    "Slightly Warm": "#eab308",

    "Extreme Caution": "#f97316",
    "Moderate Discomfort": "#f97316",
    "Moderate Cold Stress": "#f97316",
    "Cool": "#f97316",
    "Warm Stress": "#f97316",

    "Danger": "#dc2626",
    "Hot Stress": "#dc2626",
    "Severe Discomfort": "#dc2626",
    "Severe Cold Stress": "#dc2626",
    "Hot": "#dc2626",

    "Extreme Danger": "#7f1d1d",
    "Very Cold": "#7f1d1d",
}

def style_class(val):
    color = CLASS_COLORS.get(val, "#ffffff")
    return f"background-color:{color}; color:black; font-weight:600;"

# ==================================================
# CALCULATION FUNCTIONS
# ==================================================
def heat_index_noaa(ta, rh):
    t = ta * 9 / 5 + 32
    hi = (
        -42.379 + 2.04901523 * t + 10.14333127 * rh
        - 0.22475541 * t * rh
        - 6.83783e-3 * t**2
        - 5.481717e-2 * rh**2
        + 1.22874e-3 * t**2 * rh
        + 8.5282e-4 * t * rh**2
        - 1.99e-6 * t**2 * rh**2
    )
    return (hi - 32) * 5 / 9

def discomfort_index(ta, rh):
    return ta - (0.55 - 0.0055 * rh) * (ta - 14.5)

def effective_temperature(ta, rh, wind):
    return ta - 0.4 * (ta - 10) * (1 - rh / 100) - 0.7 * wind

def wind_chill(ta, wind):
    return 13.12 + 0.6215 * ta - 11.37 * wind**0.16 + 0.3965 * ta * wind**0.16

def pet_simplified(ta, rh, wind, met=1.2, clo=0.9):
    return (
        ta
        + 0.25 * (ta - 10) * (1 - wind) * (0.55 - 0.0055 * rh)
        + 0.6 * (met - 1.2)
        - 0.5 * (clo - 0.9)
    )

# ==================================================
# CLASSIFICATION
# ==================================================
def classify_heat_index(v):
    if v < 27: return "No Discomfort"
    elif v < 32: return "Caution"
    elif v < 41: return "Extreme Caution"
    elif v < 54: return "Danger"
    else: return "Extreme Danger"

def classify_di(v):
    if v < 21: return "No Discomfort"
    elif v < 24: return "Slight Discomfort"
    elif v < 27: return "Moderate Discomfort"
    else: return "Severe Discomfort"

def classify_et(v):
    if v < 16: return "Severe Cold Stress"
    elif v < 22: return "Slight Cold Stress"
    elif v < 27: return "Comfortable"
    else: return "Hot Stress"

def classify_wind_chill(v):
    if v > 10: return "No Cold Stress"
    elif v > 0: return "Slight Cold Stress"
    elif v > -10: return "Moderate Cold Stress"
    else: return "Severe Cold Stress"

def classify_pet(v):
    if v < 4: return "Very Cold"
    elif v < 8: return "Severe Cold Stress"
    elif v < 13: return "Moderate Cold Stress"
    elif v < 18: return "Slightly Cool"
    elif v < 23: return "Comfortable"
    elif v < 29: return "Slightly Warm"
    elif v < 35: return "Hot Stress"
    else: return "Extreme Danger"

def plot_class_distribution(df, class_col, class_colors):
    counts = df[class_col].value_counts()

    fig, ax = plt.subplots(figsize=(5, 4))

    bars = ax.bar(
        counts.index,
        counts.values,
        color=[class_colors.get(c, "#cccccc") for c in counts.index]
    )

    ax.set_title("Class Distribution")
    ax.set_ylabel("Count")
    ax.set_xlabel("")

    ax.set_xticklabels(counts.index, rotation=45, ha="right")

    # ✅ Add space above bars (important)
    max_count = counts.max()
    ax.set_ylim(0, max_count * 1.15)

    # ✅ Add value labels slightly above bars
    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            height + max_count * 0.02,
            f"{int(height)}",
            ha="center",
            va="bottom",
            fontsize=10
        )

    plt.tight_layout()
    return fig

# ==================================================
# TABS
# ==================================================
tab1, tab2 = st.tabs(["🔧 Analysis Setup", "📈 Results & Statistics"])

# ==================================================
# TAB 1 – ANALYSIS SETUP
# ==================================================
with tab1:

    left, right = st.columns([1, 2])

    with left:
        st.subheader("📥 Data Input")

        uploaded = st.file_uploader("Upload CSV or Excel", ["csv", "xlsx"])
        if uploaded is None:
            st.stop()

        df = pd.read_csv(uploaded) if uploaded.name.endswith(".csv") else pd.read_excel(uploaded)

        model = st.selectbox(
            "Thermal Comfort Index",
            ["Heat Index", "Discomfort Index (DI)", "Effective Temperature (ET)", "Wind Chill", "PET"]
        )

        ta_col = st.selectbox("Air Temperature (°C)", df.columns)

        if model != "Wind Chill":
            rh_col = st.selectbox("Relative Humidity (%)", df.columns)

        if model in ["Effective Temperature (ET)", "Wind Chill", "PET"]:
            wind_col = st.selectbox("Wind Speed (m/s)", df.columns)

        if model == "PET":
            met = st.slider("Metabolic Rate (met)", 0.8, 2.4, 1.2, 0.1)
            clo = st.slider("Clothing Insulation (clo)", 0.3, 1.5, 0.9, 0.05)

        if st.button("✅ Run Thermal Analysis"):

            # ---- CALCULATION PER MODEL (ALL DEFINED) ----
            if model == "Heat Index":
                values = heat_index_noaa(df[ta_col], df[rh_col])
                classes = values.apply(classify_heat_index)
                col_name = "Heat Index (°C)"

            elif model == "Discomfort Index (DI)":
                values = discomfort_index(df[ta_col], df[rh_col])
                classes = values.apply(classify_di)
                col_name = "Discomfort Index"

            elif model == "Effective Temperature (ET)":
                values = effective_temperature(df[ta_col], df[rh_col], df[wind_col])
                classes = values.apply(classify_et)
                col_name = "Effective Temperature (°C)"

            elif model == "Wind Chill":
                values = wind_chill(df[ta_col], df[wind_col])
                classes = values.apply(classify_wind_chill)
                col_name = "Wind Chill (°C)"

            elif model == "PET":
                values = pet_simplified(df[ta_col], df[rh_col], df[wind_col], met, clo)
                classes = values.apply(classify_pet)
                col_name = "PET (°C)"

            df_res = df.copy()
            df_res[col_name] = values
            df_res["Index_Class"] = classes

            st.session_state.result_df = df_res
            st.session_state.result_col = col_name
            st.session_state.selected_model = model

            st.success("✅ Analysis completed.")

    # ✅ DATA PREVIEW GERİ GELDİ
    with right:
        st.subheader("📊 Data Preview")
        st.dataframe(df, use_container_width=True, height=520)

# ==================================================
# TAB 2 – RESULTS & STATISTICS
# ==================================================

with tab2:

    if st.session_state.result_df is None:
        st.info("Run an analysis to see results.")
        st.stop()

    res = st.session_state.result_df
    col = st.session_state.result_col

    # ✅ EQUAL WIDTH COLUMNS
    left, right = st.columns([1, 1])

    # -----------------------------
    # LEFT: Calculated Indices
    # -----------------------------
    with left:
        st.subheader("📊 Calculated Indices")

        styled = (
            res[[col, "Index_Class"]]
            .style
            .applymap(style_class, subset=["Index_Class"])
        )

        st.dataframe(
            styled,
            use_container_width=True,
            height=420
        )

    # -----------------------------
    # RIGHT: Statistics + Chart
    # -----------------------------
    with right:
        st.subheader("📈 Statistical Summary")

        stats = (
            res[col]
            .describe()
            .loc[["mean", "std", "min", "50%", "max"]]
            .rename({
                "mean": "Mean",
                "std": "Std. Dev",
                "min": "Min",
                "50%": "Median",
                "max": "Max"
            })
        )

        st.dataframe(
            stats.to_frame(name=col).round(2),
            use_container_width=True
        )

        st.divider()
        st.subheader("📊 Class Distribution")

        fig = plot_class_distribution(
            res,
            class_col="Index_Class",
            class_colors=CLASS_COLORS
        )

        st.pyplot(fig)
        
        buf = io.BytesIO()
        fig.savefig(buf, format="png", dpi=600, bbox_inches="tight")
        buf.seek(0)

        st.download_button(
            label="⬇️ Download Class Distribution Chart",
            data=buf,
            file_name="class_distribution.png",
            mime="image/png",
            use_container_width=True
        )

render_footer()
