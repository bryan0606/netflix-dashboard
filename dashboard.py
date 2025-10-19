import streamlit as st
import pandas as pd
import plotly.express as px

#Load dataset
df = pd.read_csv("data/netflix_titles.csv")

#Fill in missing values & convert date_added to datetime
df['country'] = df['country'].fillna('Unknown')
df['director'] = df['director'].fillna('Unknown')
df['cast'] = df['cast'].fillna('Unknown')
df['rating'] = df['rating'].fillna('Not Rated')
df['duration'] = df['duration'].fillna('Unknown')
df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')

#Create dashboard
st.title("🎬 Netflix Dashboard")

#Sidebar filters
st.sidebar.header("Filter Options")
type_filter = st.sidebar.multiselect("Select Type",df['type'].unique(),default=df['type'].unique())
country_filter = st.sidebar.multiselect("Select Country",df['country'].unique(),default=df['country'].unique())
genre_filter = st.sidebar.multiselect("Select Genre",df['listed_in'].unique(),default=df['listed_in'].unique())

# Apply filters
filtered_df = df[
    (df['type'].isin(type_filter)) &
    (df['country'].isin(country_filter)) &
    (df['listed_in'].isin(genre_filter))
]


# Count titles by type
count_type = filtered_df['type'].value_counts().reset_index()
count_type.columns = ['Type', 'Count']

fig = px.bar(count_type, x='Type', y='Count', color='Type', title="Number of Titles by Type", text = "Count")

#Count titles by country
top_countries = filtered_df['country'].value_counts().head(10).reset_index()
top_countries.columns = ['Country', 'Count']

fig2 = px.bar(top_countries, x='Country', y='Count', color='Country', title="Top 10 Countries", text = "Count")

# Count titles by release year
release_year_count = filtered_df['release_year'].value_counts().sort_index().reset_index()
release_year_count.columns = ['Year', 'Count']

# Plot how many movies were released each year
# markers add dot for each year in the line graph
fig_year = px.line(release_year_count, x='Year', y='Count', title="Number of Titles Released Each Year", markers=True)

# Filter only Movies with numeric duration
movies_df = filtered_df[filtered_df['type'] == 'Movie'].copy()
movies_df['duration_minutes'] = pd.to_numeric(movies_df['duration'].str.replace(' min',''), errors='coerce')

# Plot histogram
fig_duration = px.histogram(
    movies_df,
    x='duration_minutes',
    nbins=20,
    title="Distribution of Movie Durations (Minutes)"
)

#Show top 10 longest movies
top_movies = movies_df.sort_values(by='duration_minutes', ascending=False).head(10)

#Add tabs for organisation
tab1, tab2, tab3 = st.tabs(["Overview", "Duration", "Top Titles"])

with tab1:
    st.plotly_chart(fig, use_container_width=True)  # bar chart
    st.plotly_chart(fig_year, use_container_width=True)  # release year trend

with tab2:
    st.plotly_chart(fig_duration, use_container_width=True)  # duration histogram

with tab3:
    st.subheader("Top 10 Longest Movies")
    st.dataframe(top_movies[['title','duration','release_year','country','rating']])

#Download button for user
st.download_button("Download CSV", filtered_df.to_csv(index=False), "netflix_filtered.csv")
