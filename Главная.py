# import pandas as pd
# import streamlit as st
# import sqlite3

# from util.config import build_config
# from util.db import request_sql
# from webapp.const import HEADER_FORMAT, SOURCE_FORMAT, sources
# from webapp.const import LINK_FORMAT
# from webapp.styles import set_style, color_pivot
# from webapp.util import get_last_date, get_types

# # Инициализация конфигурационного файла
# cfg = build_config('config.yaml')
# conn = sqlite3.connect(cfg["DBPath"])
# sb_pic_path = cfg["SBPicPath"]

# # Форматирование страницы по общему шаблону
# last_date = get_last_date(conn)
# set_style(sb_pic_path, last_date)
# types = get_types(conn, last_date)
# type = st.sidebar.radio("Выберите тип ресурса: ", types, horizontal=True)

# # Сводная таблица со средней скидкой
# st.markdown(
#     HEADER_FORMAT.format('Средний уровень цен по категориям и ресурсам'),
#     unsafe_allow_html=True
# )
# st.write(
#     """Числа в таблице показывают, на сколько % в среднем цены
#     <span style='color:red'>ниже</span> или
#     <span style='color:limegreen'>выше</span> РРЦ СТН.""",
#     unsafe_allow_html=True
# )
# pivot_query = f"""SELECT cards.resource, cards.category,
#             ROUND((SUM(prices.price)/SUM(analogues.price)-1)*100) AS perc
#             FROM prices
#             LEFT JOIN cards
#                 ON cards.id = prices.id
#             LEFT JOIN analogues
#                 ON cards.name_analogue = analogues.name_analogue
#             WHERE date = '{last_date}'
#                 AND cards.type = '{type}'
#                 AND cards.name_analogue <> 0
#                 AND prices.price <> 0
#             GROUP BY cards.category, cards.resource
#             ORDER BY cards.resource
#             """
# pivot = pd.pivot_table(
#     data=pd.DataFrame(
#         data=request_sql(conn, pivot_query),
#         columns=['Ресурс', 'Категория', '%']
#     ),
#     index="Категория",
#     columns="Ресурс",
#     values='%',
#     aggfunc="first",
#     fill_value=0
# ).astype(int)
# st.dataframe(
#     pivot.style.map(color_pivot, subset=list(pivot.columns))
# )
# st.write(
#     SOURCE_FORMAT.format(f"Источник: {sources[type]}"), unsafe_allow_html=True
# )

# # Таблица с ценами и ссылками
# st.markdown(
#     HEADER_FORMAT.format('Цены и ссылки'),
#     unsafe_allow_html=True
# )
# category = st.sidebar.radio(
#     label="Выберите категорию:",
#     options=list(pivot.index),
#     horizontal=False
# )
# query = f"""SELECT cards.resource, analogues.name_analogue,
#                 CAST(prices.price AS INT),
#                 CAST(analogues.price AS INT),
#                 CAST((prices.price/analogues.price-1)*100 AS INT),
#                 url
#             FROM prices
#             LEFT JOIN cards
#                 ON cards.id = prices.id
#             LEFT JOIN analogues
#                 ON cards.name_analogue = analogues.name_analogue
#             WHERE date = '{last_date}'
#                 AND cards.type = '{type}'
#                 AND cards.category = '{category}'
#                 AND cards.name_analogue <> 0
#                 AND prices.price <> 0
#             GROUP BY cards.resource, analogues.name_analogue
#             ORDER BY cards.resource, analogues.price
#             """
# data = pd.DataFrame(
#         data=request_sql(conn, query),
#         columns=['Ресурс', 'Аналог', '', 'Цена аналога', '%', 'url']
#     )

# # Форматирование ссылки в таблице
# for i in range(len(data)):
#     price = data.iloc[i, 2]
#     url = data.iloc[i, 5]
#     perc = data.iloc[i, 4]
#     color = 'limegreen' if perc >= 0 else 'red'
#     data.iloc[i, 2] = LINK_FORMAT.format(url, price, color, perc)
# df_prices = pd.pivot_table(
#     data=data,
#     index=['Аналог', 'Цена аналога'],
#     columns='Ресурс',
#     values=[''],
#     aggfunc='first',
#     fill_value=0
# )
# df_prices.columns = df_prices.columns.swaplevel(0, 1).map(' '.join)
# df_prices = df_prices.reindex(
#     labels=sorted(df_prices.columns),
#     axis=1
# ).sort_index(level=[1]).reset_index()
# df_prices = df_prices.reset_index(drop=True).style.\
#     applymap(
#             func=color_pivot,
#             subset=list(
#                     filter(
#                         lambda x: '%' in x,
#                         df_prices.columns
#                     )
#                 )
#         )

