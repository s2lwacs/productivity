import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# إ الصفحة
st.set_page_config(page_title="مؤشرات الإنتاجية", layout="wide")

PASTEL_COLORS = ['#A8E6CF', '#DCEDC1', '#FFD3B6', '#FFAAA5', '#FF8B94']

# البيانات
np.random.seed(42)
days = pd.date_range(start='2026-01-01', periods=100)

sleep_hours = np.random.normal(7.5, 1.5, 100)
social_media = np.random.normal(4, 1.5, 100) - (sleep_hours - 7) * 0.4
productivity = (sleep_hours * 0.8) - (social_media * 0.7) + np.random.normal(5, 1, 100)

sleep_hours = np.clip(sleep_hours, 4, 12)
social_media = np.clip(social_media, 0.5, 9)
productivity = np.clip(productivity, 1, 10)

df = pd.DataFrame({
    'التاريخ': days,
    'ساعات النوم': sleep_hours,
    'استخدام السوشال ميديا (ساعات)': social_media,
    'مستوى الإنتاجية (1-10)': productivity
})

df.fillna(df.mean(numeric_only=True), inplace=True)

#فلاتر
st.sidebar.header("🔎 الفلاتر")

sleep_range = st.sidebar.slider(
    "ساعات النوم",
    float(df['ساعات النوم'].min()),
    float(df['ساعات النوم'].max()),
    (float(df['ساعات النوم'].min()), float(df['ساعات النوم'].max()))
)

social_range = st.sidebar.slider(
    "السوشال ميديا (ساعات)",
    float(df['استخدام السوشال ميديا (ساعات)'].min()),
    float(df['استخدام السوشال ميديا (ساعات)'].max()),
    (float(df['استخدام السوشال ميديا (ساعات)'].min()), float(df['استخدام السوشال ميديا (ساعات)'].max()))
)

#  الفلاتر
filtered_df = df[
    (df['ساعات النوم'] >= sleep_range[0]) & (df['ساعات النوم'] <= sleep_range[1]) &
    (df['استخدام السوشال ميديا (ساعات)'] >= social_range[0]) & (df['استخدام السوشال ميديا (ساعات)'] <= social_range[1])
]


# الواجهة
st.markdown("<h2 style='text-align: center; color: #555;'>(لوحة تحليل الإنتاجية</h2>", unsafe_allow_html=True)
st.markdown("---")

# KPIs
col1, col2, col3 = st.columns(3)
col1.metric("متوسط الإنتاجية", f"{filtered_df['مستوى الإنتاجية (1-10)'].mean():.1f}")
col2.metric("متوسط النوم", f"{filtered_df['ساعات النوم'].mean():.1f} ساعة")
col3.metric("متوسط السوشال ميديا", f"{filtered_df['استخدام السوشال ميديا (ساعات)'].mean():.1f} ساعة")

st.markdown("---")


# الرسوم البيانية
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.markdown("#### السوشال ميديا vs الإنتاجية")
    fig1 = px.scatter(
        filtered_df,
        x='استخدام السوشال ميديا (ساعات)',
        y='مستوى الإنتاجية (1-10)',
        trendline="ols",
        color_discrete_sequence=[PASTEL_COLORS[3]]
    )
    fig1.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig1, use_container_width=True)

with col_chart2:
    st.markdown("#### النوم vs الإنتاجية")
    fig2 = px.scatter(
        filtered_df,
        x='ساعات النوم',
        y='مستوى الإنتاجية (1-10)',
        trendline="ols",
        color_discrete_sequence=[PASTEL_COLORS[0]]
    )
    fig2.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig2, use_container_width=True)
# الارتباط
st.markdown("#### 📊 تأثير العوامل على الإنتاجية )")

corr = filtered_df[['ساعات النوم', 'استخدام السوشال ميديا (ساعات)', 'مستوى الإنتاجية (1-10)']].corr()

corr_prod = corr['مستوى الإنتاجية (1-10)'].drop('مستوى الإنتاجية (1-10)')

corr_df = corr_prod.reset_index()
corr_df.columns = ['العامل', 'قوة الارتباط']

# حجم النقطة حسب قوة العلاقة
corr_df['الحجم'] = corr_df['قوة الارتباط'].abs() * 50 + 10

fig = px.scatter(
    corr_df,
    x='العامل',
    y='قوة الارتباط',
    size='الحجم',
    color='قوة الارتباط',
    text='قوة الارتباط',
    color_continuous_scale=['#FF8B94', '#F9F9F9', '#A8E6CF']
)

fig.update_traces(texttemplate='%{text:.2f}', textposition='top center')

fig.update_layout(
    xaxis_title="العوامل",
    yaxis_title="نوع وقوة العلاقة مع الإنتاجية",
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    coloraxis_showscale=False
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("### 💡 نصائح لتحسين نمط حياتك")
st.markdown("""
<style>

.card-container {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 15px;
}

.card {
    padding: 18px;
    border-radius: 15px;
    background: rgba(255, 255, 255, 0.06);
    border: 1px solid rgba(150,150,150,0.2);
    backdrop-filter: blur(8px);
    transition: all 0.3s ease;
    font-size: 15px;
    line-height: 1.8;
}

.card:hover {
    transform: translateY(-6px) scale(1.02);
    box-shadow: 0px 8px 20px rgba(0,0,0,0.15);
}

.card-title {
    font-weight: bold;
    margin-bottom: 8px;
    font-size: 16px;
}

</style>

<div class="card-container">

<div class="card">
<div class="card-title">🟡 السوشال ميديا</div>
قلل الاستخدام خاصة قبل النوم لتحسين جودة النوم.
</div>

<div class="card">

<div class="card-title">🟢 إدارة الوقت</div>
قسم يومك بين العمل والراحة بشكل متوازن.
</div>

<div class="card">

<div class="card-title">🟡 التركيز</div>
خذ فواصل قصيرة أثناء العمل لزيادة الإنتاجية.
</div>

<div class="card">

<div class="card-title">🟢 الروتين</div>
حافظ على روتين يومي ثابت لتحسين الاستقرار.
</div>

</div>
""", unsafe_allow_html=True)

#name
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray;'>✨ تصميم بواسطة سلوى الحربي</p>",
    unsafe_allow_html=True
)
