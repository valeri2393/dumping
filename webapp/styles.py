import streamlit as st
import pandas as pd

from base64 import b64encode


def set_style(sb_pic_path: str, last_date: str):
    pd.set_option('display.max_colwidth', 10)
    st.set_page_config(page_title="СТН Демпинг", page_icon="", layout="wide")
    with open(sb_pic_path, "rb") as f:
        pic_bin_string = b64encode(f.read()).decode()
    st.markdown(
        """
            <style>
                [data-testid="stSidebarNav"] {
                    background-image: url("data:image/png;base64,%s");
                    background-repeat: no-repeat;
                    background-position: %s;
                    margin-top: %s;
                    background-size: %s;
                }
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                button {visibility: hidden;}
                div.block-container{padding-top:1rem;}
            </style>
            """
        % (pic_bin_string, "50% 10%", "5%", "80%"),
        unsafe_allow_html=True
    )
    st.sidebar.write(f"Последнее обновление: {last_date}")


def color_pivot(val):
    if -100 < val < 0:
        color = 'red'
    elif val == 0:
        color = 'white'
    else:
        color = 'limegreen'
    return 'color: %s' % color


def hide_null(val):
    if val == 0:
        color = 'white'
    else:
        color = 'black'
    return 'color : %s' % color


def make_clickable(val):
    price, url = str(val).split('##')
    return f'<a target="_blank" href="{url}">{price}</a>'
