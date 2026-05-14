import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

st.set_page_config(
    page_title="Nassau Candy — Profitability Dashboard",
    page_icon="🍫",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1F3864 0%, #2D5AA0 100%);
        padding: 1.5rem 2rem;
        border-radius: 10px;
        margin-bottom: 1.5rem;
    }
    .main-header h1 { color: white; font-size: 1.8rem; margin: 0; font-weight: 600; }
    .main-header p { color: #B5D4F4; font-size: 0.9rem; margin: 0.3rem 0 0 0; }
    .kpi-card {
        background: white;
        border-radius: 10px;
        padding: 1rem 1.2rem;
        border: 1px solid #E0E4EA;
        border-top: 4px solid;
        text-align: center;
    }
    .kpi-value { font-size: 1.6rem; font-weight: 600; margin: 0.3rem 0; }
    .kpi-label { font-size: 0.75rem; color: #666; text-transform: uppercase; letter-spacing: 0.5px; }
    .kpi-trend { font-size: 0.75rem; margin-top: 0.2rem; }
    .section-title {
        font-size: 1rem;
        font-weight: 600;
        color: #1F3864;
        margin: 1rem 0 0.5rem 0;
        padding-bottom: 0.3rem;
        border-bottom: 2px solid #E6F1FB;
    }
    .finding-box {
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 0.8rem;
        border-left: 4px solid;
    }
    .finding-title { font-weight: 600; font-size: 0.85rem; margin-bottom: 0.3rem; }
    .finding-text { font-size: 0.8rem; line-height: 1.5; }
    .rec-box {
        background: #F8FAFF;
        border: 1px solid #E0E4EA;
        border-radius: 8px;
        padding: 0.8rem 1rem;
        margin-bottom: 0.6rem;
    }
    .rec-num {
        background: #1F3864;
        color: white;
        border-radius: 50%;
        width: 22px;
        height: 22px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 0.75rem;
        font-weight: 600;
        margin-right: 0.5rem;
    }
    div[data-testid="stMetricValue"] { font-size: 1.4rem !important; }
    .stSelectbox label { font-weight: 500; color: #1F3864; }
    .stMultiSelect label { font-weight: 500; color: #1F3864; }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_csv("Nassau_Candy_Distributor.csv")
    df['Gross_Margin_Pct'] = (df['Gross Profit'] / df['Sales'] * 100).round(2)
    df['Profit_Per_Unit'] = (df['Gross Profit'] / df['Units']).round(2)
    df['Cost_Ratio_Pct'] = (df['Cost'] / df['Sales'] * 100).round(2)
    df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce')
    return df

df = load_data()

products_df = df.groupby(['Product Name', 'Division']).agg(
    Total_Sales=('Sales', 'sum'),
    Total_Profit=('Gross Profit', 'sum'),
    Total_Units=('Units', 'sum'),
    Total_Cost=('Cost', 'sum')
).reset_index()
products_df['Gross_Margin_Pct'] = (products_df['Total_Profit'] / products_df['Total_Sales'] * 100).round(2)
products_df['Profit_Per_Unit'] = (products_df['Total_Profit'] / products_df['Total_Units']).round(2)
products_df['Cost_Ratio_Pct'] = (products_df['Total_Cost'] / products_df['Total_Sales'] * 100).round(2)
total_sales_all = products_df['Total_Sales'].sum()
total_profit_all = products_df['Total_Profit'].sum()
products_df['Revenue_Contribution'] = (products_df['Total_Sales'] / total_sales_all * 100).round(2)
products_df['Profit_Contribution'] = (products_df['Total_Profit'] / total_profit_all * 100).round(2)

def get_quadrant(row):
    avg_sales = products_df['Total_Sales'].mean()
    if row['Total_Sales'] > avg_sales and row['Gross_Margin_Pct'] > 60:
        return 'Star'
    elif row['Total_Sales'] > avg_sales and row['Gross_Margin_Pct'] <= 60:
        return 'Cash Trap'
    elif row['Total_Sales'] <= avg_sales and row['Gross_Margin_Pct'] > 60:
        return 'Hidden Gem'
    else:
        return 'Dead Weight'

def get_risk(row):
    if row['Gross_Margin_Pct'] < 50:
        return 'HIGH RISK'
    elif row['Gross_Margin_Pct'] < 60:
        return 'WATCH'
    else:
        return 'HEALTHY'

products_df['Quadrant'] = products_df.apply(get_quadrant, axis=1)
products_df['Risk_Flag'] = products_df.apply(get_risk, axis=1)

division_df = df.groupby('Division').agg(
    Total_Sales=('Sales', 'sum'),
    Total_Profit=('Gross Profit', 'sum'),
    Total_Units=('Units', 'sum'),
    Total_Cost=('Cost', 'sum')
).reset_index()
division_df['Gross_Margin_Pct'] = (division_df['Total_Profit'] / division_df['Total_Sales'] * 100).round(2)
division_df['Revenue_Contribution'] = (division_df['Total_Sales'] / division_df['Total_Sales'].sum() * 100).round(2)

region_df = df.groupby('Region').agg(
    Total_Sales=('Sales', 'sum'),
    Total_Profit=('Gross Profit', 'sum'),
).reset_index()
region_df['Gross_Margin_Pct'] = (region_df['Total_Profit'] / region_df['Total_Sales'] * 100).round(2)

NAVY = '#1F3864'
BLUE = '#185FA5'
GREEN = '#3B6D11'
AMBER = '#BA7517'
RED = '#A32D2D'
LIGHT_BLUE = '#E6F1FB'
LIGHT_GREEN = '#EAF3DE'
LIGHT_AMBER = '#FAEEDA'
LIGHT_RED = '#FCEBEB'

DIV_COLORS = {'Chocolate': BLUE, 'Sugar': GREEN, 'Other': AMBER}
REG_COLORS = {'Pacific': BLUE, 'Atlantic': GREEN, 'Interior': AMBER, 'Gulf': RED}
QUAD_COLORS = {'Star': GREEN, 'Hidden Gem': BLUE, 'Cash Trap': AMBER, 'Dead Weight': RED}
RISK_COLORS = {'HEALTHY': GREEN, 'WATCH': AMBER, 'HIGH RISK': RED}

st.markdown("""
<div class="main-header">
    <h1>🍫 Nassau Candy Distributor</h1>
    <p>Profitability Analysis Dashboard &nbsp;·&nbsp; FY 2024 &nbsp;·&nbsp; Prepared by Khushi</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown(f"<h2 style='color:{NAVY};font-size:1rem;margin-bottom:1rem'>Dashboard Filters</h2>", unsafe_allow_html=True)
    
    selected_divisions = st.multiselect(
        "Filter by Division",
        options=df['Division'].unique().tolist(),
        default=df['Division'].unique().tolist()
    )
    
    selected_regions = st.multiselect(
        "Filter by Region",
        options=df['Region'].unique().tolist(),
        default=df['Region'].unique().tolist()
    )
    
    selected_quadrants = st.multiselect(
        "Filter by Quadrant",
        options=['Star', 'Hidden Gem', 'Cash Trap', 'Dead Weight'],
        default=['Star', 'Hidden Gem', 'Cash Trap', 'Dead Weight']
    )
    
    margin_threshold = st.slider(
        "Min Gross Margin %",
        min_value=0, max_value=100, value=0, step=5
    )
    
    st.markdown("---")
    st.markdown(f"<p style='font-size:0.75rem;color:#666'>Data: 10,194 order records<br>13 products · 3 divisions · 4 regions</p>", unsafe_allow_html=True)

df_filtered = df[
    (df['Division'].isin(selected_divisions)) &
    (df['Region'].isin(selected_regions))
]

prod_filtered = products_df[
    (products_df['Division'].isin(selected_divisions)) &
    (products_df['Quadrant'].isin(selected_quadrants)) &
    (products_df['Gross_Margin_Pct'] >= margin_threshold)
]

total_sales = df_filtered['Sales'].sum()
total_profit = df_filtered['Gross Profit'].sum()
total_units = df_filtered['Units'].sum()
gross_margin = (total_profit / total_sales * 100) if total_sales > 0 else 0
high_risk_count = len(prod_filtered[prod_filtered['Risk_Flag'] == 'HIGH RISK'])

page = st.radio(
    "Navigate to",
    ["📊 Product Profitability", "🏭 Division & Region", "📈 Pareto & Cost Analysis", "📋 Executive Summary"],
    horizontal=True
)

st.markdown("---")

if page == "📊 Product Profitability":
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""<div class="kpi-card" style="border-top-color:{BLUE}">
            <div class="kpi-label">Total Sales</div>
            <div class="kpi-value" style="color:{BLUE}">${total_sales:,.0f}</div>
            <div class="kpi-trend" style="color:{GREEN}">All divisions combined</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class="kpi-card" style="border-top-color:{GREEN}">
            <div class="kpi-label">Total Gross Profit</div>
            <div class="kpi-value" style="color:{GREEN}">${total_profit:,.0f}</div>
            <div class="kpi-trend" style="color:{GREEN}">After manufacturing cost</div>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""<div class="kpi-card" style="border-top-color:{AMBER}">
            <div class="kpi-label">Gross Margin %</div>
            <div class="kpi-value" style="color:{AMBER}">{gross_margin:.1f}%</div>
            <div class="kpi-trend" style="color:#666">Company average</div>
        </div>""", unsafe_allow_html=True)
    with col4:
        st.markdown(f"""<div class="kpi-card" style="border-top-color:{RED}">
            <div class="kpi-label">High Risk Products</div>
            <div class="kpi-value" style="color:{RED}">{high_risk_count}</div>
            <div class="kpi-trend" style="color:{RED}">Margin below 50%</div>
        </div>""", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='section-title'>Gross Margin % by Product — Ranked</div>", unsafe_allow_html=True)
        prod_sorted = prod_filtered.sort_values('Gross_Margin_Pct', ascending=True)
        colors = [RISK_COLORS.get(r, BLUE) for r in prod_sorted['Risk_Flag']]
        fig1 = go.Figure(go.Bar(
            x=prod_sorted['Gross_Margin_Pct'],
            y=prod_sorted['Product Name'],
            orientation='h',
            marker_color=colors,
            text=prod_sorted['Gross_Margin_Pct'].apply(lambda x: f'{x:.1f}%'),
            textposition='inside',
            textfont=dict(color='white', size=11)
        ))
        fig1.add_vline(x=65, line_dash="dash", line_color=NAVY, 
                       annotation_text="Target 65%", annotation_position="top right",
                       annotation_font_color=NAVY)
        fig1.update_layout(
            height=420, margin=dict(l=10, r=10, t=10, b=10),
            plot_bgcolor='white', paper_bgcolor='white',
            xaxis=dict(showgrid=False, showticklabels=False, title=''),
            yaxis=dict(title='', tickfont=dict(size=10)),
            showlegend=False
        )
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        st.markdown("<div class='section-title'>Total Gross Profit $ by Product</div>", unsafe_allow_html=True)
        prod_profit = prod_filtered.sort_values('Total_Profit', ascending=True)
        fig2 = go.Figure(go.Bar(
            x=prod_profit['Total_Profit'],
            y=prod_profit['Product Name'],
            orientation='h',
            marker_color=GREEN,
            text=prod_profit['Total_Profit'].apply(lambda x: f'${x:,.0f}'),
            textposition='inside',
            textfont=dict(color='white', size=11)
        ))
        fig2.update_layout(
            height=420, margin=dict(l=10, r=10, t=10, b=10),
            plot_bgcolor='white', paper_bgcolor='white',
            xaxis=dict(showgrid=False, showticklabels=False, title=''),
            yaxis=dict(title='', tickfont=dict(size=10)),
            showlegend=False
        )
        st.plotly_chart(fig2, use_container_width=True)
    
    st.markdown("<div class='section-title'>Product Risk Summary Table</div>", unsafe_allow_html=True)
    
    display_cols = ['Product Name', 'Division', 'Total_Sales', 'Total_Profit', 
                    'Gross_Margin_Pct', 'Profit_Per_Unit', 'Quadrant', 'Risk_Flag']
    display_df = prod_filtered[display_cols].sort_values('Gross_Margin_Pct', ascending=False).copy()
    display_df.columns = ['Product', 'Division', 'Revenue ($)', 'Profit ($)', 
                          'Margin %', 'Profit/Unit', 'Quadrant', 'Status']
    display_df['Revenue ($)'] = display_df['Revenue ($)'].apply(lambda x: f'${x:,.2f}')
    display_df['Profit ($)'] = display_df['Profit ($)'].apply(lambda x: f'${x:,.2f}')
    display_df['Margin %'] = display_df['Margin %'].apply(lambda x: f'{x:.1f}%')
    display_df['Profit/Unit'] = display_df['Profit/Unit'].apply(lambda x: f'${x:.2f}')
    
    def color_status(val):
        if val == 'HIGH RISK':
            return 'background-color: #FCEBEB; color: #791F1F; font-weight: bold'
        elif val == 'WATCH':
            return 'background-color: #FAEEDA; color: #633806; font-weight: bold'
        else:
            return 'background-color: #EAF3DE; color: #27500A; font-weight: bold'
    
    def color_quadrant(val):
        colors_map = {'Star': '#EAF3DE', 'Hidden Gem': '#E6F1FB', 
                      'Cash Trap': '#FAEEDA', 'Dead Weight': '#FCEBEB'}
        return f'background-color: {colors_map.get(val, "white")}'
    
    styled = display_df.style.applymap(color_status, subset=['Status'])\
                              .applymap(color_quadrant, subset=['Quadrant'])
    st.dataframe(styled, use_container_width=True, hide_index=True)

elif page == "🏭 Division & Region":
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""<div class="kpi-card" style="border-top-color:{BLUE}">
            <div class="kpi-label">Divisions</div>
            <div class="kpi-value" style="color:{BLUE}">3</div>
            <div class="kpi-trend" style="color:#666">Chocolate · Sugar · Other</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class="kpi-card" style="border-top-color:{GREEN}">
            <div class="kpi-label">Regions</div>
            <div class="kpi-value" style="color:{GREEN}">4</div>
            <div class="kpi-trend" style="color:#666">Pacific · Atlantic · Interior · Gulf</div>
        </div>""", unsafe_allow_html=True)
    with col3:
        best_div = division_df.loc[division_df['Gross_Margin_Pct'].idxmax()]
        st.markdown(f"""<div class="kpi-card" style="border-top-color:{AMBER}">
            <div class="kpi-label">Best Division Margin</div>
            <div class="kpi-value" style="color:{AMBER}">{best_div['Gross_Margin_Pct']:.1f}%</div>
            <div class="kpi-trend" style="color:#666">{best_div['Division']}</div>
        </div>""", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='section-title'>Total Revenue by Division</div>", unsafe_allow_html=True)
        div_filtered = division_df[division_df['Division'].isin(selected_divisions)]
        fig3 = go.Figure(go.Bar(
            x=div_filtered['Total_Sales'],
            y=div_filtered['Division'],
            orientation='h',
            marker_color=[DIV_COLORS.get(d, BLUE) for d in div_filtered['Division']],
            text=div_filtered['Total_Sales'].apply(lambda x: f'${x:,.0f}'),
            textposition='inside',
            textfont=dict(color='white', size=12)
        ))
        fig3.update_layout(
            height=280, margin=dict(l=10, r=10, t=10, b=10),
            plot_bgcolor='white', paper_bgcolor='white',
            xaxis=dict(showgrid=False, showticklabels=False),
            yaxis=dict(title=''), showlegend=False
        )
        st.plotly_chart(fig3, use_container_width=True)
        
        st.markdown("<div class='section-title'>Gross Margin % by Division</div>", unsafe_allow_html=True)
        fig4 = go.Figure(go.Bar(
            x=div_filtered['Gross_Margin_Pct'],
            y=div_filtered['Division'],
            orientation='h',
            marker_color=[DIV_COLORS.get(d, BLUE) for d in div_filtered['Division']],
            text=div_filtered['Gross_Margin_Pct'].apply(lambda x: f'{x:.1f}%'),
            textposition='inside',
            textfont=dict(color='white', size=12)
        ))
        fig4.add_vline(x=60, line_dash="dash", line_color=RED,
                       annotation_text="Min target 60%", annotation_font_color=RED)
        fig4.update_layout(
            height=280, margin=dict(l=10, r=10, t=10, b=10),
            plot_bgcolor='white', paper_bgcolor='white',
            xaxis=dict(showgrid=False, showticklabels=False, range=[0, 85]),
            yaxis=dict(title=''), showlegend=False
        )
        st.plotly_chart(fig4, use_container_width=True)
    
    with col2:
        st.markdown("<div class='section-title'>Total Sales by Region</div>", unsafe_allow_html=True)
        reg_filtered = region_df[region_df['Region'].isin(selected_regions)].sort_values('Total_Sales', ascending=True)
        fig5 = go.Figure(go.Bar(
            x=reg_filtered['Total_Sales'],
            y=reg_filtered['Region'],
            orientation='h',
            marker_color=[REG_COLORS.get(r, BLUE) for r in reg_filtered['Region']],
            text=reg_filtered['Total_Sales'].apply(lambda x: f'${x:,.0f}'),
            textposition='inside',
            textfont=dict(color='white', size=12)
        ))
        fig5.update_layout(
            height=280, margin=dict(l=10, r=10, t=10, b=10),
            plot_bgcolor='white', paper_bgcolor='white',
            xaxis=dict(showgrid=False, showticklabels=False),
            yaxis=dict(title=''), showlegend=False
        )
        st.plotly_chart(fig5, use_container_width=True)
        
        st.markdown("<div class='section-title'>Revenue Share by Division</div>", unsafe_allow_html=True)
        fig6 = go.Figure(go.Pie(
            labels=div_filtered['Division'],
            values=div_filtered['Total_Sales'],
            hole=0.5,
            marker_colors=[DIV_COLORS.get(d, BLUE) for d in div_filtered['Division']],
            textinfo='label+percent',
            textfont=dict(size=12)
        ))
        fig6.update_layout(
            height=280, margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor='white', showlegend=False
        )
        st.plotly_chart(fig6, use_container_width=True)

elif page == "📈 Pareto & Cost Analysis":
    
    st.markdown("<div class='section-title'>Pareto Analysis — Revenue Concentration by Product</div>", unsafe_allow_html=True)
    
    pareto = prod_filtered.sort_values('Total_Sales', ascending=False).copy()
    pareto['Cumulative_Sales'] = pareto['Total_Sales'].cumsum()
    pareto['Cumulative_Pct'] = (pareto['Cumulative_Sales'] / pareto['Total_Sales'].sum() * 100).round(1)
    
    fig7 = make_subplots(specs=[[{"secondary_y": True}]])
    fig7.add_trace(go.Bar(
        x=pareto['Product Name'],
        y=pareto['Total_Sales'],
        name='Revenue ($)',
        marker_color=BLUE,
        text=pareto['Total_Sales'].apply(lambda x: f'${x:,.0f}'),
        textposition='outside',
        textfont=dict(size=9)
    ), secondary_y=False)
    fig7.add_trace(go.Scatter(
        x=pareto['Product Name'],
        y=pareto['Cumulative_Pct'],
        name='Cumulative %',
        line=dict(color=RED, width=2.5),
        mode='lines+markers',
        marker=dict(size=7, color=RED)
    ), secondary_y=True)
    fig7.add_hline(y=80, line_dash="dash", line_color=NAVY,
                   annotation_text="80% threshold", secondary_y=True)
    fig7.update_layout(
        height=380, margin=dict(l=10, r=10, t=10, b=100),
        plot_bgcolor='white', paper_bgcolor='white',
        legend=dict(orientation='h', y=1.05),
        xaxis=dict(tickangle=-35, tickfont=dict(size=9))
    )
    fig7.update_yaxes(title_text="Revenue ($)", secondary_y=False, showgrid=False)
    fig7.update_yaxes(title_text="Cumulative %", secondary_y=True, range=[0, 110],
                      showgrid=True, gridcolor='#F0F0F0')
    st.plotly_chart(fig7, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='section-title'>Cost Ratio % by Product — Risk Flagged</div>", unsafe_allow_html=True)
        cost_sorted = prod_filtered.sort_values('Cost_Ratio_Pct', ascending=True)
        cost_colors = [RED if v > 60 else AMBER if v > 40 else GREEN 
                       for v in cost_sorted['Cost_Ratio_Pct']]
        fig8 = go.Figure(go.Bar(
            x=cost_sorted['Cost_Ratio_Pct'],
            y=cost_sorted['Product Name'],
            orientation='h',
            marker_color=cost_colors,
            text=cost_sorted['Cost_Ratio_Pct'].apply(lambda x: f'{x:.1f}%'),
            textposition='inside',
            textfont=dict(color='white', size=10)
        ))
        fig8.add_vline(x=50, line_dash="dash", line_color=RED,
                       annotation_text="50% threshold", annotation_font_color=RED)
        fig8.update_layout(
            height=380, margin=dict(l=10, r=10, t=10, b=10),
            plot_bgcolor='white', paper_bgcolor='white',
            xaxis=dict(showgrid=False, showticklabels=False),
            yaxis=dict(title='', tickfont=dict(size=9)), showlegend=False
        )
        st.plotly_chart(fig8, use_container_width=True)
    
    with col2:
        st.markdown("<div class='section-title'>Sales vs Margin — Product Positioning</div>", unsafe_allow_html=True)
        avg_sales = prod_filtered['Total_Sales'].mean()
        scatter_colors = [QUAD_COLORS.get(q, BLUE) for q in prod_filtered['Quadrant']]
        fig9 = go.Figure()
        for quad in ['Star', 'Hidden Gem', 'Cash Trap', 'Dead Weight']:
            q_data = prod_filtered[prod_filtered['Quadrant'] == quad]
            fig9.add_trace(go.Scatter(
                x=q_data['Total_Sales'],
                y=q_data['Gross_Margin_Pct'],
                mode='markers+text',
                name=quad,
                marker=dict(size=q_data['Total_Profit']/200 + 8,
                           color=QUAD_COLORS.get(quad, BLUE), opacity=0.8),
                text=q_data['Product Name'].str[:15],
                textposition='top center',
                textfont=dict(size=8)
            ))
        fig9.add_vline(x=avg_sales, line_dash="dash", line_color=BLUE,
                       annotation_text="Avg sales", annotation_font_color=BLUE)
        fig9.add_hline(y=60, line_dash="dash", line_color=RED,
                       annotation_text="60% margin target", annotation_font_color=RED)
        fig9.update_layout(
            height=380, margin=dict(l=10, r=10, t=10, b=10),
            plot_bgcolor='white', paper_bgcolor='white',
            xaxis=dict(title='Total Sales ($)', showgrid=True, gridcolor='#F5F5F5'),
            yaxis=dict(title='Gross Margin %', showgrid=True, gridcolor='#F5F5F5'),
            legend=dict(orientation='h', y=-0.15, font=dict(size=10))
        )
        st.plotly_chart(fig9, use_container_width=True)

elif page == "📋 Executive Summary":
    
    st.markdown(f"""
    <div style="background:{NAVY};border-radius:10px;padding:1.5rem 2rem;margin-bottom:1.5rem">
        <h2 style="color:white;margin:0;font-size:1.4rem">Executive Summary</h2>
        <p style="color:#B5D4F4;margin:0.3rem 0 0 0;font-size:0.9rem">Nassau Candy Distributor · Profitability Analysis · FY 2024</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    kpis = [
        (f"${total_sales:,.0f}", "Total Revenue", BLUE),
        (f"${total_profit:,.0f}", "Total Profit", GREEN),
        (f"{gross_margin:.1f}%", "Gross Margin", AMBER),
        (str(high_risk_count), "High Risk Products", RED)
    ]
    for col, (val, lbl, color) in zip([col1,col2,col3,col4], kpis):
        with col:
            st.markdown(f"""<div class="kpi-card" style="border-top-color:{color}">
                <div class="kpi-label">{lbl}</div>
                <div class="kpi-value" style="color:{color}">{val}</div>
            </div>""", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='section-title'>Key Findings</div>", unsafe_allow_html=True)
        findings = [
            (BLUE, LIGHT_BLUE, "Finding 1 — Revenue Concentration",
             "Chocolate division generates 92.9% of total revenue ($131,693). This extreme concentration creates business continuity risk — any disruption to Chocolate sales would critically impact the entire company."),
            (GREEN, LIGHT_GREEN, "Finding 2 — Hidden Growth Opportunity",
             "Sugar division maintains a strong 66.6% gross margin — almost equal to Chocolate — yet contributes only 0.3% of revenue. This represents a significant untapped opportunity for profitable growth."),
            (RED, LIGHT_RED, "Finding 3 — Margin Risk in Other Division",
             "The Other division has only 44.8% gross margin — 23 percentage points below Chocolate. Products Kazookles and Wonka Gum are flagged HIGH RISK with margins below 45%."),
            (AMBER, LIGHT_AMBER, "Finding 4 — Pareto Concentration",
             "Just 5 Wonka Bar products generate 88% of all company revenue. The remaining 8 products contribute only 12% collectively, indicating significant portfolio imbalance.")
        ]
        for border, bg, title, text in findings:
            st.markdown(f"""<div class="finding-box" style="background:{bg};border-left-color:{border}">
                <div class="finding-title" style="color:{border}">{title}</div>
                <div class="finding-text" style="color:#333">{text}</div>
            </div>""", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='section-title'>Strategic Recommendations</div>", unsafe_allow_html=True)
        recs = [
            ("Grow Sugar Division",
             "Invest in marketing and distribution. With 66.6% margin, every additional dollar of Sugar revenue is nearly as profitable as Chocolate."),
            ("Review High-Risk Products",
             "Kazookles, Wonka Gum, and Lickable Wallpaper all have margins below 50%. Reprice, renegotiate costs, or discontinue these products."),
            ("Expand Gulf Region Presence",
             "Gulf generates only $22,247 vs Pacific's $46,302. Targeted expansion could significantly increase revenue at existing margin levels."),
            ("Reduce Chocolate Dependency",
             "Set a formal target to reduce Chocolate to below 80% of revenue within 3 years by growing Sugar and improving Other division margins.")
        ]
        for i, (title, text) in enumerate(recs, 1):
            st.markdown(f"""<div class="rec-box">
                <span class="rec-num">{i}</span>
                <strong style="font-size:0.85rem;color:{NAVY}">{title}</strong>
                <p style="font-size:0.8rem;color:#555;margin:0.3rem 0 0 2rem;line-height:1.5">{text}</p>
            </div>""", unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>Division Performance at a Glance</div>", unsafe_allow_html=True)
        fig10 = go.Figure(go.Bar(
            x=division_df['Division'],
            y=division_df['Gross_Margin_Pct'],
            marker_color=[DIV_COLORS.get(d, BLUE) for d in division_df['Division']],
            text=division_df['Gross_Margin_Pct'].apply(lambda x: f'{x:.1f}%'),
            textposition='outside'
        ))
        fig10.add_hline(y=60, line_dash="dash", line_color=RED)
        fig10.update_layout(
            height=220, margin=dict(l=10, r=10, t=10, b=10),
            plot_bgcolor='white', paper_bgcolor='white',
            xaxis=dict(title=''), yaxis=dict(title='Margin %', range=[0, 85]),
            showlegend=False
        )
        st.plotly_chart(fig10, use_container_width=True)
    
    st.markdown("---")
    st.markdown(f"""<p style="text-align:center;font-size:0.75rem;color:#888">
        Nassau Candy Distributor Profitability Analysis · Prepared by Khushi · May 2026 · 
        Tools: WPS Spreadsheets · SQL · Power BI · Streamlit
    </p>""", unsafe_allow_html=True)
