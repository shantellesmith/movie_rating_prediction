import streamlit as st
import pandas as pd
import numpy as np
import joblib
import pickle
import xgboost as xgb
import time
from PIL import Image
from bertopic import BERTopic
import altair as alt

import sys
sys.path.append('src')
from language_processing import *

st.set_page_config(page_title="Movie MetaScore", layout="wide")

sysmenu = '''
<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
'''
st.markdown(sysmenu,unsafe_allow_html=True)

@st.cache(suppress_st_warning=True)

def get_fvalue(val):    
    feature_dict = {"No":1,"Yes":2}    
    for key,value in feature_dict.items():        
        if val == key:            
            return value
def get_value(val,my_dict):    
    for key,value in my_dict.items():        
        if val == key:            
            return value
        
app_mode = st.sidebar.selectbox('Select Page',['Home','Prediction']) #two pages

if app_mode=='Home':    
    
    st.title('METASCORE PREDICTION :')      
    #st.image('loan_image.jpg')    
    st.markdown('Dataset :')    
    data=pd.read_csv('data/processed/df_movies_processed.csv')    
    st.write(data.head())    
    st.markdown('User Score VS MetaScore')    
    
    color = alt.Color("metascore:O")
    # We create two selections:
    # - a brush that is active on the top panel
    # - a multi-click that is active on the bottom panel
    brush = alt.selection_interval(encodings=["x"])
    click = alt.selection_multi(encodings=["color"])

    # Top panel is scatter plot of temperature vs time
    points = (
        alt.Chart(data)
        .mark_circle()
        .encode(
            alt.X("title_topic:Q", title="Title's Topic"),
            alt.Y("release_year:Q", title="Release Year",
                scale=alt.Scale(domain=[1920, 2025]),
            ),
            color="metascore:Q",#alt.condition(brush, color, alt.value("lightgray")),
        )
        .properties(width=550, height=300)
        .interactive()
    )

    #st.bar_chart(data[['user_score','metascore']].head(20))
    st.altair_chart(points, theme="streamlit", use_container_width=True)

