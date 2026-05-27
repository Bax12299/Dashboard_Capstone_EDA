import streamlit as st
import pandas as pd
import numpy as np
import ast
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter
from itertools import combinations

# CONFIG
st.set_page_config(
    page_title="IT Job Skills Dashboard",
    page_icon="■",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>

/* App shell & root background */
html, body { background-color: #ffffff !important; color: #1a1a2e !important; }
.stApp, [data-testid="stAppViewContainer"] { background-color: #ffffff !important; }
.main, [data-testid="stMain"], [data-testid="block-container"] {
    background-color: #ffffff !important;
    color: #1a1a2e !important;
}

/* ALL text elements forced dark */
p, span, div, li, ul, ol, label, h1, h2, h3, h4, h5, h6,
.stMarkdown, .stText, [data-testid="stMarkdownContainer"],
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] span {
    color: #1a1a2e !important;
    font-family: 'Segoe UI', sans-serif;
}

/* ── Sidebar ── */
[data-testid="stSidebar"],
[data-testid="stSidebar"] > div {
    background-color: #f0f4ff !important;
    border-right: 2px solid #c7d2fe;
}
[data-testid="stSidebar"] * { color: #1a1a2e !important; }
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stSlider label,
[data-testid="stSidebar"] .stMultiSelect label { color: #1a1a2e !important; font-weight: 600; }

/* ── Metric cards ── */
[data-testid="metric-container"] {
    background: linear-gradient(135deg, #f8faff 0%, #eef2ff 100%) !important;
    border: 1px solid #c7d2fe;
    border-radius: 12px;
    padding: 16px 20px;
    box-shadow: 0 2px 8px rgba(99,102,241,0.08);
}
[data-testid="metric-container"] label,
[data-testid="metric-container"] [data-testid="stMetricLabel"],
[data-testid="metric-container"] [data-testid="stMetricLabel"] p {
    color: #6366f1 !important;
    font-weight: 600 !important;
    font-size: 0.8rem !important;
}
[data-testid="metric-container"] [data-testid="stMetricValue"],
[data-testid="metric-container"] [data-testid="stMetricValue"] div {
    color: #1a1a2e !important;
    font-size: 1.6rem !important;
    font-weight: 700 !important;
}

/* ── Tabs ── */
[data-testid="stTabs"] [data-baseweb="tab-list"] {
    background-color: #f8faff !important;
    border-radius: 10px;
    padding: 4px;
}
[data-baseweb="tab"] { color: #6366f1 !important; font-weight: 600 !important; }
[data-baseweb="tab"][aria-selected="true"] {
    background-color: #eef2ff !important;
    border-bottom: 3px solid #6366f1 !important;
    color: #4338ca !important;
}
[data-baseweb="tab-panel"] { background-color: #ffffff !important; }

/* ── Selectbox / Multiselect / Dropdown ── */
[data-baseweb="select"] { background-color: #f8faff !important; }
[data-baseweb="select"] * { color: #1a1a2e !important; }
[data-baseweb="popover"] { background-color: #ffffff !important; }
[data-baseweb="popover"] * { color: #1a1a2e !important; }
[data-baseweb="menu"] { background-color: #ffffff !important; }
[data-baseweb="menu"] li { color: #1a1a2e !important; }
[data-baseweb="tag"] { background-color: #eef2ff !important; }
[data-baseweb="tag"] span { color: #4338ca !important; }

/* Selectbox & multiselect label */
.stSelectbox label, .stMultiSelect label, .stSlider label, .stTextArea label {
    color: #1a1a2e !important;
    font-weight: 600 !important;
}

/* Input textarea */
.stTextArea textarea {
    background-color: #f8faff !important;
    color: #1a1a2e !important;
    border: 1px solid #c7d2fe !important;
}

/* Slider */
[data-testid="stSlider"] * { color: #1a1a2e !important; }

/* ── Dataframe / Table ── */
/* Streamlit wraps dataframes in an iframe with its own color-scheme.
   The only reliable fix is to inject color-scheme:light on the iframe
   and patch the container background. Row text comes from the canvas
   renderer so we cannot CSS-target it - instead we rely on color-scheme. */
[data-testid="stDataFrame"] { background-color: #ffffff !important; }
[data-testid="stDataFrame"] > div { background-color: #ffffff !important; }
[data-testid="stDataFrame"] iframe {
    color-scheme: light !important;
    background-color: #ffffff !important;
}

/* ── Captions & info ── */
.stCaption, [data-testid="stCaptionContainer"] { color: #6b7280 !important; }
.stInfo { background-color: #eff6ff !important; color: #1e40af !important; }
.stWarning { background-color: #fffbeb !important; color: #92400e !important; }

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    padding: 8px 20px !important;
    transition: opacity 0.2s;
}
.stButton > button:hover { opacity: 0.88 !important; }
.stButton > button * { color: white !important; }

/* ── Section headers ── */
.section-header {
    background: linear-gradient(90deg, #6366f1 0%, #8b5cf6 100%);
    color: white !important;
    padding: 10px 20px 10px 16px;
    border-radius: 8px;
    font-size: 0.92rem;
    font-weight: 700;
    margin: 24px 0 14px 0;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    border-left: 4px solid #c4b5fd;
    box-shadow: 0 2px 10px rgba(99,102,241,0.18);
}

/* ── Insight cards ── */
.insight-card {
    background: #fffbeb !important;
    border-left: 4px solid #f59e0b;
    border-radius: 8px;
    padding: 14px 18px;
    margin: 8px 0;
    color: #1a1a2e !important;
    font-size: 0.91rem;
    line-height: 1.6;
}
.insight-card * { color: #1a1a2e !important; }
.insight-card b { color: #92400e !important; }

/* ── Tag pills ── */
.skill-pill {
    display: inline-block;
    background: #eef2ff !important;
    color: #4338ca !important;
    border: 1px solid #c7d2fe;
    border-radius: 20px;
    padding: 3px 12px;
    margin: 3px;
    font-size: 0.82rem;
    font-weight: 500;
}

/* ── Dashboard title ── */
.dashboard-title {
    color: #1a1a2e !important;
    font-size: 2rem;
    font-weight: 800;
    letter-spacing: -0.5px;
    border-left: 5px solid #6366f1;
    padding-left: 14px;
    margin-bottom: 4px;
}
.dashboard-sub { color: #6b7280 !important; padding-left: 19px; }

/* ── Divider ── */
hr { border-color: #e0e7ff !important; }

/* ── Selectbox & slider ── */
[data-baseweb="select"] { border-radius: 8px !important; }
.stSlider [data-baseweb="slider"] { color: #6366f1; }

/* ── Divider ── */
hr { border-color: #e0e7ff; }

/* ── Title ── */
.dashboard-title {
    font-size: 2rem;
    font-weight: 800;
    color: #1a1a2e;
    letter-spacing: -0.5px;
}
.dashboard-sub {
    color: #6b7280;
    font-size: 0.95rem;
    margin-top: -8px;
}
</style>
""", unsafe_allow_html=True)


# DATA LOADING
@st.cache_data
def load_data():
    df = pd.read_csv("cleaned_combined_jobs_v4.csv")

    def parse_skills(s):
        try:
            return ast.literal_eval(s)
        except:
            return []

    df['skills_parsed'] = df['skills_list'].apply(parse_skills)
    df['n_skills'] = df['skills_parsed'].apply(len)
    df['complexity'] = df['n_skills'].apply(
        lambda x: 'Low (≤5)' if x <= 5 else ('Medium (6–10)' if x <= 10 else 'High (>10)')
    )
    return df


def render_table(df, max_rows=None, truncate_cols=None):
    if max_rows:
        df = df.head(max_rows).copy()
    else:
        df = df.copy()

    if truncate_cols:
        for col in truncate_cols:
            if col in df.columns:
                df[col] = df[col].astype(str).apply(
                    lambda x: x[:80] + '...' if len(x) > 80 else x
                )
    headers = ''.join(f'<th>{col}</th>' for col in df.columns)
    rows = ''
    for i, (_, row) in enumerate(df.iterrows()):
        bg = '#f8faff' if i % 2 == 0 else '#ffffff'
        cells = ''.join(f'<td style="padding:8px 14px;color:#1a1a2e;border-bottom:1px solid #e0e7ff;">{val}</td>'
                        for val in row.values)
        rows += f'<tr style="background:{bg};">{cells}</tr>'

    html = f"""
    <div style="overflow-x:auto; border-radius:10px; border:1px solid #e0e7ff; margin-top:8px;">
    <table style="width:100%;border-collapse:collapse;font-size:0.87rem;font-family:'Segoe UI',sans-serif;">
        <thead>
        <tr style="background:linear-gradient(90deg,#6366f1,#8b5cf6);">
            {headers.replace('<th>', '<th style="padding:10px 14px;text-align:left;font-weight:700;color:white;letter-spacing:0.4px;">')}
        </tr>
        </thead>
        <tbody>{rows}</tbody>
    </table>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

df = load_data()

# Top jobs
TOP_JOBS_LIST = df['job_normalized'].value_counts().head(50).index.tolist()
df_top = df[df['job_normalized'].isin(TOP_JOBS_LIST)]


# SIDEBAR
with st.sidebar:
    st.markdown("## [ Filter & Settings ]")
    st.markdown("---")

    selected_jobs = st.multiselect(
        "Filter Job Role",
        options=TOP_JOBS_LIST,
        default=TOP_JOBS_LIST,
    )

    top_n_skills = st.slider("Top N Skills ditampilkan", 5, 30, 10)
    cooc_threshold = st.slider("Min co-occurrence count", 10, 200, 50)
    freq_threshold = st.slider("Threshold frekuensi skill (%)", 1, 50, 20)

    st.markdown("---")
    st.markdown("### - Dataset Info -")
    st.metric("Total Records", f"{len(df):,}")
    st.metric("Unique Job Roles", f"{df['job_normalized'].nunique():,}")
    all_skills_flat = [s for row in df['skills_parsed'] for s in row]
    st.metric("Unique Skills", f"{len(set(all_skills_flat)):,}")

if not selected_jobs:
    st.warning("Pilih minimal 1 job role di sidebar.")
    st.stop()

df_filtered = df[df['job_normalized'].isin(selected_jobs)]


# HEADER
st.markdown('<div class="dashboard-title">IT Job Skills Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="dashboard-sub">Analisis komprehensif skill, demand pekerjaan, dan rekomendasi karir di industri IT</div>', unsafe_allow_html=True)
st.markdown("---")

# KPI ROW
k1, k2, k3, k4, k5 = st.columns(5)
total_jobs      = len(df_filtered)
avg_skills      = df_filtered['n_skills'].mean()
top_job         = df_filtered['job_normalized'].value_counts().idxmax()
top_job_count   = df_filtered['job_normalized'].value_counts().max()
all_sk          = Counter(s for row in df_filtered['skills_parsed'] for s in row)
top_skill       = all_sk.most_common(1)[0][0] if all_sk else '-'

k1.metric("Total Lowongan", f"{total_jobs:,}")
k2.metric("Rata-rata Skill / Job", f"{avg_skills:.1f}")
k3.metric("Job Terpopuler", top_job.title())
k4.metric("Lowongan Top Job", f"{top_job_count:,}")
k5.metric("Skill Terpopuler", top_skill.title())


# TABS
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Demand & Tren",
    "Analisis Skill",
    "Co-occurrence",
    "Gap & Rekomendasi",
    "Perbandingan Role",
    "Kompleksitas Job",
])


# TAB 1 - DEMAND & TREN
with tab1:
    st.markdown('<div class="section-header">Demand &amp; Tren Pekerjaan IT</div>', unsafe_allow_html=True)

    job_counts = df_filtered['job_normalized'].value_counts().reset_index()
    job_counts.columns = ['job_role', 'count']
    job_counts['percentage'] = (job_counts['count'] / job_counts['count'].sum() * 100).round(2)

    col1, col2 = st.columns([3, 2])

    with col1:
        fig_bar = px.bar(
            job_counts, x='count', y='job_role', orientation='h',
            color='count', color_continuous_scale='Blues',
            text='count', title='Jumlah Lowongan per Job Role',
            labels={'count': 'Jumlah Lowongan', 'job_role': 'Job Role'}
        )
        fig_bar.update_traces(textposition='outside')
        fig_bar.update_layout(
            plot_bgcolor='white', paper_bgcolor='white',
            font_color='#1a1a2e', showlegend=False,
            yaxis={'categoryorder': 'total ascending'},
            coloraxis_showscale=False,
            margin=dict(l=10, r=20, t=40, b=20)
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    with col2:
        fig_pie = px.pie(
            job_counts, values='count', names='job_role',
            title='Distribusi % Job Role',
            color_discrete_sequence=px.colors.sequential.Blues_r,
            hole=0.4
        )
        fig_pie.update_layout(
            paper_bgcolor='white', font_color='#1a1a2e',
            margin=dict(l=10, r=10, t=40, b=20),
            legend=dict(font=dict(size=10))
        )
        fig_pie.update_traces(textinfo='percent', textfont_size=11)
        st.plotly_chart(fig_pie, use_container_width=True)

    # Top 3 + insights
    st.markdown('<div class="section-header">Insight Otomatis</div>', unsafe_allow_html=True)
    top3 = job_counts.head(3)
    top3_pct = job_counts.head(3)['percentage'].sum()
    most_pct  = job_counts.iloc[0]['percentage']
    skewed = "Ya, sangat skewed" if most_pct > 30 else "Relatif seimbang"

    ic1, ic2 = st.columns(2)
    with ic1:
        st.markdown(f"""
        <div class="insight-card"><b>[ Top 3 ] Job Role Paling Dicari:</b><br>
        {' → '.join([f"<b>{r['job_role'].title()}</b> ({r['count']:,})" for _, r in top3.iterrows()])}<br>
        Ketiganya mencakup <b>{top3_pct:.1f}%</b> dari total dataset yang dipilih.
        </div>""", unsafe_allow_html=True)

    with ic2:
        st.markdown(f"""
        <div class="insight-card"><b>[ Distribusi ] Apakah Seimbang?</b><br>
        Job terbesar (<b>{job_counts.iloc[0]['job_role'].title()}</b>) menguasai
        <b>{most_pct:.1f}%</b> dari total lowongan.<br>
        Kesimpulan: <b>{skewed}</b>
        </div>""", unsafe_allow_html=True)

    st.markdown("#### Tabel Detail")
    render_table(job_counts.rename(columns={'job_role': 'Job Role', 'count': 'Jumlah', 'percentage': '%'}))


# TAB 2 - ANALISIS SKILL
with tab2:
    st.markdown('<div class="section-header">Analisis Skill Paling Dibutuhkan</div>', unsafe_allow_html=True)

    all_skills_ctr = Counter(s for row in df_filtered['skills_parsed'] for s in row)
    total_postings  = len(df_filtered)

    # Top N overall
    top_skills_df = pd.DataFrame(all_skills_ctr.most_common(top_n_skills), columns=['skill', 'count'])
    top_skills_df['freq_%'] = (top_skills_df['count'] / total_postings * 100).round(1)

    col1, col2 = st.columns([3, 2])
    with col1:
        fig_skill = px.bar(
            top_skills_df, x='freq_%', y='skill', orientation='h',
            color='freq_%', color_continuous_scale='Purples',
            text='freq_%', title=f'Top {top_n_skills} Skill - Frekuensi (%)',
            labels={'freq_%': 'Frekuensi (%)', 'skill': 'Skill'}
        )
        fig_skill.update_traces(texttemplate='%{text}%', textposition='outside')
        fig_skill.update_layout(
            plot_bgcolor='white', paper_bgcolor='white', font_color='#1a1a2e',
            yaxis={'categoryorder': 'total ascending'},
            coloraxis_showscale=False,
            margin=dict(l=10, r=20, t=40, b=20)
        )
        st.plotly_chart(fig_skill, use_container_width=True)

    with col2:
        above_thresh = top_skills_df[top_skills_df['freq_%'] >= freq_threshold]
        avg_sk = df_filtered['n_skills'].mean()

        st.metric("Avg Skill per Posting", f"{avg_sk:.1f}")
        st.metric(f"Skill dengan frekuensi ≥{freq_threshold}%", f"{len(above_thresh)} skill")
        st.markdown(f"**Skill di atas threshold ({freq_threshold}%):**")
        pills_html = "".join([f'<span class="skill-pill">{r["skill"]}</span>' for _, r in above_thresh.iterrows()])
        st.markdown(pills_html, unsafe_allow_html=True)

    # Skill per job heatmap
    st.markdown('<div class="section-header">Heatmap Skill × Job Role</div>', unsafe_allow_html=True)

    TOP_SKILL_HEATMAP = 15
    top_skill_names = [s for s, _ in all_skills_ctr.most_common(TOP_SKILL_HEATMAP)]

    heatmap_data = []
    for job in selected_jobs:
        mask = df_filtered['job_normalized'] == job
        ctr  = Counter(s for row in df_filtered[mask]['skills_parsed'] for s in row)
        tot  = mask.sum()
        for sk in top_skill_names:
            heatmap_data.append({'Job': job.title(), 'Skill': sk, 'Freq%': round(ctr.get(sk, 0) / tot * 100, 1)})

    hm_df = pd.DataFrame(heatmap_data).pivot(index='Skill', columns='Job', values='Freq%').fillna(0)

    fig_hm = px.imshow(
        hm_df, color_continuous_scale='Blues', aspect='auto',
        title='Frekuensi Skill per Job Role (%)',
        labels=dict(color='Freq%')
    )
    fig_hm.update_layout(paper_bgcolor='white', font_color='#1a1a2e',
                         margin=dict(l=10, r=10, t=40, b=20))
    st.plotly_chart(fig_hm, use_container_width=True)

    # Skill per job - select
    st.markdown('<div class="section-header">Top Skill untuk Job Spesifik</div>', unsafe_allow_html=True)
    chosen_job = st.selectbox("Pilih Job Role:", selected_jobs, key='tab2_job')
    mask_j = df_filtered['job_normalized'] == chosen_job
    ctr_j  = Counter(s for row in df_filtered[mask_j]['skills_parsed'] for s in row)
    tot_j  = mask_j.sum()
    df_j   = pd.DataFrame(ctr_j.most_common(top_n_skills), columns=['skill', 'count'])
    df_j['freq_%'] = (df_j['count'] / tot_j * 100).round(1)

    fig_j = px.bar(df_j, x='skill', y='freq_%', color='freq_%',
                   color_continuous_scale='Teal', text='freq_%',
                   title=f'Top {top_n_skills} Skill - {chosen_job.title()}',
                   labels={'freq_%': 'Frekuensi (%)', 'skill': 'Skill'})
    fig_j.update_traces(texttemplate='%{text}%', textposition='outside')
    fig_j.update_layout(plot_bgcolor='white', paper_bgcolor='white',
                        font_color='#1a1a2e', coloraxis_showscale=False,
                        margin=dict(l=10, r=10, t=40, b=20))
    st.plotly_chart(fig_j, use_container_width=True)


# TAB 3 - CO-OCCURRENCE
with tab3:
    st.markdown('<div class="section-header">Skill Co-occurrence &amp; Relasi</div>', unsafe_allow_html=True)

    @st.cache_data
    def compute_cooccurrence(jobs_tuple):
        df_co = df[df['job_normalized'].isin(jobs_tuple)]
        pair_ctr = Counter()
        skill_ctr = Counter()
        for row in df_co['skills_parsed']:
            skill_ctr.update(row)
            for a, b in combinations(sorted(set(row)), 2):
                pair_ctr[(a, b)] += 1
        return pair_ctr, skill_ctr

    pair_ctr, skill_ctr_co = compute_cooccurrence(tuple(selected_jobs))

    # Top pairs
    top_pairs = pd.DataFrame(
        [(a, b, c) for (a, b), c in pair_ctr.most_common(50) if c >= cooc_threshold],
        columns=['Skill A', 'Skill B', 'Co-occurrence']
    )

    if top_pairs.empty:
        st.warning(f"Tidak ada pasangan skill dengan co-occurrence ≥ {cooc_threshold}. Coba turunkan threshold di sidebar.")
    else:
        col1, col2 = st.columns([3, 2])
        with col1:
            fig_co = px.bar(
                top_pairs.head(20), x='Co-occurrence', y='Skill A',
                orientation='h', color='Co-occurrence',
                color_continuous_scale='Greens', text='Co-occurrence',
                hover_data=['Skill B'],
                title='Top 20 Pasangan Skill (Co-occurrence)',
                labels={'Skill A': 'Skill Utama'}
            )
            fig_co.update_traces(textposition='outside')
            fig_co.update_layout(
                plot_bgcolor='white', paper_bgcolor='white',
                font_color='#1a1a2e', coloraxis_showscale=False,
                yaxis={'categoryorder': 'total ascending'},
                margin=dict(l=10, r=20, t=40, b=20)
            )
            st.plotly_chart(fig_co, use_container_width=True)

        with col2:
            st.markdown("#### Tabel Co-occurrence")
            render_table(top_pairs, max_rows=15)

    # Conditional probability
    st.markdown('<div class="section-header">Conditional Probability - P(B | A)</div>', unsafe_allow_html=True)
    st.caption("Probabilitas kemunculan Skill B jika Skill A ada dalam satu posting")

    top20_skills = [s for s, _ in skill_ctr_co.most_common(20)]
    skill_a = st.selectbox("Pilih Skill A:", top20_skills, key='skill_a')

    cond_probs = []
    for (a, b), cnt in pair_ctr.items():
        if a == skill_a or b == skill_a:
            other = b if a == skill_a else a
            prob  = cnt / skill_ctr_co[skill_a] * 100
            cond_probs.append({'Skill B': other, 'P(B|A) %': round(prob, 1), 'Co-count': cnt})

    if cond_probs:
        cond_df = pd.DataFrame(cond_probs).sort_values('P(B|A) %', ascending=False).head(15)
        fig_cond = px.bar(
            cond_df, x='Skill B', y='P(B|A) %', color='P(B|A) %',
            color_continuous_scale='Oranges', text='P(B|A) %',
            title=f'P(Skill B | {skill_a}) - Top 15'
        )
        fig_cond.update_traces(texttemplate='%{text}%', textposition='outside')
        fig_cond.update_layout(
            plot_bgcolor='white', paper_bgcolor='white',
            font_color='#1a1a2e', coloraxis_showscale=False,
            margin=dict(l=10, r=10, t=40, b=20)
        )
        st.plotly_chart(fig_cond, use_container_width=True)
    else:
        st.info("Tidak ada data untuk skill ini.")


# TAB 4 - GAP & REKOMENDASI
with tab4:
    st.markdown('<div class="section-header">Gap Skill &amp; Rekomendasi</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])
    with col1:
        target_job = st.selectbox("Target Job Role:", selected_jobs, key='gap_job')
        user_input  = st.text_area(
            "Masukkan skill yang kamu punya (pisahkan dengan koma):",
            placeholder="python, sql, excel, tableau",
            height=120
        )
        analyze_btn = st.button("Analisis Gap")

    # Precompute job skill frequencies
    mask_tgt  = df_filtered['job_normalized'] == target_job
    ctr_tgt   = Counter(s for row in df_filtered[mask_tgt]['skills_parsed'] for s in row)
    tot_tgt   = mask_tgt.sum()
    job_skills_df = pd.DataFrame(
        [(s, c, round(c / tot_tgt * 100, 1)) for s, c in ctr_tgt.most_common(30)],
        columns=['skill', 'count', 'freq_%']
    )

    with col2:
        if analyze_btn and user_input.strip():
            user_skills = set(s.strip().lower() for s in user_input.split(',') if s.strip())
            job_req     = set(job_skills_df['skill'].tolist())

            matched  = user_skills & job_req
            gap      = job_req - user_skills
            coverage = len(matched) / len(job_req) * 100 if job_req else 0

            m1, m2, m3 = st.columns(3)
            m1.metric("Skill Match", len(matched))
            m2.metric("Skill Gap", len(gap))
            m3.metric("Coverage", f"{coverage:.1f}%")

            # Gap skills ranked by frequency
            gap_df = job_skills_df[job_skills_df['skill'].isin(gap)].head(15)
            if not gap_df.empty:
                fig_gap = px.bar(
                    gap_df, x='freq_%', y='skill', orientation='h',
                    color='freq_%', color_continuous_scale='Reds',
                    text='freq_%', title=f'Skill Gap untuk {target_job.title()} (ranked by importance)',
                    labels={'freq_%': 'Demand (%)', 'skill': 'Skill yang belum dimiliki'}
                )
                fig_gap.update_traces(texttemplate='%{text}%', textposition='outside')
                fig_gap.update_layout(
                    plot_bgcolor='white', paper_bgcolor='white',
                    font_color='#1a1a2e', coloraxis_showscale=False,
                    yaxis={'categoryorder': 'total ascending'},
                    margin=dict(l=10, r=10, t=40, b=20)
                )
                st.plotly_chart(fig_gap, use_container_width=True)

            # Skill Rekomendasi berdasarkan co-occurrence
            st.markdown("#### Rekomendasi Skill Berikutnya")
            rec_scores = Counter()
            for us in user_skills:
                for (a, b), cnt in pair_ctr.items():
                    if a == us or b == us:
                        other = b if a == us else a
                        if other not in user_skills:
                            rec_scores[other] += cnt

            if rec_scores:
                rec_df = pd.DataFrame(rec_scores.most_common(10), columns=['Skill', 'Score'])
                rec_df['Dibutuhkan Job?'] = rec_df['Skill'].apply(lambda x: 'Ya' if x in job_req else 'Tidak')
                render_table(rec_df)
                st.caption("Score = total co-occurrence dengan skill yang sudah kamu miliki")
        else:
            st.markdown("#### Top Skill yang Dibutuhkan untuk:")
            st.markdown(f"**{target_job.title()}**")
            fig_req = px.bar(
                job_skills_df.head(15), x='freq_%', y='skill', orientation='h',
                color='freq_%', color_continuous_scale='Blues',
                text='freq_%', title='Skill Requirements',
                labels={'freq_%': 'Demand (%)', 'skill': 'Skill'}
            )
            fig_req.update_traces(texttemplate='%{text}%', textposition='outside')
            fig_req.update_layout(
                plot_bgcolor='white', paper_bgcolor='white',
                font_color='#1a1a2e', coloraxis_showscale=False,
                yaxis={'categoryorder': 'total ascending'},
                margin=dict(l=10, r=10, t=40, b=20)
            )
            st.plotly_chart(fig_req, use_container_width=True)
            st.info("Masukkan skill kamu di kiri untuk melihat gap analysis.")


# TAB 5 - PERBANDINGAN ROLE
with tab5:
    st.markdown('<div class="section-header">Perbandingan Skill Antar Role</div>', unsafe_allow_html=True)

    compare_jobs = st.multiselect(
        "Pilih 2–4 job role untuk dibandingkan:",
        selected_jobs,
        default=selected_jobs[:3] if len(selected_jobs) >= 3 else selected_jobs,
        max_selections=4,
        key='compare_jobs'
    )

    if len(compare_jobs) < 2:
        st.warning("Pilih minimal 2 role untuk perbandingan.")
    else:
        TOP_N_COMPARE = 20
        role_skill_sets = {}
        role_skill_freq = {}

        for job in compare_jobs:
            mask = df_filtered['job_normalized'] == job
            ctr  = Counter(s for row in df_filtered[mask]['skills_parsed'] for s in row)
            role_skill_sets[job] = set(s for s, _ in ctr.most_common(TOP_N_COMPARE))
            role_skill_freq[job] = ctr

        # Jaccard similarity matrix
        jobs_list = compare_jobs
        n = len(jobs_list)
        sim_matrix = np.zeros((n, n))
        for i, j_a in enumerate(jobs_list):
            for j, j_b in enumerate(jobs_list):
                inter = len(role_skill_sets[j_a] & role_skill_sets[j_b])
                union = len(role_skill_sets[j_a] | role_skill_sets[j_b])
                sim_matrix[i][j] = round(inter / union, 3) if union > 0 else 0

        col1, col2 = st.columns(2)
        with col1:
            fig_sim = px.imshow(
                sim_matrix,
                x=[j.title() for j in jobs_list],
                y=[j.title() for j in jobs_list],
                color_continuous_scale='Blues', text_auto=True,
                title='Jaccard Similarity Antar Role',
                zmin=0, zmax=1
            )
            fig_sim.update_layout(paper_bgcolor='white', font_color='#1a1a2e',
                                  margin=dict(l=10, r=10, t=40, b=20))
            st.plotly_chart(fig_sim, use_container_width=True)

        with col2:
            # Overlap & unique
            all_union   = set.union(*role_skill_sets.values())
            all_overlap = set.intersection(*role_skill_sets.values())

            st.markdown("#### Skill Overlap Semua Role")
            if all_overlap:
                pills = "".join([f'<span class="skill-pill">{s}</span>' for s in sorted(all_overlap)])
                st.markdown(pills, unsafe_allow_html=True)
            else:
                st.info("Tidak ada skill yang sama persis di semua role yang dipilih.")

            st.markdown("#### Skill Eksklusif per Role")
            for job in compare_jobs:
                others  = set().union(*[role_skill_sets[j] for j in compare_jobs if j != job])
                excl    = role_skill_sets[job] - others
                if excl:
                    st.markdown(f"**{job.title()}:** " + "".join(
                        [f'<span class="skill-pill">{s}</span>' for s in sorted(excl)]
                    ), unsafe_allow_html=True)
                else:
                    st.markdown(f"**{job.title()}:** *(tidak ada skill eksklusif di top-{TOP_N_COMPARE})*")

        # Radar chart
        st.markdown('<div class="section-header">Radar Chart - Top Shared Skills</div>', unsafe_allow_html=True)
        shared_skills = list(set.union(*role_skill_sets.values()))
        total_counts = Counter()
        for job in compare_jobs:
            total_counts.update(role_skill_freq[job])
        top_radar = [s for s, _ in total_counts.most_common(12) if s in shared_skills]

        fig_radar = go.Figure()
        for job in compare_jobs:
            mask = df_filtered['job_normalized'] == job
            tot  = mask.sum()
            vals = [round(role_skill_freq[job].get(s, 0) / tot * 100, 1) for s in top_radar]
            fig_radar.add_trace(go.Scatterpolar(
                r=vals + [vals[0]], theta=top_radar + [top_radar[0]],
                fill='toself', name=job.title(), opacity=0.7
            ))

        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, max(
                role_skill_freq[j].get(s, 0) / df_filtered[df_filtered['job_normalized']==j].shape[0] * 100
                for j in compare_jobs for s in top_radar
            ) + 5])),
            paper_bgcolor='white', font_color='#1a1a2e',
            title='Perbandingan Frekuensi Skill (%) Antar Role',
            margin=dict(l=40, r=40, t=60, b=40)
        )
        st.plotly_chart(fig_radar, use_container_width=True)


# TAB 6 - KOMPLEKSITAS JOB
with tab6:
    st.markdown('<div class="section-header">Kompleksitas Job Berdasarkan Jumlah Skill</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        # Distribusi kompleksitas
        comp_counts = df_filtered['complexity'].value_counts().reset_index()
        comp_counts.columns = ['Kompleksitas', 'Jumlah']
        order = ['Low (≤5)', 'Medium (6–10)', 'High (>10)']
        comp_counts['Kompleksitas'] = pd.Categorical(comp_counts['Kompleksitas'], categories=order, ordered=True)
        comp_counts = comp_counts.sort_values('Kompleksitas')

        fig_comp = px.bar(
            comp_counts, x='Kompleksitas', y='Jumlah',
            color='Kompleksitas',
            color_discrete_map={'Low (≤5)': '#93c5fd', 'Medium (6–10)': '#6366f1', 'High (>10)': '#1e1b4b'},
            text='Jumlah', title='Distribusi Kompleksitas Job'
        )
        fig_comp.update_traces(textposition='outside')
        fig_comp.update_layout(
            plot_bgcolor='white', paper_bgcolor='white',
            font_color='#1a1a2e', showlegend=False,
            margin=dict(l=10, r=10, t=40, b=20)
        )
        st.plotly_chart(fig_comp, use_container_width=True)

    with col2:
        # Avg skill count per job role
        avg_by_job = df_filtered.groupby('job_normalized')['n_skills'].mean().reset_index()
        avg_by_job.columns = ['Job Role', 'Avg Skills']
        avg_by_job = avg_by_job.sort_values('Avg Skills', ascending=False)

        fig_avg = px.bar(
            avg_by_job, x='Avg Skills', y='Job Role', orientation='h',
            color='Avg Skills', color_continuous_scale='Purples',
            text=avg_by_job['Avg Skills'].round(1),
            title='Rata-rata Jumlah Skill per Job Role',
            labels={'Avg Skills': 'Avg Skill Count', 'Job Role': ''}
        )
        fig_avg.update_traces(textposition='outside')
        fig_avg.update_layout(
            plot_bgcolor='white', paper_bgcolor='white',
            font_color='#1a1a2e', coloraxis_showscale=False,
            yaxis={'categoryorder': 'total ascending'},
            margin=dict(l=10, r=20, t=40, b=20)
        )
        st.plotly_chart(fig_avg, use_container_width=True)

    # Box plot distribusi skill per job
    st.markdown('<div class="section-header">Distribusi Skill Count per Role</div>', unsafe_allow_html=True)
    fig_box = px.box(
        df_filtered, x='job_normalized', y='n_skills',
        color='job_normalized',
        color_discrete_sequence=px.colors.qualitative.Set2,
        title='Sebaran Jumlah Skill per Job Role',
        labels={'n_skills': 'Jumlah Skill', 'job_normalized': 'Job Role'},
        points='outliers'
    )
    fig_box.update_layout(
        plot_bgcolor='white', paper_bgcolor='white',
        font_color='#1a1a2e', showlegend=False,
        xaxis_tickangle=-35,
        margin=dict(l=10, r=10, t=40, b=80)
    )
    st.plotly_chart(fig_box, use_container_width=True)

    # Top most complex jobs
    st.markdown('<div class="section-header">Job Posting dengan Skill Terbanyak</div>', unsafe_allow_html=True)
    top_complex = (
        df_filtered[['job_normalized', 'n_skills', 'skills_list']]
        .sort_values('n_skills', ascending=False)
        .head(10)
        .rename(columns={'job_normalized': 'Job Role', 'n_skills': 'Jumlah Skill', 'skills_list': 'Skills'})
    )
    render_table(top_complex, truncate_cols=['Skills'])

    # Summary metrics
    st.markdown("---")
    c1, c2, c3, c4 = st.columns(4)
    low_pct  = (df_filtered['complexity'] == 'Low (≤5)').mean() * 100
    med_pct  = (df_filtered['complexity'] == 'Medium (6–10)').mean() * 100
    high_pct = (df_filtered['complexity'] == 'High (>10)').mean() * 100
    c1.metric("Low Complexity", f"{low_pct:.1f}%")
    c2.metric("Medium Complexity", f"{med_pct:.1f}%")
    c3.metric("High Complexity", f"{high_pct:.1f}%")
    c4.metric("Median Skill / Job", f"{df_filtered['n_skills'].median():.0f}")


# FOOTER
st.markdown("---")
st.markdown(
    '<div style="text-align:center; color:#9ca3af; font-size:0.82rem;">'
    'IT Job Skills Dashboard'
    '</div>',
    unsafe_allow_html=True
)