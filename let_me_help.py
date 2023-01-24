import os.path
from os import listdir
from os.path import isfile, join
import streamlit as st
import pandas as pd
import numpy as np


import data
import questions
import recommender

NUM_QUESTIONS = 7
IMGS_DIR_PATH = 'images'

files = [f for f in listdir(IMGS_DIR_PATH) if isfile(join(IMGS_DIR_PATH, f))]

# Create session variables
if "session_type" not in st.session_state:
    st.session_state.session_type = None  # can be one of (None, 'recommendation', 'decision')

if "type_btn_disabled" not in st.session_state:
    st.session_state.type_btn_disabled = False

if "started" not in st.session_state:
    st.session_state.started = False

if "finished" not in st.session_state:
    st.session_state.finished = False

if 'selections' not in st.session_state:
    st.session_state.selections = []

if 'question_count' not in st.session_state:
    st.session_state.question_count = 0

if 'questions' not in st.session_state:
    st.session_state.questions = questions.get_questions(NUM_QUESTIONS)

if 'btn_disabled' not in st.session_state:
    st.session_state.btn_disabled = False

if 'recommendations' not in st.session_state:
    st.session_state.recommendations = []

if 'new_recommendations' not in st.session_state:
    st.session_state.new_recommendations = []

if 'features' not in st.session_state:
    st.session_state.features = []

if 'user_score' not in st.session_state:
    st.session_state.features = []

if "domain" not in st.session_state:
    st.session_state.domain = None

if "restart_btn_disabled" not in st.session_state:
    st.session_state.restart_btn_disabled = True

if "textbox_disabled" not in st.session_state:
    st.session_state.textbox_disabled = True


# help functions
def set_session_type(type):
    """:type: one of (None, 'recommendation', 'decision')"""
    st.session_state.session_type = type
    if type:
        st.session_state.type_btn_disabled = True
        st.session_state.restart_btn_disabled = False
    else:
        st.session_state.type_btn_disabled = False


def start_questions():
    st.session_state.started = True


def question_answered(selection: tuple):
    st.session_state.question_count = min(
        st.session_state.question_count + 1, NUM_QUESTIONS)
    st.session_state.selections.append(selection)


def get_new_recommendations(new_user_score, domain=st.session_state.domain):
    new_rec, _, _ = recommender.get_recommendations(domain=domain,
                                                    user_score=new_user_score)
    st.session_state.new_recommendations = new_rec


def restart():
    st.session_state.question_count = 0
    st.session_state.btn_disabled = False
    st.session_state.finished = False
    st.session_state.started = False
    st.session_state.restart_btn_disabled = True
    set_session_type(None)
    st.session_state.questions = questions.get_questions(NUM_QUESTIONS + 1)
    st.session_state.selections = []
    st.session_state.question_count = 0
    st.session_state.new_recommendations = []


# app layout and flow
st.title(':green[Let Me Help]')
st.subheader("Need an advice? Having hard time picking the right gift or "
             "vacation destination? Need some ideas?")
st.subheader("Let Me Help you!")
# st.subheader('How may I help you?')

if not st.session_state.session_type:
    col1, col2 = st.columns(2)
    with col1:
        st.write("If you want to get some ideas click here:")
        st.button("I want a recommendation", on_click=set_session_type,
                  args=('recommendation', ),
                  disabled=st.session_state.type_btn_disabled)
    with col2:
        st.write("If you have something in mind but can't decide click here:")
        st.button("Help me decide", on_click=set_session_type,
                  args=('decision', ),
                  disabled=st.session_state.type_btn_disabled)

# user chose to get recommendation
if st.session_state.session_type == 'recommendation':
    # select the domain
    st.session_state.domain = st.selectbox(
        'What do you need recommendations for?',
        ('Vacation', 'Gift'))  #, 'Restaurant', 'Movie'))
    # st.write(f"Sure, let's find you a {domain}.")
    #
    st.write("""
        You are going to be presented with a short series of questions.\n
        On every question, all you have to do is select 1 picture and 
        I'll do the rest.
    """)

