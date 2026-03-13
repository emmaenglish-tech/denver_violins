import streamlit as st
import  gspread
from gspread_dataframe import get_as_dataframe

# dataframe import utils
def get_data_from_gsheets(sheet_name, gc):
    sheet = gc.open(sheet_name)
    worksheet = sheet.sheet1
    df = get_as_dataframe(worksheet, evaluate_formulas=True)
    final_df = df.dropna(axis=0, how='all').copy()
    return final_df