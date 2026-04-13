import streamlit as st
from utils.footer import render_footer

st.set_page_config(
    page_title="Help",
    page_icon="❓"
)

st.title("❓Help")

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
            <span class="current">Help</span>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("""
---

## 1. What is ThermoGIS?

**ThermoGIS** is a web-based platform designed to:

- Calculate **thermal comfort indices** from meteorological data,
- Analyze results statistically,
- Visualize spatial patterns using interpolation and maps,
- Support **urban climate studies, thermal comfort research, and decision-making**.

The software is especially suitable for:
- City and regional scale studies,
- Outdoor thermal comfort assessments,
- Academic research and applied GIS analysis.

---

## 2. Application Structure

ThermoGIS consists of four main pages:

- **Thermal Analysis**
- **Spatial Interpolation**
- **Help**
- **About**

This Help page explains how to use the **Thermal Analysis** and **Spatial Interpolation** modules step by step.

---

## 3. Thermal Analysis Page

The **Thermal Analysis** page is used to compute thermal comfort indices from point-based meteorological data.

### 3.1. Data Input

At the top of the page, you can upload a dataset in one of the following formats:

- CSV (`.csv`)
- Excel (`.xlsx`)

The dataset should include meteorological variables such as:
- Air temperature (°C),
- Relative humidity (%),
- Wind speed (m/s),
depending on the selected index.

After uploading the file, a **data preview** is shown on the right side of the page.

---

### 3.2. Thermal Comfort Indices

You can select one of the following indices:

#### 🔹 Heat Index  
Represents heat stress under high temperature and humidity conditions.

#### 🔹 Discomfort Index (DI)  
Evaluates human discomfort based on temperature and humidity.

#### 🔹 Effective Temperature (ET)  
Combines temperature, humidity, and wind effects.

#### 🔹 Wind Chill  
Represents perceived cold stress due to wind under cold conditions.

#### 🔹 PET (Physiological Equivalent Temperature)  
A human-biometeorological index widely used for **outdoor thermal comfort analysis**.

> ℹ️ PET is computed using a **simplified, Streamlit-safe formulation** to ensure stable performance.

---

### 3.3. Parameter Selection

Based on the selected index, relevant columns must be selected from the dataset:

- Air Temperature
- Relative Humidity
- Wind Speed

For PET, additional personal parameters can be set:
- **Metabolic Rate (met)**
- **Clothing Insulation (clo)**

---

### 3.4. Running the Analysis

Click **“Run Thermal Analysis”** to start the computation.

The software will:
- Calculate the selected index,
- Assign a **thermal stress class** to each record,
- Store results automatically for further analysis.

---

## 4. Results & Statistics Page

This page displays **all computed results automatically**.

### 4.1. Results Table (Left Panel)

The table includes:
- The computed index value,
- The corresponding **thermal stress class**.

All classes are displayed using a **consistent color system**:

- 🟢 Green → Comfortable / No stress
- 🟡 Yellow → Mild stress
- 🟠 Orange → Moderate stress
- 🔴 Red → Severe stress
- 🟣 Dark red → Extreme stress

The same color system is used throughout the application.

---

### 4.2. Statistical Summary (Right Panel)

For the selected index, the following statistics are shown:

- Mean
- Standard Deviation
- Minimum
- Median
- Maximum

This provides a quick overview of the general thermal conditions in the dataset.

---

### 4.3. Class Distribution Chart

Below the statistics, a **bar chart** shows the distribution of thermal stress classes.

This chart helps identify:
- Dominant stress levels,
- Frequency of extreme or comfortable conditions,
- Overall thermal conditions of the study area.

---

## 5. Spatial Interpolation Page

The **Spatial Interpolation** page is used to visualize analysis results on a map.

### 5.1. Point Data

You upload or select:
- Latitude,
- Longitude,
- A numeric variable (e.g. PET, Heat Index).

Points are displayed directly on the interactive map.

---

### 5.2. Interpolation Boundary

A boundary file in **GeoPackage (.gpkg)** format can be uploaded.

This boundary:
- Defines the spatial extent,
- Is used for automatic map zooming,
- Acts as a reference area for interpolation.

---

### 5.3. IDW Interpolation

Interpolation is performed using **Inverse Distance Weighting (IDW)**.

You can adjust:
- Grid resolution,
- IDW power parameter.

The resulting surface is displayed as a raster layer.

---

### 5.4. Map & Legend

The map includes:
- Point locations,
- Interpolated surface,
- A **class-based legend**.

The legend uses the **same color system** as the Thermal Analysis page.

---

### 5.5. GeoTIFF Export

The interpolated surface can be downloaded as a:

- **GeoTIFF (.tif)** file

This file can be opened directly in GIS software such as:
- QGIS
- ArcGIS

""")

render_footer()