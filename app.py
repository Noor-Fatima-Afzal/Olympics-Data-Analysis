import streamlit as st
import pandas as pd
import preprocessor, helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

df = pd.read_csv(r'C:\Users\InfoBay\OneDrive\المستندات\olympic_analysis_web_app\athlete_events.csv')
df_region = pd.read_csv(r'C:\Users\InfoBay\OneDrive\المستندات\olympic_analysis_web_app\noc_regions.csv')

df = preprocessor.preprocess(df, df_region)

st.sidebar.title('Olympics Analysis')
st.sidebar.image(r'C:\Users\InfoBay\OneDrive\المستندات\olympic_analysis_web_app\oly.png')
user_menue = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally', 'Overall Analysis', 'Country Wise Analysis', 'Athelete wise Analysis')
)


if user_menue == 'Medal Tally':
    st.header('Olympics Medal Tally')
    years, countries = helper.country_year_list(df)
    selected_year = st.sidebar.selectbox('Select Year', years)
    selected_country = st.sidebar.selectbox('Select Country', countries)

    medal_tally =  helper.fetch_medal_tally(df, selected_year, selected_country)
    if selected_country == 'Overall' and selected_year == 'Overall':
        st.title('Overall Medal Tally')
    if selected_country != 'Overall' and selected_year == 'Overall':
        st.title(selected_country + ' Medal Tally')
    if selected_country == 'Overall' and selected_year != 'Overall':
        st.title('Medal Tally in ' + str(selected_year) + ' Olympics')
    if selected_country != 'Overall' and selected_year != 'Overall':
        st.title(selected_country + ' Medal Tally in ' + str(selected_year) + ' Olympics')
    st.table(medal_tally)

if user_menue == 'Overall Analysis':
    editions = df['Year'].unique().shape[0]-1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    event  = df['Event'].unique().shape[0]
    atheletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title('Top Statistics')

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header('Editions')
        st.title(editions)
    with col2:
        st.header('Hosts')
        st.title(cities)
    with col3:
        st.header('Sports')
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header('Events')
        st.title(event)
    with col2:
        st.header('Atheletes')
        st.title(atheletes)
    with col3:
        st.header('Nations')
        st.title(nations)

    nations_over_time = helper.data_over_time(df, 'region')
    fig = px.line(nations_over_time, x = 'Edition', y = 'region')
    st.title('Participating Nations Over Years')
    st.plotly_chart(fig)

    events_over_time = helper.data_over_time(df, 'Event')
    fig = px.line(events_over_time, x = 'Edition', y = 'Event')
    st.title('Events Over the Years')
    st.plotly_chart(fig)

    atheletes_over_time = helper.data_over_time(df, 'Name')
    fig = px.line(atheletes_over_time, x = 'Edition', y = 'Name')
    st.title('Atheletes Over the Years')
    st.plotly_chart(fig)

    st.title('Number of events over time(Every Sport)')
    fig, ax = plt.subplots(figsize=(20,20))
    x = df.drop_duplicates(['Year','Sport','Event'])
    ax = sns.heatmap(x.pivot_table(index= 'Sport', columns = 'Year', values = 'Event', aggfunc = 'count').fillna(0).astype('int'),annot = True)
    st.pyplot(fig)

    st.title('Most Successful Athletes')
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    selected_sport = st.selectbox('Select a Sport', sport_list)
    x = helper.most_successful(df, selected_sport)
    st.table(x)

if user_menue == 'Country Wise Analysis':

    st.sidebar.title('Country Wise Analysis')
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()
    selected_country = st.sidebar.selectbox('Select a Country', country_list)
    country_df = helper.year_wise_medal_tally(df, selected_country)
    fig = px.line(country_df, x = 'Year', y = 'Medal')
    st.title(selected_country + 'Medal Tally Over the Years')
    st.plotly_chart(fig)
    pt = helper.country_event_heatmap(df, selected_country)
    fig, ax = plt.subplots(figsize=(20,20))
    ax = sns.heatmap(pt, annot=True)
    st.title(selected_country + ' Performance Over the Years')
    st.pyplot(fig) 

    top10_df = helper.most_successful_countrywise(df, selected_country)
    st.title('Most Successful Athletes from ' + selected_country)
    st.table(top10_df)

if user_menue == 'Athelete wise Analysis':
    athelete_df = df.drop_duplicates(subset=['Name', 'region'])
    x1 = athelete_df['Age'].dropna()
    x2 = athelete_df[athelete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athelete_df[athelete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athelete_df[athelete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold medalist', 'Silver medalist', 'Bronze medalist'], show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600, title='Age Distribution of Atheletes')

    st.title('Age Distribution')
    st.plotly_chart(fig)

    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in famous_sports:
        temp_df = athelete_df[athelete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age wrt Sports(Gold Medalist)")
    st.plotly_chart(fig)

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    st.title('Height Vs Weight')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp_df = helper.weight_vs_height(df,selected_sport)
    fig,ax = plt.subplots()
    ax = sns.scatterplot(x='Weight', y='Height', hue='Medal', style='Sex', s=60, data=temp_df, ax=ax)
    st.pyplot(fig)

    st.title("Men Vs Women Participation Over the Years")
    final = helper.men_vs_women(df)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)