# user chose to get help with decision
if st.session_state.session_type == "decision":
    st.write("""I can help you decide between 2 options.
             What do you have in mind?\nEnter below please:""")
    col1, col2 = st.columns(2)

    with col1:
        text_input_1 = st.text_input(
            "Option 1",
            # disabled=st.session_state.textbox_disabled,
            placeholder="e.g. take a walk",
        )
    with col2:
        text_input_2 = st.text_input(
            "Option 2",
            # disabled=st.session_state.textbox_disabled,
            placeholder="e.g. see a movie",
        )
    st.write(text_input_1)

    st.write("""
            You are going to be presented with a short series of questions.\n
            On every question, all you have to do is select 1 picture and 
            I'll do the rest.
        """)

# type of help was chosen, start questions
if st.session_state.session_type:
    start_btn = st.button('Start', disabled=st.session_state.started,
                          on_click=start_questions)

    if st.session_state.started and not st.session_state.finished:
        if st.session_state.question_count == NUM_QUESTIONS:
            st.session_state.btn_disabled = True
            st.session_state.finished = True

        q_df = st.session_state.questions
        index = min(st.session_state.question_count, NUM_QUESTIONS-1)
        left_img = q_df.iloc[index, :2].values
        right_img = q_df.iloc[index, 2:].values

        col1, col2 = st.columns(2)
        with col1:
            st.image(os.path.join(IMGS_DIR_PATH, left_img[0]), caption=left_img[1])
            left_btn = st.button('Choose This', key='left_btn',
                                 on_click=question_answered,
                                 args=((left_img[1], right_img[1]), ),
                                 disabled=st.session_state.btn_disabled)
        with col2:
            st.image(os.path.join(IMGS_DIR_PATH, right_img[0]), caption=right_img[1])
            right_btn = st.button('Choose This', key='right_btn',
                                  on_click=question_answered,
                                  args=((right_img[1], left_img[1]), ),
                                  disabled=st.session_state.btn_disabled)

        progress_bar = st.progress(st.session_state.question_count / NUM_QUESTIONS)

# questions session is finished, give recommendations/decision
if st.session_state.finished:
    if st.session_state.session_type == "recommendation":
        st.session_state.recommendations, \
            st.session_state.user_score, \
            st.session_state.features = recommender.get_recommendations(
            st.session_state.domain, st.session_state.selections)

        # st.write(st.session_state.user_score)

        st.subheader(f"Recommended {st.session_state.domain}:")
        st.table(pd.DataFrame(
            st.session_state.recommendations,
            index=np.arange(1, len(st.session_state.recommendations)+1),
            columns=[f'Recommended {st.session_state.domain}']))

        st.write(f'The recommendations are based on the following parameters '
                 f'which were deduced from your answers')
        sliders = dict()
        for f in st.session_state.features:
            sliders[f] = st.slider(f, 0, 10,
                                   round(st.session_state.user_score[f] * 10))

        st.write("If you would different recommendations, change the sliders to "
                 "match your preferences and click the button below.")

        new_user_score = dict([(f, sliders[f]) for f in st.session_state.features])

        st.button("Get New Recommendations", on_click=get_new_recommendations,
                  args=(new_user_score, ))
        # st.session_state.new_recommendations = get_new_recommendations(new_user_score)

        if st.session_state.new_recommendations:
            st.subheader(f"New recommended {st.session_state.domain}:")
            st.table(pd.DataFrame(
                st.session_state.new_recommendations,
                index=np.arange(1, len(st.session_state.new_recommendations) + 1),
                columns=[f'Recommended {st.session_state.domain}']))

    if st.session_state.session_type == "decision":
        options = {1: text_input_1, 2: text_input_2}
        # st.write("finished")
        decision = recommender.help_decide(text_input_1, text_input_2,
                                st.session_state.selections)
        st.write("The winner is:")
        st.subheader(options[decision])

st.button("Restart", disabled=st.session_state.restart_btn_disabled,
          on_click=restart)
