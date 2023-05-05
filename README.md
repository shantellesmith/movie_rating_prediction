# MetaCritic Model and Streamlit App

## Table of Contents
1. [Overview](#overview)
2. [Technologies](#technologies)
3. [Installation and How to Run](#installation-and-how-to-run)
4. [Authors and Acknowledgements](#authors-and-acknowledgement)
5. [Project Status](#project-status)

## Overview

This repo is for a training project with the aim of practicing skills using streamlit and docker. 
The streamlit app uses a random forest model, trained on movie data from MetaCritic, to predict MetaScores (a rating out of 100 given by MetaCritic). The user of the app inputs some basic information about the movie, including title, synopsis, release date, and rating and receives a prediction of the MetaScore. The model includes NLP of the movie title and synopsis, including topic identification. 

***

## Technologies
This project used python 3.7 in Visual Studio Code to explore and process data and create a random forest model on movie metascores. A streamlit app was created to run in a docker container.

***

## Installation and How to Run

### Step 1

Download repo as .zip folder and extract. Change directory in terminal to extracted folder.

### Step 2

```python
docker build -t metascore_streamlit_app .
```

### Step 3

```python
docker run --name MyContainer -p 8501:8501 metascore_streamlit_app
```

### Step 4

Open [http://0.0.0.0:8501/](http://0.0.0.0:8501/)

### Step 5

Navigate to ‘Prediction’ using left dropdown menu.

### Step 6

Fill in the information about your movie on the left panel and click predict on the right when ready. The app will display the predicted MetaScore. 
***

## Authors and acknowledgement
Data obtained from https://www.kaggle.com/datasets/patkle/metacritic-scores-for-games-movies-tv-and-music.
All code created by Shantelle Smith. 

***
## Project status
A basic version of a streamlit app has been created with the ability to build and run it in a docker container.
Future expansions on this project aims to include other data on the movies (e.g. revenue and director names); testing best practices (e.g. using pytest); improved visuals and design (e.g. colour scheme and pictures of searched images); improved capabilities/features; performance improvements to increase the speed and accuracy of the prediction; remove dependence on user score so a non-existent movie can be used. Using an alternative target variable (e.g. gross profit) could provide a better business use case for this type of application/model and binning the target could be used in a classification problem (e.g. high and low scored movies). Optimising the regression model could be achieved by finding more predictive features, attempting further feature selection, transforming the target (e.g. log), using an alternative regression model or target. 

***