# Research and Development TEMPLATE

This is the template used to for all coding research and development projects. 

## Getting started

To use this template, read the [project template setup](https://www.notion.so/Gitlab-project-template-setup-ef2ee3e599f24ab1ad794274935e41c0?pvs=4) page which outlines the steps to use this repository. These include:

1. Navigate to this GitLab project to use as a template.
2. Click on the "Settings" icon in the sidebar, then select "General."
3. Scroll down to the "Advanced" section and click on the "Export project" button.
4. Download the exported project file.
5. Create a new project on GitLab and give it a name according to [Naming Conventions](https://www.notion.so/Naming-Conventions-080a14ec00b243149b9848dd7533c302?pvs=4).
6. In the new project, click on the "Import project" button.
7. Select the exported project file as the import source and choose the "Create as a template project" option.

**Note:** Adhere to Palindrome's [Naming Conventions](https://www.notion.so/Naming-Conventions-080a14ec00b243149b9848dd7533c302?pvs=4) for code, notebook/script and folder naming and [Git Best Practices](https://www.notion.so/Git-Best-Practices-9ff74439890d4518860e958def235304?pvs=4).

## Table of Contents
*Update table of contents with reference to the sections below*
1. [Getting Started](#getting-started) 
2. [Overview](#Overview)
3. [Technologies](#technologies)
4. [Installation](#installation)
5. [Folder Structure](#folder-structure)
6. [How to Run](#how-to-run)
7. [FAQs](#faqs)
8. [Contributing](#contributing)
9. [Authors and Acknowledgements](#authors-and-acknowledgment)
10. [Project Status](#project-status)

## Overview

This repo is for a training project with the aim of practicing skills using streamlit and docker. 
The streamlit app uses a random forest model, trained on movie data from MetaCritic, to predict MetaScores (a rating out of 100 given by MetaCritic). The user of the app inputs some basic information about the movie, including title, synopsis, release date, and rating and receives a prediction of the MetaScore. The model includes NLP of the movie title and synopsis, including topic identification. 

***

## Technologies
This project used python 3.7 in Visual Studio Code to explore and process data and create a random forest model on movie metascores. A streamlit app was created to run in a docker container.

***

## Installation and How to Run
Within a particular ecosystem, there may be a common way of installing things, such as using Yarn, NuGet, or Homebrew. However, consider the possibility that whoever is reading your README is a novice and would like more guidance. Listing specific steps helps remove ambiguity and gets people to using your project as quickly as possible. If it only runs in a specific context like a particular programming language version or operating system or has dependencies that have to be installed manually, also add a Requirements subsection.

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
Future expansions on this project aims to include other data on the movies (e.g. revenue and director names); testing best practices (e.g. using pytest); improved visuals and design (e.g. colour scheme and pictures of searched images); improved capabilities/features; performance improvements to increase the speed of the prediction; remove dependence on user score so a non-existent movie can be used. 

***