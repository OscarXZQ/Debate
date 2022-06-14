import streamlit as st
import json
import pandas as pd
import sys
import numpy as np
import random
from utils import *

# def flatten_nested_json_df(df):

#     df = df.reset_index()

#     print(f"original shape: {df.shape}")
#     print(f"original columns: {df.columns}")


#     # search for columns to explode/flatten
#     s = (df.applymap(type) == list).all()
#     list_columns = s[s].index.tolist()

#     s = (df.applymap(type) == dict).all()
#     dict_columns = s[s].index.tolist()

#     print(f"lists: {list_columns}, dicts: {dict_columns}")
#     while len(list_columns) > 0 or len(dict_columns) > 0:
#         new_columns = []

#         for col in dict_columns:
#             print(f"flattening: {col}")
#             # explode dictionaries horizontally, adding new columns
#             horiz_exploded = pd.json_normalize(df[col]).add_prefix(f'{col}.')
#             horiz_exploded.index = df.index
#             df = pd.concat([df, horiz_exploded], axis=1).drop(columns=[col])
#             new_columns.extend(horiz_exploded.columns) # inplace

# #         for col in list_columns:
# #             print(f"exploding: {col}")
# #             # explode lists vertically, adding new columns
# #             df = df.drop(columns=[col]).join(df[col].explode().to_frame())
# #             new_columns.append(col)

#         # check if there are still dict o list fields to flatten
#         s = (df[new_columns].applymap(type) == list).all()
#         list_columns = s[s].index.tolist()

#         s = (df[new_columns].applymap(type) == dict).all()
#         dict_columns = s[s].index.tolist()

#         print(f"lists: {list_columns}, dicts: {dict_columns}")

#     print(f"final shape: {df.shape}")
#     print(f"final columns: {df.columns}")
#     return df

# def inspect(nli, clause):
#     #st.write(nli[clause])
#     st.write(nli[clause][["example.premise", "example.hypothesis", 'label_counter.n', 'label_counter.c', 'label_counter.e']])

# def need_comment(item):
#     count[0] += 1
#     st.write("Premise: ", item["example.premise"])
#     st.write("Hypothesis: ", item["example.hypothesis"])
#     # st.text_input("Good Data Point or Not")
#     # st.text_input("Comments")
#     st.selectbox('Data Point Quality' + str(count[0]), ['Bad', 'Neutral', "Good"])

st.title("chaosNLI")

jsonFile_snli = "chaosNLI_v1.0/chaosNLI_snli.jsonl"
jsonFile_mnli = "chaosNLI_v1.0/chaosNLI_mnli_m.jsonl"
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

