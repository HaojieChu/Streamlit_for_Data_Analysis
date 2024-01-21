import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
from PIL import Image
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
from plotly.subplots import make_subplots

st.set_page_config(
     page_title='Streamlit cheat sheet',
     layout="wide",
     initial_sidebar_state="expanded",
     
)

st.title('Dashboard (7009 Alternative Assessment)')
with st.chat_message("Haojie Chu", avatar="🐰"):
    st.write("Haojie Chu S2175919")

df = pd.read_csv('Entrepreneurial Competency Dataset.csv')

col1, col2, col3 = st.columns(3, gap = "medium")

with col1:
    st.header("Distribution of Key Traits Among Entrepreneurs")
    entrepreneurs = df[df['entrepreneur or not '] == 1]

    # Count the frequency of each key trait
    key_trait_counts = entrepreneurs['KeyTraits'].value_counts()

    # Create a pie chart
    fig = px.pie(
        names=key_trait_counts.index,
        values=key_trait_counts.values,
    )
    st.plotly_chart(fig)


with col2:
    st.header("Comparison of Attributes: Entrepreneurs vs Non-Entrepreneurs")

    # List of attributes to analyze
    attributes = ['Perseverance', 'DesireToTakeInitiative', 'Competitiveness',
                'SelfReliance', 'StrongNeedToAchieve', 'SelfConfidence', 'GoodPhysicalHealth']

    # Calculate the average of each attribute for entrepreneurs (1) and non-entrepreneurs (0)
    avg_attributes_entrepreneurs = df[df['entrepreneur or not '] == 1][attributes].mean()
    avg_attributes_non_entrepreneurs = df[df['entrepreneur or not '] == 0][attributes].mean()

    # Convert averages to lists and append the first value to close the radar chart
    avg_attributes_entrepreneurs_list = avg_attributes_entrepreneurs.tolist() + [avg_attributes_entrepreneurs[0]]
    avg_attributes_non_entrepreneurs_list = avg_attributes_non_entrepreneurs.tolist() + [avg_attributes_non_entrepreneurs[0]]

    # Create radar chart
    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=avg_attributes_entrepreneurs_list,
        theta=attributes + [attributes[0]],
        fill='toself',
        name='Entrepreneurs',
        fillcolor = px.colors.qualitative.Plotly[2],
        marker_color = px.colors.qualitative.Plotly[2],
        opacity=0.7
    ))

    fig.add_trace(go.Scatterpolar(
        r=avg_attributes_non_entrepreneurs_list,
        theta=attributes + [attributes[0]],
        fill='toself',
        name='Non-Entrepreneurs',
        fillcolor = px.colors.qualitative.Plotly[1],
        marker_color = px.colors.qualitative.Plotly[1],
        opacity=0.7
    ))

    # Update the layout
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, max(avg_attributes_entrepreneurs_list + avg_attributes_non_entrepreneurs_list)]
            )),
        margin=dict(t=15, b=15, l = 50, r = 15),
        showlegend=True,
    )

    st.plotly_chart(fig)

with col3:
    st.header("Number of People Becoming Entrepreneurs by Education Sector")
    grouped_data = df.groupby(['EducationSector', 'entrepreneur or not ']).size().unstack().reset_index()

    # Melt the DataFrame for Plotly
    melted_data = pd.melt(grouped_data, id_vars=['EducationSector'], value_vars=[0, 1],
                        var_name='Entrepreneur Status', value_name='Number of People')

    # Plotting using Plotly Express
    fig = px.bar(melted_data, x='EducationSector', y='Number of People', color='Entrepreneur Status',
                # title='Number of People Becoming Entrepreneurs by Education Sector',
                labels={'EducationSector': 'Education Sector', 'Number of People': 'Number of People'},
                category_orders={'EducationSector': sorted(df['EducationSector'].unique())},
                width=800, height=500,
                color_discrete_map={0: px.colors.qualitative.Plotly[2], 1: px.colors.qualitative.Plotly[1]})

    # Rotate x-axis labels for better readability
    fig.update_layout(xaxis=dict(tickangle=45))

    # Show the plot
    st.plotly_chart(fig)

col4, col5 = st.columns(2, )

with col4:
    st.header("Key Reasons for Lacking of Entrepreneurial Intention")

    # Filter for rows where 'entrepreneur or not' is 0
    filtered_data = df[df['entrepreneur or not '] == 0]

    # Extract 'ReasonsForLack' text
    reasons_for_lack_text = ' '.join(filtered_data['ReasonsForLack'].dropna())

    # Define the set of stop words, remove 'not' from it, and add 'something'
    stopwords = set(STOPWORDS)
    stopwords.remove('not')  # Ensure 'not' is not treated as a stop word
    stopwords.add('something')  # Add 'something' to the stop words

    # Generate the word cloud
    wordcloud = WordCloud(width=500, height=200,
                        background_color='white',
                        stopwords=stopwords,
                        min_font_size=10).generate(reasons_for_lack_text)

    # Display the word cloud
    plt.figure(figsize=(5, 5), facecolor=None)
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.tight_layout(pad=0)
    st.pyplot(plt)

with col5:
    st.header("Mental Health Distribution: Entrepreneurs vs Non-Entrepreneurs")
    entrepreneurs = df[df['entrepreneur or not '] == 1]
    non_entrepreneurs = df[df['entrepreneur or not '] == 0]

    # Count the occurrences of mental disorders in both groups
    mental_health_counts_entrepreneurs = entrepreneurs['MentalDisorder'].value_counts()
    mental_health_counts_non_entrepreneurs = non_entrepreneurs['MentalDisorder'].value_counts()

    # Create subplots for two pie charts
    fig = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}]])
    fig.add_trace(go.Pie(labels=mental_health_counts_entrepreneurs.index,
                        values=mental_health_counts_entrepreneurs.values,
                        name='Entrepreneurs', marker_colors = [px.colors.qualitative.Plotly[1], px.colors.qualitative.Plotly[2]]),
                1, 1,)
    fig.add_trace(go.Pie(labels=mental_health_counts_non_entrepreneurs.index,
                        values=mental_health_counts_non_entrepreneurs.values,
                        name='Non-Entrepreneurs', marker_colors = [px.colors.qualitative.Plotly[1], px.colors.qualitative.Plotly[2]]),
                1, 2)

    # Update the layout
    fig.update_layout(
        annotations=[dict(text='Entrepreneurs', x=0.18, y=0.5, font_size=12, showarrow=False, font_color = 'black'),
                    dict(text='Non-Entrepreneurs', x=0.82, y=0.5, font_size=12, showarrow=False, font_color = 'black')]
    )
    st.plotly_chart(fig)