# with st.container():
#     st.write(
#         df_prices.to_html(
#             render_links=True,
#             escape=False),
#         unsafe_allow_html=True
#     )

import pandas as pd
import streamlit as st
import sqlite3

from util.config import build_config
from util.db import request_sql
from webapp.const import HEADER_FORMAT, SOURCE_FORMAT, sources
from webapp.const import LINK_FORMAT
from webapp.styles import set_style, color_pivot
from webapp.util import get_last_date, get_types

# Инициализация конфигурационного файла
cfg = build_config('config.yaml')
conn = sqlite3.connect(cfg["DBPath"])
sb_pic_path = cfg["SBPicPath"]

# Форматирование страницы по общему шаблону
last_date = get_last_date(conn)
set_style(sb_pic_path, last_date)
types = get_types(conn, last_date)

if types:  # Проверка, чтобы список типов не был пустым
    type = st.sidebar.radio("Выберите тип ресурса: ", types, horizontal=True)
else:
    type = None

# Проверяем, существует ли type в sources
source_text = sources.get(type, "Источник неизвестен")

# # Сводная таблица со средней скидкой
# st.markdown(
#     HEADER_FORMAT.format('Средний уровень цен по категориям и ресурсам'),
#     unsafe_allow_html=True
# )
# st.write(
#     """Числа в таблице показывают, на сколько % в среднем цены
#     <span style='color:red'>ниже</span> или
#     <span style='color:limegreen'>выше</span> РРЦ СТН.""",
#     unsafe_allow_html=True
# )

# # Запрос к базе данных
# if type:
#     pivot_query = f"""SELECT cards.resource, cards.category,
#                 ROUND((SUM(prices.price)/SUM(analogues.price)-1)*100) AS perc
#                 FROM prices
#                 LEFT JOIN cards
#                     ON cards.id = prices.id
#                 LEFT JOIN analogues
#                     ON cards.name_analogue = analogues.name_analogue
#                 WHERE date = '{last_date}'
#                     AND cards.type = '{type}'
#                     AND cards.name_analogue <> 0
#                     AND prices.price <> 0
#                 GROUP BY cards.category, cards.resource
#                 ORDER BY cards.resource
#                 """
#     pivot_data = request_sql(conn, pivot_query)
    
#     if pivot_data:
#         pivot = pd.pivot_table(
#             data=pd.DataFrame(
#                 data=pivot_data,
#                 columns=['Ресурс', 'Категория', '%']
#             ),
#             index="Категория",
#             columns="Ресурс",
#             values='%',
#             aggfunc="first",
#             fill_value=0
#         ).astype(int)
        
#         st.dataframe(
#             pivot.style.applymap(color_pivot, subset=list(pivot.columns))
#         )
#     else:
#         st.warning("Нет данных для отображения.")
# else:
#     st.error("Тип ресурса не выбран или отсутствует.")

# # Источник данных
# st.write(
#     SOURCE_FORMAT.format(f"Источник: {source_text}"), unsafe_allow_html=True
# )

# # Таблица с ценами и ссылками
# st.markdown(
#     HEADER_FORMAT.format('Цены и ссылки'),
#     unsafe_allow_html=True
# )

# if type and not pivot.empty:
#     category = st.sidebar.radio(
#         label="Выберите категорию:",
#         options=list(pivot.index),
#         horizontal=False
#     )

#     query = f"""SELECT cards.resource, analogues.name_analogue,
#                     CAST(prices.price AS INT),
#                     CAST(analogues.price AS INT),
#                     CAST((prices.price/analogues.price-1)*100 AS INT),
#                     url
#                 FROM prices
#                 LEFT JOIN cards
#                     ON cards.id = prices.id
#                 LEFT JOIN analogues
#                     ON cards.name_analogue = analogues.name_analogue
#                 WHERE date = '{last_date}'
#                     AND cards.type = '{type}'
#                     AND cards.category = '{category}'
#                     AND cards.name_analogue <> 0
#                     AND prices.price <> 0
#                 GROUP BY cards.resource, analogues.name_analogue
#                 ORDER BY cards.resource, analogues.price
#                 """
#     data = pd.DataFrame(
#         data=request_sql(conn, query),
#         columns=['Ресурс', 'Аналог', 'Цена', 'Цена аналога', '%', 'url']
#     )

#     # Форматирование ссылок в таблице
#     for i in range(len(data)):
#         price = data.iloc[i, 2]
#         url = data.iloc[i, 5]
#         perc = data.iloc[i, 4]
#         color = 'limegreen' if perc >= 0 else 'red'
#         data.iloc[i, 2] = LINK_FORMAT.format(url, price, color, perc)

