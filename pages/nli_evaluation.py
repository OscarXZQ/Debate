import streamlit as st
import json
import pandas as pd
import sys
import numpy as np
import random

import streamlit as st
import json
import pandas as pd
from collections import Counter

uploaded_file = st.file_uploader("Choose a jsonl file prediction to upload", type=["jsonl"])
data = []
labels = ['is against Hillary', 'asks about a location', 'is related to math and science', 'asks for a quantity', 'related to computer or internet', 'involves a situation where people need clean water', 'is grammatical', 'is about world news', 'insult women or immigrants', 'expresses need for utility, energy or sanitation', 'describes a situation that involves terrorism', 'is about physics', 'is about sports news', 'asks about an entity', 'is a more objective description of what happened', 'describes a situation where people need shelter', 'is related to a medical situation', 'supports abortion', 'is about math research', 'is related to food security', 'is related to business', 'is against religion', 'believes in god', 'thinks the movie is good', 'is about entertainment', 'supports feminism', 'is related to technology', 'asks for an opinion', 'asks about a person', 'is against environmentalist', 'is related to health', 'contains subjective opinion', 'involves crime', 'is related to politics or government', 'is pro-life', 'is related to computer science', 'is about statistics', 'involves a search/rescue situation', 'is related to infrastructure', 'contains a bad movie review', 'is ungrammatical', 'asks for factual information', 'is about family and relationships', 'asks about an abbreviation', 'is environmentalist', 'contains offensive content', 'involves a need for people to evacuate', 'is related to sports', 'is offensive to women', 'contains a definition', 'describes a regime change', 'contains irony', 'supports hillary', 'is a spam']

if uploaded_file:
    data = uploaded_file.readlines()
    def convert(tup):
        return f"{tup[0]}: {tup[1]:.2f}"
    i = st.sidebar.number_input("Choose a line number", min_value=0, max_value=len(data[0]))
    do_clear = st.sidebar.button("Clear eval stats")
    if "scores" not in st.session_state or do_clear:
        st.session_state["scores"] = {}
    if "machine_debate" not in st.session_state or do_clear:
        st.session_state["machine_debate"] = {}
    if "human_comment" not in st.session_state or do_clear:
        st.session_state["human_comment"] = {}
    options = {
        '(A): Excellent data point, can be attacked by some interesting perspectives': 3,
        '(B), Good data point, can be reasonably attacked but a little boring".': 2,
        '(C), The advice is not worth debating (too trivial or too deterministic to be debated': 1,
        '(D), Complete bullshit': 0,
    }

    if len(data) == 0:
        st.write("No data uploaded")
    else:
        st.header("Input data")
        i = int(i)
        line = json.loads(data[0])[i]
        col1, col2, col3 = st.columns(3)
        col1.metric(label="n", value=line["label_counter.n"])
        col2.metric(label="c", value=line["label_counter.c"])
        col3.metric(label="e", value=line["label_counter.e"])
        st.markdown("**Premise:** " + line["example.premise"])
        st.markdown("**Hypothesis:** " + line["example.hypothesis"])
        LIMIT_COMMENTS = 3
        for j in range(LIMIT_COMMENTS):
            try:
                st.markdown(f"**Comment {j+1}**:" + line["good_comments"][j]['body'])
            except:
                break
        # st.header("Gold label")
        # st.text(labels[i] if "label_processed" not in line else line["label_processed"])
        # st.header("Predicted label")
        # st.text(line[key_out])

        option = st.selectbox(
        "What do you want to do now?", ("view history (Please set to this status when changing line number)", "input new comments"))
        if option == "input new comments":
            st.session_state["scores"][i] = options[st.radio("Do you like model output? Choose a score", options.keys())]
            st.session_state["machine_debate"][i] = st.text_input("Machine generated debate:")
            st.session_state["human_comment"][i] = st.text_input("Human comment:")
        else:
            try:
                st.subheader("**History**")
                st.markdown("**machine debate generation:**")
                st.text(st.session_state["machine_debate"][i])
                st.markdown("**Human comment:**")
                st.text(st.session_state["human_comment"][i])
                #st.text(st.session_state["human_comment"])
            except:
                st.text("No History")

        #st.text(st.session_state["human_comment"][i])
        st.write(f"Average: {sum(st.session_state['scores'].values()) / len(st.session_state['scores']) if len(st.session_state['scores']) > 0 else 0 :.2f}, Count = {len(st.session_state['scores'])}")
        counter = Counter(st.session_state["scores"].values())
        for opt, i in options.items():
            st.write(f"{opt}: {counter[i] if i in counter else 0}")
        st.write(st.session_state["scores"])
        # if "top6_decoded" in line:
        #     st.header("Tokenwise top 6 probability breakdown")
        #     dataframe = pd.DataFrame({
        #         f"{i}-th Prediction": [convert(list(p.items())[i]) for p in line["top6_decoded"] if len(p) >= 6]
        #         for i in range(6)
        #     })
        #     st.dataframe(dataframe)
