import pandas as pd
import streamlit as st
import plotly.express as px

# 1. Mandatory First Streamlit Execution Rule
st.set_page_config(layout="wide")

# 2. Establish dataset with explicit whole-number metrics
data = {
    'Necessity': [
        'Education', 'Housing', 'Health care', 'Having a family', 
        'Groceries', 'Food', 'Utilities', 'Transportation'
    ],
    'Unaffordable': [58, 54, 47, 44, 28, 26, 23, 22],
    'Unknown/No Opinion': [8, 2, 3, 5, 1, 1, 1, 3],
    'Somewhat Affordable': [26, 31, 37, 38, 54, 59, 57, 47],
    'Mostly Affordable': [8, 13, 13, 13, 17, 14, 19, 28]
}

df = pd.DataFrame(data)

# Sort ascending so the highest 'Unaffordable' value is positioned at the top of the horizontal layout
df = df.sort_values(by='Unaffordable', ascending=True)

# 3. Melt dataframe for perfect Plotly compatibility and custom hover string construction
df_melted = df.melt(id_vars='Necessity', var_name='Sentiment', value_name='Percentage')

def construct_hover(row):
    if row['Sentiment'] == 'Unknown/No Opinion':
        return f"{row['Percentage']}% of voters declined to answer"
    else:
        return f"{row['Percentage']}% of voters find {row['Necessity']} to be {row['Sentiment']}"

df_melted['Custom_Hover'] = df_melted.apply(construct_hover, axis=1)

# 4. Exact NYT Color Palette mapping
color_map = {
    'Unaffordable': '#e28743',
    'Unknown/No Opinion': '#e0e0e0',
    'Somewhat Affordable': '#a3d9c9',
    'Mostly Affordable': '#2a7561'
}

# 5. Generate Interactive Plotly Chart
fig = px.bar(
    df_melted,
    y='Necessity',
    x='Percentage',
    color='Sentiment',
    orientation='h',
    color_discrete_map=color_map,
    category_orders={"Sentiment": ['Unaffordable', 'Unknown/No Opinion', 'Somewhat Affordable', 'Mostly Affordable']},
    custom_data=['Custom_Hover']
)

# Apply specific text formatting to ensure clean layout with black text inside bars
fig.update_traces(
    texttemplate='%{x}%', 
    textposition='inside',
    textfont=dict(color='black', size=12, family="Arial"),
    hovertemplate='%{customdata[0]}<extra></extra>'
)

# Configure layout properties to eliminate grid lines and match clean journalism style
fig.update_layout(
    title=dict(text="<b>Voter Sentiment Regarding Affordability of Necessities</b>", x=0.01, font=dict(size=18)),
    xaxis=dict(visible=False, range=[0, 100]),
    yaxis=dict(title=""),
    barmode='stack',
    showlegend=True,
    legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5, title=""),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=150, r=20, t=60, b=60),
    height=500
)

# 6. Render Chart Element
st.plotly_chart(fig, use_container_width=True)