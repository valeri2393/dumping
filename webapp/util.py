import pandas as pd
from datetime import datetime
from sqlite3 import Connection
from util.db import request_sql
from webapp.const import DATE_FORMAT


def get_last_date(conn: Connection):
    dates = [
        datetime.strptime(data[0], DATE_FORMAT) for data in
        request_sql(conn, "SELECT DISTINCT date FROM prices")
    ]
    dates.sort()
    last_date = dates[-1].strftime(DATE_FORMAT)
    return last_date


def get_types(conn: Connection, last_date: str):
    types = [
        data[0] for data in
        request_sql(
            conn=conn,
            query=f"""SELECT DISTINCT cards.type
                    FROM prices
                    LEFT JOIN cards ON prices.id=cards.id
                        WHERE prices.date = '{last_date}'"""
        )
    ]
    return types


def get_sql_list(lst: list):
    st = "'"
    for i in range(len(lst)):
        st += str(lst[i])
        if i != len(lst) - 1:
            st += str("', '")
        else:
            st += str("'")
    return st


def cell_styling(df: pd.DataFrame, red: list, green: list):
    df_styler = pd.DataFrame('', index=df.index, columns=df.columns)
    for i in red:
        df_styler.iloc[i[0], i[1]] = 'color: red'
    for i in green:
        df_styler.iloc[i[0], i[1]] = 'color: LimeGreen'
    return df_styler
