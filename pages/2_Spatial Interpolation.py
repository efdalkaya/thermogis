
import streamlit as st
import pandas as pd
import geopandas as gpd
import numpy as np
import folium
from streamlit_folium import st_folium
from scipy.spatial import cKDTree
import matplotlib.cm as cm
import matplotlib.colors as colors
import branca.colormap as bcm
import rasterio
from rasterio.transform import from_bounds
import tempfile

from utils.footer import render_footer

st.set_page_config(
    page_title="Spatial Interpolation",
    page_icon="🔄"
)

st.title("🔄 Spatial Interpolation")

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
            <span class="current">Spatial Interpolation</span>
        </div>
        """,
        unsafe_allow_html=True
    )

# ==================================================
# SESSION STATE INITIALIZATION
# ==================================================
for key in [
    "lat_col", "lon_col", "val_col",
    "idw_done", "idw_bounds",
    "idw_vmin", "idw_vmax",
    "idw_image", "idw_array",
    "colormap"
]:
    if key not in st.session_state:
        st.session_state[key] = None

# ==================================================
# IDW FUNCTION
# ==================================================
def idw_interpolation(x, y, z, xi, yi, power=2):
    tree = cKDTree(np.c_[x, y])
    dist, idx = tree.query(np.c_[xi.ravel(), yi.ravel()], k=8)
    weights = 1.0 / (dist ** power + 1e-12)
    zi = np.sum(weights * z[idx], axis=1) / np.sum(weights, axis=1)
    return zi.reshape(xi.shape)

# ==================================================
# GEOTIFF EXPORT FUNCTION
# ==================================================
def export_geotiff(z, bounds, crs="EPSG:4326"):
    ymin, xmin = bounds[0]
    ymax, xmax = bounds[1]
    height, width = z.shape

    transform = from_bounds(xmin, ymin, xmax, ymax, width, height)

    tmp = tempfile.NamedTemporaryFile(suffix=".tif", delete=False)

    with rasterio.open(
        tmp.name,
        "w",
        driver="GTiff",
        height=height,
        width=width,
        count=1,
        dtype=str(z.dtype),
        crs=crs,
        transform=transform,
        nodata=np.nan,
    ) as dst:
        dst.write(z, 1)

    return tmp.name

# ==================================================
# LAYOUT
# ==================================================
left, right = st.columns([1, 2])

# ==================================================
# LEFT PANEL – INPUTS
# ==================================================
with left:
    st.subheader("📥 Point Data")

    data_file = st.file_uploader("Upload CSV or Excel", ["csv", "xlsx"])
    df = None

    if data_file:
        df = pd.read_csv(data_file) if data_file.name.endswith(".csv") else pd.read_excel(data_file)

    if df is not None:
        st.markdown("### 🔧 Select Columns")
        st.session_state.lat_col = st.selectbox("Latitude", df.columns)
        st.session_state.lon_col = st.selectbox("Longitude", df.columns)
        st.session_state.val_col = st.selectbox("Interpolation Variable", df.columns)

    st.subheader("🗂️ Interpolation Boundary")
    boundary_file = st.file_uploader("Upload boundary (.gpkg)", ["gpkg"])
    gdf_boundary = None

    if boundary_file:
        gdf_boundary = gpd.read_file(boundary_file).to_crs(epsg=4326)
        gdf_boundary = gdf_boundary[["geometry"]]

    resolution = st.slider(
        "Grid Resolution (higher = more detail, slower)",
        min_value=100,
        max_value=1000,
        value=500,
        step=50
    )

    st.caption(
        "ℹ️ City scale: 300–500 | Province scale: 500–800 | Very high values may slow down computation."
    )

    power = st.slider("IDW Power", 1.0, 4.0, 2.0, 0.5)

    st.subheader("🎨 Color Palette")
    st.session_state.colormap = st.selectbox(
        "Select color palette",
        ["coolwarm", "viridis", "plasma", "YlOrRd", "Blues"]
    )

    if st.button("▶ Run IDW Interpolation", use_container_width=True):

        st.session_state.idw_done = True

        # ✅ GRID EXTENT = INTERPOLATION BOUNDARY
        xmin, ymin, xmax, ymax = gdf_boundary.total_bounds

        xi = np.linspace(xmin, xmax, resolution)
        yi = np.linspace(ymin, ymax, resolution)
        xi, yi = np.meshgrid(xi, yi)

        zi = idw_interpolation(
            df[st.session_state.lon_col].values,
            df[st.session_state.lat_col].values,
            df[st.session_state.val_col].values,
            xi, yi,
            power=power
        )

        # Store arrays & bounds
        st.session_state.idw_array = zi
        st.session_state.idw_bounds = [[ymin, xmin], [ymax, xmax]]
        st.session_state.idw_vmin = float(np.nanmin(zi))
        st.session_state.idw_vmax = float(np.nanmax(zi))

        norm = colors.Normalize(
            vmin=st.session_state.idw_vmin,
            vmax=st.session_state.idw_vmax
        )

        cmap = cm.get_cmap(st.session_state.colormap)
        rgba = cmap(norm(zi))
        image = (rgba[:, :, :3] * 255).astype(np.uint8)
        st.session_state.idw_image = image

# ==================================================
# MAP VIEW – RIGHT PANEL
# ==================================================

with right:
    st.subheader("🌍 Map View")

    if df is None or gdf_boundary is None:
        st.info("Upload point data and interpolation boundary.")
        st.stop()

    # Initial map (temporary center)
    m = folium.Map(
        location=[
            df[st.session_state.lat_col].mean(),
            df[st.session_state.lon_col].mean()
        ],
        zoom_start=8,
        tiles="OpenStreetMap"
    )

    # ---- POINTS ----
    for _, r in df.iterrows():
        folium.CircleMarker(
            [r[st.session_state.lat_col], r[st.session_state.lon_col]],
            radius=4,
            color="blue",
            fill=True,
            fill_opacity=0.7
        ).add_to(m)

    # ---- BOUNDARY ----
    folium.GeoJson(
        gdf_boundary,
        style_function=lambda x: {
            "color": "red",
            "weight": 2,
            "fillOpacity": 0
        },
        name="Interpolation Boundary"
    ).add_to(m)

    # ✅ AUTO-ZOOM TO BOUNDARY
    xmin, ymin, xmax, ymax = gdf_boundary.total_bounds
    m.fit_bounds([[ymin, xmin], [ymax, xmax]])

    # ---- IDW OVERLAY ----
    if st.session_state.idw_done:
        folium.raster_layers.ImageOverlay(
            image=st.session_state.idw_image,
            bounds=st.session_state.idw_bounds,
            opacity=0.6,
            name="IDW Interpolation"
        ).add_to(m)

        bcm.LinearColormap(
            cm.get_cmap(st.session_state.colormap).colors
            if hasattr(cm.get_cmap(st.session_state.colormap), "colors")
            else [cm.get_cmap(st.session_state.colormap)(i) for i in np.linspace(0, 1, 256)],
            vmin=st.session_state.idw_vmin,
            vmax=st.session_state.idw_vmax,
            caption="IDW Value"
        ).add_to(m)

        # Download button (aynı kalır)
        tif_path = export_geotiff(
            st.session_state.idw_array,
            st.session_state.idw_bounds
        )

        with open(tif_path, "rb") as f:
            st.download_button(
                "⬇️ Download IDW GeoTIFF",
                f,
                file_name="idw_interpolation.tif",
                mime="image/tiff",
                use_container_width=True
            )

    folium.LayerControl().add_to(m)
    st_folium(m, width=900, height=600)

render_footer()