#     if not data.empty:
#         df_prices = pd.pivot_table(
#             data=data,
#             index=['Аналог', 'Цена аналога'],
#             columns='Ресурс',
#             values=['Цена'],
#             aggfunc='first',
#             fill_value=0
#         )
#         df_prices.columns = df_prices.columns.swaplevel(0, 1).map(' '.join)
#         df_prices = df_prices.reindex(
#             labels=sorted(df_prices.columns),
#             axis=1
#         ).sort_index(level=[1]).reset_index()

#         df_prices = df_prices.style.applymap(
#             color_pivot,
#             subset=list(filter(lambda x: '%' in x, df_prices.columns))
# )

#         with st.container():
#             st.write(
#                 df_prices.to_html(render_links=True, escape=False),
#                 unsafe_allow_html=True
#             )
#     else:
#         st.warning("Нет данных для выбранной категории.")
# else:
#     st.warning("Выберите корректный тип ресурса и категорию.")
# Сводная таблица со средней скидкой
if type:
    pivot_query = f"""SELECT cards.resource, cards.category,
                ROUND((SUM(prices.price)/SUM(analogues.price)-1)*100) AS perc
                FROM prices
                LEFT JOIN cards
                    ON cards.id = prices.id
                LEFT JOIN analogues
                    ON cards.name_analogue = analogues.name_analogue
                WHERE date = '{last_date}'
                    AND cards.type = '{type}'
                    AND cards.name_analogue <> 0
                    AND prices.price <> 0
                GROUP BY cards.category, cards.resource
                ORDER BY cards.resource
                """
    pivot_data = request_sql(conn, pivot_query)
    
    if pivot_data:
        pivot = pd.pivot_table(
            data=pd.DataFrame(
                data=pivot_data,
                columns=['Ресурс', 'Категория', '%']
            ),
            index="Категория",
            columns="Ресурс",
            values='%',
            aggfunc="first",
            fill_value=0
        ).astype(int)
        
        st.dataframe(
            pivot.style.applymap(color_pivot, subset=list(pivot.columns))
        )
    else:
        st.warning("Нет данных для отображения.")
else:
    st.error("Тип ресурса не выбран или отсутствует.")

# Таблица с ценами и ссылками
if type and not pivot.empty:
    category = st.sidebar.radio(
        label="Выберите категорию:", 
        options=list(pivot.index), 
        horizontal=False
    )

    query = f"""SELECT cards.resource, analogues.name_analogue,
                    CAST(prices.price AS INT),
                    CAST(analogues.price AS INT),
                    CAST((prices.price/analogues.price-1)*100 AS INT),
                    url
                FROM prices
                LEFT JOIN cards
                    ON cards.id = prices.id
                LEFT JOIN analogues
                    ON cards.name_analogue = analogues.name_analogue
                WHERE date = '{last_date}'
                    AND cards.type = '{type}'
                    AND cards.category = '{category}'
                    AND cards.name_analogue <> 0
                    AND prices.price <> 0
                GROUP BY cards.resource, analogues.name_analogue
                ORDER BY cards.resource, analogues.price
                """
    data = pd.DataFrame(
        data=request_sql(conn, query),
        columns=['Ресурс', 'Аналог', 'Цена', 'Цена аналога', '%', 'url']
    )

    # Форматирование ссылок в таблице
    for i in range(len(data)):
        price = data.iloc[i, 2]
        url = data.iloc[i, 5]
        perc = data.iloc[i, 4]
        color = 'limegreen' if perc >= 0 else 'red'
        data.iloc[i, 2] = LINK_FORMAT.format(url, price, color, perc)

    if not data.empty:
        df_prices = pd.pivot_table(
            data=data,
            index=['Аналог', 'Цена аналога'],
            columns='Ресурс',
            values=['Цена'],
            aggfunc='first',
            fill_value=0
        )
        df_prices.columns = df_prices.columns.swaplevel(0, 1).map(' '.join)
        df_prices = df_prices.reindex(
            labels=sorted(df_prices.columns),
            axis=1
        ).sort_index(level=[1]).reset_index()

        df_prices = df_prices.style.applymap(
            color_pivot,
            subset=list(filter(lambda x: '%' in x, df_prices.columns))
        )

        with st.container():
            st.write(
                df_prices.to_html(render_links=True, escape=False),
                unsafe_allow_html=True
            )
    else:
        st.warning("Нет данных для выбранной категории.")
else:
    st.warning("Выберите корректный тип ресурса и категорию.")