elif app_mode == 'Prediction':    
    #st.image('slider-short-3.jpg')    
    st.subheader('Please fill in all necessary informations in order    \
                 to determine the metascore for a movie !')
    with st.sidebar:
        st.markdown(
        """
        <style>
        .sidebar .sidebar-content {
            background-image: none;
            color: #887BB0;
        }
        </style>
        """,
            unsafe_allow_html=True,
        )
        st.sidebar.header("Informations about the movie :")
        months_dict = {'Jan':1,'Feb':2,'Mar':3,'Apr':4,'May':5,'Jun':6,'Jul':7,'Aug':8,'Sep':9,'Oct':10,'Nov':11,'Dec':12}
        rating_dict = {'Unknown':0, 'Approved':1, 'G':2, 'GP':3, 'M':4, 'M-PG':5, 'MA-17':6, 'NC-17':7,
                        'Not Rated':8, 'Open':9, 'PG':10, 'PG-13':11, 'Passed':12, 'R':13, 'TV-14':14, 'TV-G':15,
                        'TV-MA':16, 'TV-PG':17, 'TV-Y7':18, 'TV-Y7-FV':19}
        feature_dict = {"No":1,"Yes":2}
        ReleaseYear=st.sidebar.slider('Release Year',1990,2050,2000,1)
        ReleaseMonth=st.sidebar.selectbox('Release Month',tuple(months_dict.keys()))
        ReleaseQuarter=st.sidebar.slider('Release Quarter',1,4,1,1)
        ReleaseYearWeek=st.sidebar.slider('Release Week Number',1,52,1,1)
        Rating=st.sidebar.selectbox('Box Office Rating',tuple(rating_dict.keys()))
        UserScore=st.sidebar.slider('User Score',0.0,10.0,5.0,0.1)
        Title=st.sidebar.text_input('Movie Title',"Star Wars: The Rise of Skywalker")
        Summary=st.sidebar.text_input('Movie Summary (Synopsis)',
                                    "When it's discovered that the evil Emperor Palpatine did not die at the hands of Darth Vader, \
                                        the rebels must race against the clock to find out his whereabouts. \
                                            Finn and Poe lead the Resistance to put a stop to the First Order's plans to form \
                                                a new Empire, while Rey anticipates her inevitable confrontation with Kylo Ren.")
        TitleCapCount=count_capital_words(Title)
        SummaryCapCount=count_capital_words(Summary)
        TitleSentCount=count_sent(Title)
        SummarySentCount=count_sent(Summary)
        TitleLength=len(Title) #Length in chars not words
        SummaryLength=len(Summary)
        TitleAvgWordLength=len(Title)/len(Title.split())
        SummaryAvgWordLength=len(Summary)/len(Summary.split())
        TitleUniqWordRatio=count_unique_words(Title)/len(Title.split())
        SummaryUniqWordRatio=count_unique_words(Summary)/len(Summary.split())
        TitleStopCount=count_stopwords(Title)
        SummaryStopCount=count_stopwords(Summary)
        TitleStopWordsRatio=TitleStopCount/len(Title.split())
        SummaryStopWordsRatio=SummaryStopCount/len(Summary.split())

    if st.button("Predict"):
        ReleaseMonth=months_dict.get(ReleaseMonth, ReleaseMonth)
        RatingScore=rating_dict.get(Rating, Rating)
        
        data1={'rating':RatingScore, 'user_score':UserScore,    
            'release_year':ReleaseYear, 'release_month':ReleaseMonth,    
            'release_quarter':ReleaseQuarter, 'release_yearweek':ReleaseYearWeek,    
            'title_len':TitleLength, 'summary_len':SummaryLength,
            'title_avg_wordlength':TitleAvgWordLength, 'summary_avg_wordlength':SummaryAvgWordLength, 
            'title_capcount':TitleCapCount,'summary_capcount':SummaryCapCount, 
            'title_sentcount':TitleSentCount, 'summary_sentcount':SummarySentCount,
            'title_uniq_vs_words':TitleUniqWordRatio, 'summary_uniq_vs_words':SummaryUniqWordRatio, 
            'title_stopcount':TitleStopCount,'summary_stopcount':SummaryStopCount, 
            'title_stopwords_vs_words':TitleStopWordsRatio,
            'summary_stopwords_vs_words':SummaryStopWordsRatio}       
        
        topic_model_title = BERTopic.load("models/topic_model_title")
        topic_model_summary = BERTopic.load("models/topic_model_summary")
        sentence_model = sentence_transformers.SentenceTransformer("all-MiniLM-L6-v2")
        embeddings_title = sentence_model.encode([Title], show_progress_bar=False)
        embeddings_summary = sentence_model.encode([Summary], show_progress_bar=False)
        topics_t, probabilities_t = topic_model_title.transform([Title], embeddings_title)
        TitleTopic=topics_t[0]#topic_model_title.topics_[:]
        topics_s, probabilities_s = topic_model_summary.transform([Summary], embeddings_summary)
        SummaryTopic=topics_s[0]#topic_model_summary.topics_[:]

        data1['title_topic']=TitleTopic
        data1['summary_topic']=SummaryTopic
        feature_list=list(data1.values())
        single_sample = pd.DataFrame(np.array(feature_list, dtype='float').reshape(1,-1),columns=list(data1.keys()))
        
        #model = xgb.Booster()
        #model.load_model('models/xgboost_reg_model_metascore.pkl')
        model = joblib.load('models/random_forest_reg_model_metascore.joblib')
        #single_sample_dmatrix = xgb.DMatrix(single_sample) 
        #st.text("Data modified")
        prediction = model.predict(single_sample)
        st.write("The metascore will be ")
        st.write(prediction[0].round(1))   
