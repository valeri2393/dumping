
import altair as alt
import pandas as pd
import streamlit as st
import sqlite3
from datetime import datetime

from util.config import build_config
from util.db import request_sql
from webapp.const import HEADER_FORMAT, DATE_FORMAT, SOURCE_FORMAT
from webapp.const import CHART_FORMAT
from webapp.styles import set_style
from webapp.util import get_last_date, get_types, get_sql_list, cell_styling

# Инициализация конфигурационного файла
cfg = build_config('config.yaml')
conn = sqlite3.connect(cfg["DBPath"])
sb_pic_path = cfg["SBPicPath"]

# Форматирование страницы по общему шаблону
last_date = get_last_date(conn)
set_style(sb_pic_path, last_date)
types = get_types(conn, last_date)
type = st.sidebar.radio("Выберите тип ресурса: ", types, horizontal=True)

# Выбор ресурса
resources = [
    data[0] for data in
    request_sql(
        conn=conn,
        query=f"""SELECT DISTINCT resource FROM cards WHERE type = '{type}'"""
    )
]
resource = st.sidebar.radio(
    label="Выберите ресурс:",
    options=resources,
    horizontal=False
)

# Выбор дат
dates = [
        datetime.strptime(data[0], DATE_FORMAT) for data in
        request_sql(
            conn=conn,
            query=f"""SELECT DISTINCT prices.date FROM prices
                    LEFT JOIN cards ON prices.id = cards.id
                    WHERE cards.type = '{type}'
                        AND cards.resource = '{resource}'
                    """
        )
]

# График изменения цен на ресурсе
st.markdown(
    HEADER_FORMAT.format(f'Динамика изменения цен. Ресурс: {resource}'),
    unsafe_allow_html=True
)
if len(dates) > 1:
    dates.sort()
    dates = [date.strftime(DATE_FORMAT) for date in dates]
    start_date, end_date = st.select_slider(
        label="Выберите даты",
        options=dates,
        value=[dates[0], dates[-1]]
    )
    choose_dates = dates[
        dates.index(start_date):dates.index(end_date)+1
    ]
    st.write(
        SOURCE_FORMAT.format(
            "Линии на графике показывают ежедневную динамику изменения %"
            " скидки продавца относительно РРЦ СТН по категориям товаров."
        ) +
        CHART_FORMAT.format(resource, start_date, end_date),
        unsafe_allow_html=True
    )
    query = f"""SELECT cards.category, prices.date,
            ROUND((SUM(prices.price)/SUM(analogues.price)-1)*100)
            FROM prices
            LEFT JOIN cards
                ON cards.id = prices.id
            LEFT JOIN analogues
                ON cards.name_analogue = analogues.name_analogue
            WHERE date in ({get_sql_list(choose_dates)})
                AND cards.type = '{type}'
                AND cards.resource = '{resource}'
                AND cards.name_analogue <> 0
                AND prices.price <> 0
            GROUP BY cards.category, prices.date"""
    data = pd.DataFrame(
        [
            [
                el[0],
                datetime.strptime(el[1], DATE_FORMAT),
                el[2]
            ]
            for el in request_sql(conn, query)
        ],
        columns=['Категория', 'Дата', '%']
    )
    data.sort_values(by='Дата', inplace=True)
    data["Дата_"] = [x.strftime(DATE_FORMAT) for x in data['Дата']]
    chart = alt.Chart(data).mark_line(point=True).encode(
        x=alt.X('Дата_', sort=list(data["Дата"])),
        y='%',
        color='Категория',
    ).interactive()
    st.altair_chart(chart, use_container_width=True)

    # Изменение цен по позициям
    st.markdown(
        HEADER_FORMAT.format(f'Цены {resource} с {start_date} по {end_date}'),
        unsafe_allow_html=True
    )
    categories = data["Категория"].unique()
    category = st.radio(
        label="Выберите категорию: ",
        options=categories,
        horizontal=True
    )
    query = f"""SELECT analogues.name_analogue, prices.date,
            CAST(analogues.price AS INT),
            CAST(prices.price AS INT)
            FROM prices
            LEFT JOIN cards
                ON cards.id = prices.id
            LEFT JOIN analogues
                ON cards.name_analogue = analogues.name_analogue
            WHERE date in ({get_sql_list(choose_dates)})
                AND cards.type = '{type}'
                AND cards.resource = '{resource}'
                AND cards.category = '{category}'
                AND cards.name_analogue <> 0
                AND prices.price <> 0
            GROUP BY analogues.name_analogue, prices.date
            ORDER BY analogues.price"""
    data = pd.DataFrame(
        data=request_sql(conn, query),
        columns=['Аналог', 'Дата', 'Цена аналога', 'Цена']
    )
    data['Дата'] = data['Дата'].apply(
        lambda x: datetime.strptime(x, DATE_FORMAT)
    )
    data = pd.pivot_table(
        data=data,
        values='Цена',
        index=['Аналог', 'Цена аналога'],
        columns='Дата',
        aggfunc='first',
        fill_value=0
    )
    data.columns = [x.strftime(DATE_FORMAT) for x in data.columns]
    data.sort_index(level=[1], inplace=True)
    red_cells = []
    green_cells = []
    for i in range(len(data)):
        for j in range(1, data.shape[1]):
            if data.iloc[i, j] < data.iloc[i, j-1]:
                red_cells.append([i, j])
            elif data.iloc[i, j] > data.iloc[i, j-1]:
                green_cells.append([i, j])

    data = data.style.apply(
        cell_styling,
        red=red_cells,
        green=green_cells,
        axis=None
    )
    st.dataframe(data)
else:
    st.write(
        SOURCE_FORMAT.format("Нет данных"), unsafe_allow_html=True
    )
