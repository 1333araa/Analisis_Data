import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
from matplotlib.patches import Patch

# ─────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────
st.set_page_config(
    page_title="Bike Sharing Dashboard",
    page_icon="🚲",
    layout="wide",
    initial_sidebar_state="expanded"
)

sns.set_style("whitegrid")
plt.rcParams["font.family"] = "DejaVu Sans"

# ─────────────────────────────────────────
# LOAD & PREP DATA
# ─────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("dashboard/main_data.csv", parse_dates=["dteday"])

    df["season_label"] = df["season"].map({1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"})
    df["weather_label"] = df["weather"].map({
        1: "Clear/Partly Cloudy",
        2: "Mist/Cloudy",
        3: "Light Rain/Snow",
        4: "Heavy Rain/Snow",
    })
    df["year_label"] = df["year"].map({0: "2011", 1: "2012"})
    df["weekday_label"] = df["weekday"].map({
        0: "Sunday", 1: "Monday", 2: "Tuesday", 3: "Wednesday",
        4: "Thursday", 5: "Friday", 6: "Saturday",
    })
    df["month_label"] = df["month"].map({
        1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun",
        7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec",
    })
    df["temp_celsius"]  = df["temp_norm"]  * 41
    df["humidity_pct"]  = df["humidity"]   * 100
    df["windspeed_kmh"] = df["windspeed_norm"] * 67
    return df


@st.cache_data
def load_hour():
    hour = pd.read_csv("data/hour.csv", parse_dates=["dteday"])
    hour.rename(columns={
        "yr": "year", "mnth": "month", "hum": "humidity",
        "cnt": "total_count", "temp": "temp_norm",
        "atemp": "atemp_norm", "windspeed": "windspeed_norm",
        "weathersit": "weather",
    }, inplace=True)
    hour["weekday_label"] = hour["weekday"].map({
        0: "Sunday", 1: "Monday", 2: "Tuesday", 3: "Wednesday",
        4: "Thursday", 5: "Friday", 6: "Saturday",
    })
    return hour


day_df  = load_data()
hour_df = load_hour()

# ─────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────
st.sidebar.image("https://img.icons8.com/color/96/000000/bicycle.png", width=80)
st.sidebar.title("🚲 Bike Sharing")
st.sidebar.markdown("**Analisis Data 2011–2012**")
st.sidebar.markdown("---")

year_filter = st.sidebar.multiselect(
    "Tahun", options=[0, 1], default=[0, 1],
    format_func=lambda x: "2011" if x == 0 else "2012"
)
season_filter = st.sidebar.multiselect(
    "Musim", options=[1, 2, 3, 4], default=[1, 2, 3, 4],
    format_func=lambda x: {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}[x]
)

df_filtered = day_df[
    day_df["year"].isin(year_filter) & day_df["season"].isin(season_filter)
]
hour_filtered = hour_df[hour_df["year"].isin(year_filter)]

st.sidebar.markdown("---")
st.sidebar.caption("Dashboard by Dicoding Final Project")

# ─────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────
st.title("🚲 Bike Sharing Analysis Dashboard")
st.markdown("Eksplorasi interaktif data penyewaan sepeda Washington D.C. (2011–2012)")
st.markdown("---")

# ─────────────────────────────────────────
# KPI METRICS
# ─────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)
col1.metric("📦 Total Penyewaan",       f"{df_filtered['total_count'].sum():,.0f}")
col2.metric("📅 Rata-rata/Hari",         f"{df_filtered['total_count'].mean():,.0f}")
col3.metric("👤 Pengguna Kasual",        f"{df_filtered['casual'].sum():,.0f}")
col4.metric("🎟️ Pengguna Terdaftar",    f"{df_filtered['registered'].sum():,.0f}")

st.markdown("---")

# ─────────────────────────────────────────
# TAB LAYOUT
# ─────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["🌤️ Cuaca & Musim", "⏰ Pola Jam & Hari", "📊 Clustering Jam"])

# ══════════════════════════════════════════
# TAB 1 — CUACA & MUSIM
# ══════════════════════════════════════════
with tab1:
    st.subheader("Pertanyaan 1: Bagaimana pengaruh cuaca & musim terhadap penyewaan?")

    c1, c2 = st.columns(2)

    # Boxplot musim
    with c1:
        fig, ax = plt.subplots(figsize=(7, 4))
        order_s = ["Spring", "Summer", "Fall", "Winter"]
        palette_s = {"Spring": "#81C784", "Summer": "#FFB74D", "Fall": "#F06292", "Winter": "#64B5F6"}
        sns.boxplot(data=df_filtered, x="season_label", y="total_count",
                    order=order_s, palette=palette_s, ax=ax)
        ax.set_title("Distribusi Penyewaan per Musim", fontweight="bold")
        ax.set_xlabel("Musim")
        ax.set_ylabel("Total Penyewaan/Hari")
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    # Bar cuaca
    with c2:
        fig, ax = plt.subplots(figsize=(7, 4))
        order_w = ["Clear/Partly Cloudy", "Mist/Cloudy", "Light Rain/Snow"]
        pal_w = {"Clear/Partly Cloudy": "#AED6F1", "Mist/Cloudy": "#7FB3D3", "Light Rain/Snow": "#4A90D9"}
        wdf = df_filtered[df_filtered["weather_label"].isin(order_w)]
        weather_avg = wdf.groupby("weather_label", observed=True)["total_count"].mean().reindex(order_w)
        bars = ax.bar(order_w, weather_avg.values, color=[pal_w[k] for k in order_w], edgecolor="white")
        for bar, val in zip(bars, weather_avg.values):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 30,
                    f"{val:.0f}", ha="center", fontsize=9, fontweight="bold")
        ax.set_title("Rata-rata Penyewaan per Kondisi Cuaca", fontweight="bold")
        ax.set_ylabel("Rata-rata/Hari")
        ax.tick_params(axis="x", rotation=12)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    # Scatter suhu
    fig, ax = plt.subplots(figsize=(12, 4))
    sc = ax.scatter(df_filtered["temp_celsius"], df_filtered["total_count"],
                    c=df_filtered["season"].cat.codes if hasattr(df_filtered["season"], "cat")
                    else df_filtered["season"],
                    cmap="RdYlGn", alpha=0.5, s=18)
    z = np.polyfit(df_filtered["temp_celsius"], df_filtered["total_count"], 2)
    p = np.poly1d(z)
    xline = np.linspace(df_filtered["temp_celsius"].min(), df_filtered["temp_celsius"].max(), 100)
    ax.plot(xline, p(xline), "r--", linewidth=2, label="Trend (Poly2)")
    ax.set_title("Suhu (°C) vs Total Penyewaan Harian", fontweight="bold")
    ax.set_xlabel("Suhu (°C)")
    ax.set_ylabel("Total Penyewaan")
    ax.legend()
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    st.info("""
    **Insight:**
    - Musim **Fall** memiliki rata-rata penyewaan tertinggi; Spring terendah.
    - Cuaca **cerah** menghasilkan ~2.7x lebih banyak penyewaan dibanding hujan ringan.
    - Suhu optimal untuk bersepeda berada di kisaran **20–28°C**.
    - Kelembaban tinggi berkorelasi negatif dengan jumlah penyewaan.
    """)

# ══════════════════════════════════════════
# TAB 2 — POLA JAM & HARI
# ══════════════════════════════════════════
with tab2:
    st.subheader("Pertanyaan 2: Bagaimana pola penyewaan berdasarkan jam dan hari?")

    c1, c2 = st.columns(2)

    with c1:
        fig, ax = plt.subplots(figsize=(7, 4))
        hourly_wd = hour_filtered[hour_filtered["workingday"] == 1].groupby("hr")["total_count"].mean()
        hourly_we = hour_filtered[hour_filtered["workingday"] == 0].groupby("hr")["total_count"].mean()
        ax.plot(hourly_wd.index, hourly_wd.values, "o-", color="#1565C0", linewidth=2, markersize=4, label="Hari Kerja")
        ax.plot(hourly_we.index, hourly_we.values, "s-", color="#E65100", linewidth=2, markersize=4, label="Akhir Pekan")
        ax.axvspan(6, 9, alpha=0.08, color="blue")
        ax.axvspan(16, 19, alpha=0.08, color="green")
        ax.set_title("Rata-rata Penyewaan per Jam", fontweight="bold")
        ax.set_xlabel("Jam (0–23)")
        ax.set_ylabel("Rata-rata Penyewaan")
        ax.set_xticks(range(0, 24, 2))
        ax.legend()
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    with c2:
        fig, ax = plt.subplots(figsize=(7, 4))
        order_d = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        wd_data = df_filtered.groupby("weekday_label", observed=True)[["casual", "registered"]].mean()
        wd_data = wd_data.reindex(order_d)
        x = np.arange(len(order_d))
        w = 0.35
        ax.bar(x - w/2, wd_data["casual"],     width=w, label="Kasual",    color="#F4845F", edgecolor="white")
        ax.bar(x + w/2, wd_data["registered"], width=w, label="Terdaftar", color="#4C9BE8", edgecolor="white")
        ax.set_xticks(x)
        ax.set_xticklabels(order_d, rotation=20, ha="right", fontsize=8)
        ax.set_title("Rata-rata Penyewaan per Hari", fontweight="bold")
        ax.set_ylabel("Rata-rata/Hari")
        ax.legend()
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    # Heatmap jam × hari
    fig, ax = plt.subplots(figsize=(14, 4))
    order_d = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    pivot_hw = hour_filtered.groupby(["weekday_label", "hr"], observed=True)["total_count"].mean().unstack()
    pivot_hw = pivot_hw.reindex(order_d)
    sns.heatmap(pivot_hw, cmap="YlOrRd", ax=ax, linewidths=0,
                cbar_kws={"label": "Rata-rata/Jam"})
    ax.set_title("Heatmap: Hari × Jam dalam Sehari", fontweight="bold")
    ax.set_xlabel("Jam")
    ax.set_ylabel("Hari")
    ax.set_xticks(range(0, 24, 2))
    ax.set_xticklabels(range(0, 24, 2))
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    st.info("""
    **Insight:**
    - **Hari kerja** memiliki pola bimodal: puncak pagi (08.00) & sore (17–18.00) — pola komuter.
    - **Akhir pekan** berpola unimodal di siang hari (10–14.00) — pola rekreasi.
    - Pengguna **terdaftar** dominan pada hari kerja; pengguna **kasual** dominan di akhir pekan.
    """)

# ══════════════════════════════════════════
# TAB 3 — CLUSTERING
# ══════════════════════════════════════════
with tab3:
    st.subheader("Analisis Lanjutan: Clustering Jam Berdasarkan Intensitas Penggunaan")
    st.markdown("Pengelompokan jam menggunakan **manual binning berbasis kuartil** untuk membantu optimasi distribusi armada.")

    hourly_stats = hour_filtered.groupby("hr").agg(
        avg_total  = ("total_count", "mean"),
        avg_casual = ("casual",      "mean"),
        avg_reg    = ("registered",  "mean"),
    ).reset_index()

    q1, q2, q3 = hourly_stats["avg_total"].quantile([0.25, 0.50, 0.75])

    def assign_cluster(val):
        if val <= q1:   return "Sangat Rendah"
        elif val <= q2: return "Rendah"
        elif val <= q3: return "Tinggi"
        else:           return "Sangat Tinggi"

    hourly_stats["cluster"] = hourly_stats["avg_total"].apply(assign_cluster)
    hourly_stats["cluster"] = pd.Categorical(
        hourly_stats["cluster"],
        categories=["Sangat Rendah", "Rendah", "Tinggi", "Sangat Tinggi"],
        ordered=True
    )

    color_map = {
        "Sangat Rendah": "#B0BEC5",
        "Rendah":        "#81C784",
        "Tinggi":        "#FFB74D",
        "Sangat Tinggi": "#E57373",
    }

    c1, c2 = st.columns(2)

    with c1:
        fig, ax = plt.subplots(figsize=(7, 4))
        colors_bar = [color_map[c] for c in hourly_stats["cluster"]]
        ax.bar(hourly_stats["hr"], hourly_stats["avg_total"],
               color=colors_bar, edgecolor="white", linewidth=0.5)
        legend_elements = [Patch(facecolor=color_map[k], label=k) for k in color_map]
        ax.legend(handles=legend_elements, title="Cluster", fontsize=8)
        ax.set_title("Rata-rata Penyewaan per Jam (Clustering)", fontweight="bold")
        ax.set_xlabel("Jam (0–23)")
        ax.set_ylabel("Rata-rata Penyewaan")
        ax.set_xticks(range(0, 24))
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    with c2:
        fig, ax = plt.subplots(figsize=(7, 4))
        for cluster, grp in hourly_stats.groupby("cluster", observed=True):
            ax.scatter(grp["avg_casual"], grp["avg_reg"],
                       s=grp["avg_total"] * 0.8,
                       c=color_map[cluster], label=cluster, alpha=0.85, edgecolors="white")
            for _, row in grp.iterrows():
                ax.annotate(f"{int(row['hr'])}h", (row["avg_casual"], row["avg_reg"]),
                            fontsize=7, ha="center")
        ax.set_title("Kasual vs Terdaftar per Jam", fontweight="bold")
        ax.set_xlabel("Rata-rata Pengguna Kasual")
        ax.set_ylabel("Rata-rata Pengguna Terdaftar")
        ax.legend(title="Cluster", fontsize=8)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    # Tabel cluster
    cluster_tbl = hourly_stats.groupby("cluster", observed=True).apply(
        lambda g: pd.Series({
            "Jam": str(sorted(g["hr"].tolist())),
            "Rata-rata/Jam": f"{g['avg_total'].mean():.1f}",
            "% Kasual": f"{(g['avg_casual'] / g['avg_total']).mean()*100:.1f}%",
        })
    ).reset_index()
    st.dataframe(cluster_tbl, use_container_width=True)

    st.info("""
    **Insight:**
    - **Sangat Tinggi** (07–09, 17–19): Rush hour — prioritaskan ketersediaan armada penuh.
    - **Tinggi** (10–16): Aktivitas siang — pertahankan ketersediaan sepeda.
    - **Rendah** (20–22): Mulai rotasi & redistribusi armada.
    - **Sangat Rendah** (00–06, 23): Waktu ideal untuk maintenance & redistribusi antar stasiun.
    """)
