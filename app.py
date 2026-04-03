import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# ─── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Supermarket Sales EDA",
    page_icon="assets/icon.png" if False else None,
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Google Fonts + Custom CSS ────────────────────────────────────────────────
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&display=swap" rel="stylesheet">

<style>
/* ── Root palette ── */
:root {
    --bg:           #F8F6F1;
    --surface:      #FFFFFF;
    --accent:       #2D6A4F;
    --accent-light: #52B788;
    --accent-muted: #D8F3DC;
    --warn:         #E76F51;
    --text-primary: #1A1A2E;
    --text-muted:   #6B7280;
    --border:       #E5E0D8;
}

/* ── Global background ── */
html, body, .stApp, [data-testid="stAppViewContainer"] {
    background-color: var(--bg) !important;
    font-family: 'DM Sans', sans-serif;
    color: var(--text-primary);
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background-color: var(--accent) !important;
}
[data-testid="stSidebar"] * {
    color: #FFFFFF !important;
}
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stRadio label,
[data-testid="stSidebar"] p {
    color: rgba(255,255,255,0.85) !important;
    font-size: 0.85rem;
    letter-spacing: 0.03em;
}
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #FFFFFF !important;
    font-family: 'DM Serif Display', serif;
}

/* ── Headings ── */
h1, h2, h3, h4 {
    font-family: 'DM Serif Display', serif !important;
    color: var(--text-primary) !important;
}

/* ── Metric cards ── */
[data-testid="metric-container"] {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1rem 1.2rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    font-family: 'DM Serif Display', serif;
    font-size: 1.8rem !important;
    color: var(--accent) !important;
}
[data-testid="metric-container"] [data-testid="stMetricLabel"] {
    font-size: 0.78rem;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    color: var(--text-muted) !important;
}

/* ── Section dividers ── */
hr {
    border: none;
    border-top: 1px solid var(--border);
    margin: 1.5rem 0;
}

/* ── Dataframe ── */
[data-testid="stDataFrame"] {
    border-radius: 10px;
    overflow: hidden;
    border: 1px solid var(--border);
}

/* ── Plot containers ── */
[data-testid="stImage"] img {
    border-radius: 10px;
}

/* ── Selectbox / Radio ── */
.stSelectbox > div > div,
.stRadio > div {
    background: var(--surface) !important;
    border-radius: 8px !important;
    border: 1px solid var(--border) !important;
}

/* ── Tabs ── */
[data-baseweb="tab-list"] {
    background: var(--surface) !important;
    border-bottom: 2px solid var(--border) !important;
    border-radius: 8px 8px 0 0;
    gap: 0;
}
[data-baseweb="tab"] {
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500;
    color: var(--text-muted) !important;
    padding: 0.65rem 1.4rem !important;
}
[aria-selected="true"][data-baseweb="tab"] {
    color: var(--accent) !important;
    border-bottom: 3px solid var(--accent) !important;
}

/* ── Callout boxes ── */
.insight-box {
    background: var(--accent-muted);
    border-left: 4px solid var(--accent);
    border-radius: 0 8px 8px 0;
    padding: 0.8rem 1.1rem;
    margin: 0.6rem 0 1.2rem;
    font-size: 0.88rem;
    color: #1A3D28;
    line-height: 1.55;
}

