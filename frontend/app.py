import os
import requests
import pandas as pd
import streamlit as st
import plotly.express as px

# ==========================================
# 1. PAGE LAYOUT & STREAMLIT CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Customer Segmentation Control Center",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Pull internal routing configurations safely from environment definitions
BACKEND_URL = os.getenv("BACKEND_API_URL", "http://127.0.0")

# Core application layout branding header anchors
st.title("📊 Customer Segmentation & Anomaly Dashboard")
st.markdown("""
Transform flat transaction logs into multi-dimensional behavioral marketing cohorts. 
This system utilizes a **DBSCAN parameter sweep engine** to group consumers and isolate system anomalies via **PCA reduction**.
""")

# Setup sidebar data collection controls
st.sidebar.header("📁 Data Management Center")
uploaded_file = st.sidebar.file_uploader(
    "Upload Transaction Log History (.CSV)", 
    type=["csv"],
    help="Requires headers: CustomerID, Quantity, UnitPrice, InvoiceDate, InvoiceNo"
)

# ==========================================
# 2. RUNTIME INGESTION ENGINE INTERACTION
# ==========================================
if uploaded_file is not None:
    st.sidebar.success("File context successfully loaded into system memory buffer.")
    
    # Initialize computation processing triggers
    if st.sidebar.button("Run Segmentation Pipeline", type="primary"):
        with st.spinner("Streaming file stream to FastAPI for parameter optimization and clustering..."):
            try:
                # Wrap binary data objects into standard multipart/form-data payload arrays
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "text/csv")}
                response = requests.post(BACKEND_URL, files=files, timeout=60)
                
                if response.status_code == 200:
                    # Parse returned dictionary payload structures out into app variables
                    payload = response.json()
                    metrics = payload["metadata"]
                    df_res = pd.DataFrame(payload["data"])
                    
                    # Store current run state data into user stream context blocks
                    st.session_state['df_res'] = df_res
                    st.session_state['metrics'] = metrics
                    st.sidebar.info("Model pipeline execution tracking state saved.")
                else:
                    st.sidebar.error(f"Server rejected parsing: {response.json().get('detail', 'Unknown error')}")
            except requests.exceptions.RequestException as e:
                st.sidebar.error(f"Failed to communicate with the downstream cluster worker node: {str(e)}")

# ==========================================
# 3. INTERACTIVE METRIC & GRAPH PRESENTATION
# ==========================================
if 'df_res' in st.session_state and 'metrics' in st.session_state:
    df_res = st.session_state['df_res']
    metrics = st.session_state['metrics']
    
    # Render key machine learning metrics across dashboard summary tiles
    st.markdown("### 📈 Pipeline Optimization Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    col1.metric("Optimized DBSCAN Radius (Eps)", f"{metrics['eps']:.2f}")
    col2.metric("Min Density Core Threshold", f"{metrics['min_samples']}")
    col3.metric("Silhouette Evaluation Score", f"{metrics['silhouette_score']:.4f}")
    
    # Map visual markers indicating whether the PCA metrics satisfy stability rules
    variance_flag = "🟢 Passing" if metrics['variance_threshold_met'] else "🔴 Low Information"
    col4.metric("PCA Explained Variance Total", f"{metrics['total_explained_variance']*100:.2f}%", delta=variance_flag)
    
    st.markdown("---")
    
    # Separate anomalies and valid target core groupings
    outliers = df_res[df_res['Cluster'] == -1]
    valid_segments = df_res[df_res['Cluster'] != -1]
    
    # Create responsive navigation dashboard layout elements
    tab_viz, tab_anomalies, tab_export = st.tabs([
        "🚀 Interactive 3D Clusters", 
        "🚨 Outlier Telemetry Tracker", 
        "📥 Automated Marketing Exporter"
    ])
    
    with tab_viz:
        st.subheader("Principal Component Interaction Space Topology")
        st.markdown("Click, drag, and scroll on the plot below to explore patterns in your consumer segments.")
        
        # Cast tracking identifiers to discrete strings to force categorical color splits
        valid_segments['Cluster_Label'] = valid_segments['Cluster'].astype(str).apply(lambda x: f"Cluster {float(x):.0f}")
        
        # Build high-density 3D spatial models natively across client web engines
        fig = px.scatter_3d(
            valid_segments, 
            x='PC1', y='PC2', z='PC3',
            color='Cluster_Label',
            title='Customer Behavior Topology',
            hover_data=['CustomerID', 'Recency', 'Frequency', 'Monetary'],
            color_discrete_sequence=px.colors.qualitative.Bold,
            height=700
        )
        
        fig.update_layout(
            margin=dict(l=0, r=0, b=0, t=30),
            scene=dict(
                xaxis_title='PC 1 (Recency Focus)',
                yaxis_title='PC 2 (Frequency Focus)',
                zaxis_title='PC 3 (Monetary Focus)'
            )
        )
        st.plotly_chart(fig, use_container_width=True)
        
    with tab_anomalies:
        st.subheader("Isolated System Noise & Bulk Buying Entities")
        st.markdown(f"DBSCAN density scans flagged **{len(outliers)}** out-of-bounds user entities as structural anomalies.")
        
        if not outliers.empty:
            st.dataframe(
                outliers[['CustomerID', 'Recency', 'Frequency', 'Monetary']],
                use_container_width=True
            )
            st.warning("⚠️ These rows typically indicate wholesale scrapers, data entry bugs, or extreme outliers. Filter them out of your standard marketing campaigns.")
        else:
            st.success("🎉 Excellent data homogeneity. Zero structural anomalies or outliers were detected in this dataset.")
            
    with tab_export:
        st.subheader("Dynamic Cohort Packaging & Download Core")
        st.markdown("Extract distinct customer files to feed into your CRM or marketing automation tools.")
        
        # Map clusters to operational marketing strategy names
        cluster_list = sorted(df_res['Cluster'].unique())
        
        selected_cluster = st.selectbox(
            "Select Customer Portfolio Focus to Bundle:", 
            options=cluster_list,
            format_func=lambda x: f"System Group Anomaly Target (Cluster {x})" if x == -1 else f"Core Operational Cluster Segment {int(x)}"
        )
        
        # Bundle chosen cohorts on the fly into clean download buffers
        cohort = df_res[df_res['Cluster'] == selected_cluster]
        
        st.markdown(f"**Cohort Summary Stats:** This group contains **{len(cohort)}** unique user records.")
        st.dataframe(cohort[['CustomerID', 'Recency', 'Frequency', 'Monetary']].head(10), use_container_width=True)
        
        # Build in-memory file streaming triggers
        csv_buffer = cohort[['CustomerID', 'Recency', 'Frequency', 'Monetary']].to_csv(index=False)
        
        st.download_button(
            label=f"Download Portfolio Package CSV (Cluster {selected_cluster})",
            data=csv_buffer,
            file_name=f"customer_cohort_cluster_{selected_cluster}.csv",
            mime="text/csv",
            type="secondary"
        )
else:
    # Handle baseline greeting frame when no dataset is present inside global thread session states
    st.info("👋 Welcome to the Segmentation System. Please locate the side panel control deck, feed in your transactional file history data records, and run the machine learning pipeline model to initialize calculations views.")
