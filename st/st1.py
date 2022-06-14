import streamlit as st
import json
import pandas as pd
import sys
import numpy as np
import random
sys.path.append("../")
from utils import *
count = [0]

def inspect(nli, clause):
    #st.write(nli[clause])
    st.write(nli[clause][["example.premise", "example.hypothesis", 'label_counter.n', 'label_counter.c', 'label_counter.e']])

def need_comment(item):
    count[0] += 1
    st.write("Premise: ", item["example.premise"])
    st.write("Hypothesis: ", item["example.hypothesis"])
    # st.text_input("Good Data Point or Not")
    # st.text_input("Comments")
    st.selectbox('Data Point Quality' + str(count[0]), ['Bad', 'Neutral', "Good"])

st.title("chaosNLI")

jsonFile_snli = "../chaosNLI_v1.0/chaosNLI_snli.jsonl"
jsonFile_mnli = "../chaosNLI_v1.0/chaosNLI_mnli_m.jsonl"
jsonFile_anli = "chaosNLI_v1.0/chaosNLI_alphanli.jsonl"
snli = flatten_nested_json_df(pd.read_json(jsonFile_snli, lines=True))
mnli = flatten_nested_json_df(pd.read_json(jsonFile_mnli, lines=True))
# snli["label_counter.c"].fillna(0)
# snli["label_counter.e"].fillna(0)
# snli["label_counter.n"].fillna(0)
# snli["label_counter.c"], snli["label_counter.e"], snli["label_counter.n"] = snli["label_counter.c"].astype(int), snli["label_counter.e"].astype(int), snli["label_counter.n"].astype(int)
mnli.fillna(0)
st.header("Statistics")
col1, col2, col3 = st.columns(3)
col1.metric("Neutral", round(snli['label_counter.n'].mean(), 2))
col2.metric("Contradiction", round(snli['label_counter.c'].mean(), 2))
col3.metric("Entailment", round(snli['label_counter.e'].mean(), 2))


st.header("Data points filtered by labels")
x = st.slider("neutral labels less than")
y = st.slider("entailment labels more than")
z = st.slider("contradiction labels more than")
t = st.slider("difference between entailment and contradiction less than")
inspect(snli, (snli['label_counter.n'] <= x) & (snli['label_counter.e'] >= y)
& (snli['label_counter.c'] >= z) & (abs(snli["label_counter.e"] - snli['label_counter.c']) <= t))