/* ── Section header band ── */
.section-header {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 0.7rem 1.2rem;
    margin-bottom: 1.2rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.section-header h3 {
    margin: 0 !important;
    font-size: 1.05rem !important;
    color: var(--accent) !important;
}

/* ── Hero strip ── */
.hero {
    background: linear-gradient(135deg, var(--accent) 0%, #1B4332 100%);
    border-radius: 14px;
    padding: 2.2rem 2.5rem;
    margin-bottom: 1.8rem;
}
.hero h1 { color: #FFFFFF !important; font-size: 2.1rem !important; margin: 0 0 0.4rem; }
.hero p  { color: rgba(255,255,255,0.80); font-size: 0.95rem; margin: 0; }
</style>
""", unsafe_allow_html=True)

# ─── Matplotlib theme ──────────────────────────────────────────────────────────
PALETTE = ["#2D6A4F", "#52B788", "#E76F51", "#F4A261", "#264653", "#74C69D", "#A8DADC"]
sns.set_theme(style="whitegrid", palette=PALETTE)
plt.rcParams.update({
    "font.family":      "DejaVu Sans",
    "axes.facecolor":   "#FFFFFF",
    "figure.facecolor": "#FFFFFF",
    "axes.edgecolor":   "#E5E0D8",
    "axes.titlesize":   12,
    "axes.titleweight": "bold",
    "axes.labelsize":   10,
    "xtick.labelsize":  9,
    "ytick.labelsize":  9,
    "axes.spines.top":  False,
    "axes.spines.right":False,
    "grid.color":       "#F0EDE8",
    "grid.linewidth":   0.7,
})

# ─── Helper ────────────────────────────────────────────────────────────────────
def insight(text: str):
    st.markdown(f'<div class="insight-box">{text}</div>', unsafe_allow_html=True)

def section(title: str):
    st.markdown(f'<div class="section-header"><h3>{title}</h3></div>', unsafe_allow_html=True)

def fig_show(fig):
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

# ─── Data Loading ──────────────────────────────────────────────────────────────
@st.cache_data
def load_data(file):
    df = pd.read_csv(file)
    df.columns = df.columns.str.strip()
    # Date parsing
    df["Date"] = pd.to_datetime(df["Date"], dayfirst=False, errors="coerce")
    df["month"]  = df["Date"].dt.month_name()
    df["hour"]   = pd.to_datetime(df["Time"], format="%H:%M", errors="coerce").dt.hour
    return df

# ─── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## Supermarket EDA")
    st.markdown("---")
    uploaded = st.file_uploader("Upload CSV dataset", type=["csv"])
    st.markdown("---")
    st.markdown("**Navigation**")
    section_choice = st.radio(
        "",
        ["Overview", "Univariate Analysis", "Bivariate Analysis", "Business Insights"],
        label_visibility="collapsed",
    )
    st.markdown("---")
    st.markdown(
        "<p style='font-size:0.78rem;opacity:0.7'>Supermarket Sales Dataset · EDA</p>",
        unsafe_allow_html=True,
    )

# ─── Load ──────────────────────────────────────────────────────────────────────
if uploaded:
    dt = load_data(uploaded)
else:
    st.markdown("""
    <div class="hero">
        <h1>Supermarket Sales EDA</h1>
        <p>Upload your <strong>supermarket_sales.csv</strong> file in the sidebar to begin the analysis.</p>
    </div>
    """, unsafe_allow_html=True)
    st.info("Please upload the dataset using the sidebar to continue.")
    st.stop()

# ─── Filters ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("**Filters**")
    all_branches = ["All"] + sorted(dt["Branch"].dropna().unique().tolist())
    branch_sel = st.selectbox("Branch", all_branches)
    all_cities = ["All"] + sorted(dt["City"].dropna().unique().tolist())
    city_sel = st.selectbox("City", all_cities)

df = dt.copy()
if branch_sel != "All":
    df = df[df["Branch"] == branch_sel]
if city_sel != "All":
    df = df[df["City"] == city_sel]

# ─── HERO ──────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero">
    <h1>Supermarket Sales — Exploratory Analysis</h1>
    <p>Uncovering patterns in customer behaviour, branch performance, and product line revenue across 3 cities.</p>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
if section_choice == "Overview":
    section("Dataset Snapshot")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Records",    f"{len(df):,}")
    c2.metric("Total Revenue",    f"${df['Total'].sum():,.0f}")
    c3.metric("Avg. Transaction", f"${df['Total'].mean():,.2f}")
    c4.metric("Avg. Rating",      f"{df['Rating'].mean():.2f} / 10")

    st.markdown("<br>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["First 5 Rows", "Data Types & Nulls", "Descriptive Statistics"])

    with tab1:
        st.dataframe(df.head(10), use_container_width=True)

    with tab2:
        info_df = pd.DataFrame({
            "Column":     df.columns,
            "Dtype":      df.dtypes.values,
            "Non-Null":   df.notnull().sum().values,
            "Null Count": df.isnull().sum().values,
            "Unique":     df.nunique().values,
        })
        st.dataframe(info_df, use_container_width=True, hide_index=True)
        insight("The dataset has <strong>zero null values</strong> across all 17 columns — no imputation needed. Gross margin percentage is constant (4.76%) and can be excluded from further analysis.")

    with tab3:
        st.dataframe(df.describe().round(3), use_container_width=True)
        insight("1,000 complete records. Sales totals range from $10.68 to $1,042.65 (mean $322.97). Ratings are roughly symmetric around 6.97 / 10.")

# ══════════════════════════════════════════════════════════════════════════════
# UNIVARIATE
# ══════════════════════════════════════════════════════════════════════════════
elif section_choice == "Univariate Analysis":
    section("Categorical Distributions")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("##### Branch Distribution")
        fig, ax = plt.subplots(figsize=(5, 3.5))
        counts = df["Branch"].value_counts()
        bars = ax.bar(counts.index, counts.values, color=PALETTE[:3], width=0.5, edgecolor="white", linewidth=1.2)
        ax.bar_label(bars, padding=4, fontsize=9, color=PALETTE[0])
        ax.set_xlabel("Branch")
        ax.set_ylabel("Count")
        fig_show(fig)

    with col2:
        st.markdown("##### Customer Type")
        fig, ax = plt.subplots(figsize=(5, 3.5))
        counts = df["Customer type"].value_counts()
        wedges, texts, autotexts = ax.pie(
            counts, labels=counts.index, autopct="%1.1f%%",
            colors=PALETTE[:2], startangle=140,
            wedgeprops=dict(linewidth=2, edgecolor="white"),
        )
        for t in autotexts: t.set_fontsize(10)
        fig_show(fig)

    col3, col4 = st.columns(2)
    with col3:
        st.markdown("##### Payment Method")
        fig, ax = plt.subplots(figsize=(5, 3.5))
        counts = df["Payment"].value_counts()
        ax.barh(counts.index, counts.values, color=PALETTE[2:5], edgecolor="white", height=0.5)
        ax.bar_label(ax.containers[0], padding=4, fontsize=9)
        ax.set_xlabel("Count")
        fig_show(fig)

    with col4:
        st.markdown("##### Gender Split")
        fig, ax = plt.subplots(figsize=(5, 3.5))
        counts = df["Gender"].value_counts()
        ax.bar(counts.index, counts.values, color=[PALETTE[1], PALETTE[2]], width=0.45, edgecolor="white")
        ax.bar_label(ax.containers[0], padding=4, fontsize=9)
        ax.set_xlabel("Gender")
        ax.set_ylabel("Count")
        fig_show(fig)

    insight("Branch sales are nearly <strong>equally distributed</strong> (A, B, C each ~33%). Members vs Normal customers are also balanced. Ewallet is the most used payment method, closely followed by Cash and Credit Card.")

    st.markdown("---")
    section("Numerical Distributions")

    num_col = st.selectbox("Choose a numeric column:", ["Total", "Unit price", "Quantity", "gross income", "cogs", "Rating"])

    col5, col6 = st.columns(2)
    with col5:
        st.markdown(f"##### Distribution of {num_col}")
        fig, ax = plt.subplots(figsize=(5.5, 3.8))
        sns.histplot(df[num_col], kde=True, color=PALETTE[0], ax=ax, bins=25, linewidth=0.8)
        ax.set_xlabel(num_col)
        fig_show(fig)

    with col6:
        st.markdown(f"##### Box Plot — {num_col}")
        fig, ax = plt.subplots(figsize=(5.5, 3.8))
        sns.boxplot(y=df[num_col], color=PALETTE[1], ax=ax, width=0.4, linewidth=1.2,
                    flierprops=dict(marker='o', markerfacecolor=PALETTE[2], markersize=4))
        ax.set_ylabel(num_col)
        fig_show(fig)

    skew_val = df[num_col].skew()
    insight(f"<strong>Skewness of {num_col}:</strong> {skew_val:.3f}. "
            + ("Right-skewed — a few high-value transactions pull the mean upward." if skew_val > 0.5
               else "Left-skewed — most values cluster near the upper end." if skew_val < -0.5
               else "Approximately symmetric distribution."))

    st.markdown("---")
    section("Sales by Month")
    fig, ax = plt.subplots(figsize=(8, 4))
    month_order = ["January", "February", "March"]
    month_counts = df["month"].value_counts().reindex(month_order).dropna()
    ax.bar(month_counts.index, month_counts.values, color=PALETTE[:3], width=0.5, edgecolor="white")
    ax.bar_label(ax.containers[0], padding=4, fontsize=9)
    ax.set_ylabel("Transactions")
    ax.set_xlabel("Month")
    fig_show(fig)
    insight("January records the highest transaction volume, while March is comparatively lower — likely due to the dataset covering early 2019.")

# ══════════════════════════════════════════════════════════════════════════════
# BIVARIATE
# ══════════════════════════════════════════════════════════════════════════════
elif section_choice == "Bivariate Analysis":

    tab_n, tab_c, tab_nc = st.tabs(["Numerical vs Numerical", "Categorical vs Categorical", "Numerical vs Categorical"])

    # ── Num–Num ──────────────────────────────────────────────────────────────
    with tab_n:
        section("Does Cost of Goods Sold Affect Customer Ratings?")
        fig, ax = plt.subplots(figsize=(7, 4.5))
        ax.scatter(df["cogs"], df["Rating"], alpha=0.35, color=PALETTE[0], edgecolors="none", s=28)
        m, b = np.polyfit(df["cogs"].dropna(), df["Rating"].dropna(), 1)
        x_line = np.linspace(df["cogs"].min(), df["cogs"].max(), 200)
        ax.plot(x_line, m * x_line + b, color=PALETTE[2], linewidth=1.8, label="Trend line")
        ax.set_xlabel("COGS ($)")
        ax.set_ylabel("Customer Rating")
        ax.legend()
        fig_show(fig)
        insight("The scatter plot reveals <strong>no meaningful linear relationship</strong> between COGS and customer rating — customers rate based on experience, not spend.")

        st.markdown("---")
        section("Correlation Heatmap")
        fig, ax = plt.subplots(figsize=(8, 5.5))
        num_cols = ["Unit price", "Quantity", "Tax 5%", "Total", "cogs", "gross income", "Rating"]
        corr = df[num_cols].corr()
        mask = np.triu(np.ones_like(corr, dtype=bool))
        cmap = sns.diverging_palette(145, 20, as_cmap=True)
        sns.heatmap(corr, mask=mask, annot=True, fmt=".2f", cmap=cmap,
                    linewidths=0.5, linecolor="#F8F6F1", ax=ax, annot_kws={"size": 9})
        ax.set_title("Correlation Matrix — Numeric Features", pad=12)
        fig_show(fig)
        insight("Total, COGS, Tax, and Gross Income are near-perfectly correlated (all derived from unit price × quantity). Rating shows negligible correlation with all financial metrics.")

    # ── Cat–Cat ──────────────────────────────────────────────────────────────
    with tab_c:
        section("Product Line Preference by Gender")
        fig, ax = plt.subplots(figsize=(9, 4.5))
        ct = pd.crosstab(df["Product line"], df["Gender"])
        ct.plot(kind="bar", ax=ax, color=[PALETTE[1], PALETTE[2]], edgecolor="white", width=0.65)
        ax.set_xlabel("Product Line")
        ax.set_ylabel("Count")
        ax.legend(title="Gender")
        plt.xticks(rotation=35, ha="right")
        fig_show(fig)
        insight("Fashion accessories and Food & Beverages show a female-skewed preference, while Health & Beauty shows the reverse — useful for targeted promotions.")

        st.markdown("---")
        section("Payment Method by City")
        fig, ax = plt.subplots(figsize=(8, 4.5))
        ct2 = pd.crosstab(df["City"], df["Payment"])
        ct2.plot(kind="bar", ax=ax, color=PALETTE[:3], edgecolor="white", width=0.6)
        ax.set_xlabel("City")
        ax.set_ylabel("Count")
        ax.legend(title="Payment")
        plt.xticks(rotation=0)
        fig_show(fig)
        insight("Cash is preferred in Mandalay, while Naypyitaw customers lean toward Ewallets. Credit card usage is relatively uniform across cities.")

    # ── Num–Cat ──────────────────────────────────────────────────────────────
    with tab_nc:
        section("Gross Income by Branch and City")
        fig, ax = plt.subplots(figsize=(7, 4.5))
        sns.barplot(x="Branch", y="gross income", data=df, hue="City",
                    palette=PALETTE[:3], ax=ax, capsize=0.05, errwidth=1.2)
        ax.set_ylabel("Gross Income ($)")
        ax.legend(title="City")
        fig_show(fig)
        insight("Branch C (Naypyitaw) generates the highest average gross income per transaction, suggesting either higher-priced product lines or larger basket sizes.")

        st.markdown("---")
        section("Unit Price by Product Line")
        fig, ax = plt.subplots(figsize=(9, 4.5))
        sns.barplot(x="Product line", y="Unit price", data=df,
                    hue="Product line", palette=PALETTE, ax=ax, dodge=False, legend=False)
        ax.set_xlabel("Product Line")
        ax.set_ylabel("Avg. Unit Price ($)")
        plt.xticks(rotation=35, ha="right")
        fig_show(fig)
        insight("Home & Lifestyle and Fashion Accessories carry the highest average unit prices, while Food & Beverages are the most affordable product line.")

        st.markdown("---")
        section("Total Revenue by Customer Type")
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.boxplot(x="Customer type", y="Total", data=df,
                    palette=[PALETTE[0], PALETTE[1]], ax=ax, width=0.45,
                    flierprops=dict(marker='o', markerfacecolor=PALETTE[2], markersize=4))
        ax.set_ylabel("Transaction Total ($)")
        fig_show(fig)
        insight("Members and Normal customers show similar transaction value distributions — membership status alone does not drive higher spending.")

# ══════════════════════════════════════════════════════════════════════════════
# BUSINESS INSIGHTS
# ══════════════════════════════════════════════════════════════════════════════
elif section_choice == "Business Insights":

    section("Revenue by Product Line")
    fig, ax = plt.subplots(figsize=(9, 4.5))
    rev = df.groupby("Product line")["Total"].sum().sort_values(ascending=True)
    bars = ax.barh(rev.index, rev.values, color=PALETTE[:len(rev)], edgecolor="white", height=0.55)
    ax.bar_label(bars, fmt="$%.0f", padding=5, fontsize=9)
    ax.set_xlabel("Total Revenue ($)")
    fig_show(fig)
    insight("Food & Beverages and Sports & Travel are the top revenue-generating categories, together likely contributing over 35% of total sales.")

    st.markdown("---")
    section("Peak Sales Hours")
    fig, ax = plt.subplots(figsize=(9, 4))
    hour_counts = df["hour"].value_counts().sort_index()
    ax.plot(hour_counts.index, hour_counts.values, color=PALETTE[0], linewidth=2.2, marker="o",
            markersize=5, markerfacecolor=PALETTE[2])
    ax.fill_between(hour_counts.index, hour_counts.values, alpha=0.12, color=PALETTE[0])
    ax.set_xlabel("Hour of Day")
    ax.set_ylabel("Number of Transactions")
    ax.xaxis.set_major_locator(mticker.MultipleLocator(1))
    fig_show(fig)
    insight("Peak footfall occurs at <strong>10 AM, 1 PM, and 7 PM</strong> — morning shoppers, lunch-hour traffic, and post-work visits drive the busiest periods. Staffing and promotions should be aligned accordingly.")

    st.markdown("---")
    section("Rating Distribution by Product Line")
    fig, ax = plt.subplots(figsize=(9, 4.5))
    sns.boxplot(x="Product line", y="Rating", data=df, palette=PALETTE, ax=ax, width=0.5,
                flierprops=dict(marker='o', markersize=4, markerfacecolor=PALETTE[2]))
    plt.xticks(rotation=35, ha="right")
    ax.set_ylabel("Customer Rating")
    fig_show(fig)
    insight("Ratings are broadly consistent across product lines (median ~7). Food & Beverages has a slightly higher median rating, suggesting a satisfying in-store experience for grocery shoppers.")

    st.markdown("---")
    col_a, col_b = st.columns(2)
    with col_a:
        section("Gross Income by Payment Method")
        fig, ax = plt.subplots(figsize=(5, 3.8))
        sns.barplot(x="Payment", y="gross income", data=df,
                    palette=PALETTE[:3], ax=ax, capsize=0.06, errwidth=1.2)
        ax.set_ylabel("Avg. Gross Income ($)")
        ax.set_xlabel("Payment Method")
        plt.xticks(rotation=15, ha="right")
        fig_show(fig)

    with col_b:
        section("Transaction Count by City")
        fig, ax = plt.subplots(figsize=(5, 3.8))
        counts = df["City"].value_counts()
        ax.bar(counts.index, counts.values, color=PALETTE[:3], width=0.5, edgecolor="white")
        ax.bar_label(ax.containers[0], padding=4, fontsize=9)
        ax.set_ylabel("Transactions")
        fig_show(fig)

    insight("Naypyitaw leads in average gross income per payment regardless of method. Credit card users yield marginally higher gross income, potentially due to larger basket sizes.")

    st.markdown("---")
    st.markdown("### Key Takeaways")
    st.markdown("""
| Finding | Detail |
|---|---|
| Revenue Leaders | Food & Beverages, Sports & Travel top total revenue |
| Peak Hours | 10 AM, 1 PM, 7 PM — align promotions and staffing here |
| Top Branch | Branch C (Naypyitaw) — highest average gross income |
| Payment Mix | Ewallet most popular; Credit Card correlates with higher spend |
| Gender Preference | Fashion Accessories skews Female; Health & Beauty skews Male |
| Rating Insight | No correlation between spend and rating — experience matters more |
    """)
