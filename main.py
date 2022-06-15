import streamlit as st
import json
import pandas as pd
import sys
import numpy as np
import random
from utils import *

st.title("chaosNLI")

jsonFile_snli = "chaosNLI_v1.0/chaosNLI_snli.jsonl"
jsonFile_mnli = "chaosNLI_v1.0/chaosNLI_mnli_m.jsonl"
jsonFile_anli = "chaosNLI_v1.0/chaosNLI_alphanli.jsonl"
snli = flatten_nested_json_df(pd.read_json(jsonFile_snli, lines=True))
mnli = flatten_nested_json_df(pd.read_json(jsonFile_mnli, lines=True))
if st.checkbox('Show raw data'):
    snli

st.header("Dataset")
selection = st.radio('Pick Dataset', ['snli', 'mnli'])
nli = snli if selection == 'snli' else mnli

mnli.fillna(0)
st.subheader("Statistics")
col1, col2, col3 = st.columns(3)
col1.metric("Neutral", round(nli['label_counter.n'].mean(), 2))
col2.metric("Contradiction", round(nli['label_counter.c'].mean(), 2))
col3.metric("Entailment", round(nli['label_counter.e'].mean(), 2))


st.subheader("Data points filtered by labels")
x = st.slider("neutral labels less than", value=20)
y = st.slider("entailment labels more than")
z = st.slider("contradiction labels more than")
t = st.slider("difference between entailment and contradiction less than", value=20)

st.metric("Count", len(nli[(nli['label_counter.n'] <= x) & (nli['label_counter.e'] >= y)
& (nli['label_counter.c'] >= z) & (abs(nli["label_counter.e"] - nli['label_counter.c']) <= t)]))
inspect(nli, (nli['label_counter.n'] <= x) & (nli['label_counter.e'] >= y)
& (nli['label_counter.c'] >= z) & (abs(nli["label_counter.e"] - nli['label_counter.c']) <= t))

