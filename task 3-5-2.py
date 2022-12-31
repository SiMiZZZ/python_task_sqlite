import sqlite3

import pandas as pd
from numpy import nan
from datetime import datetime
import requests


def make_dict_from_lists(lst_keys, lst_values):
    return {lst_keys[i]: lst_values[i] for i in range(0, len(lst_keys), 1)}


def set_salary(row, currency_con):
    salary = 0
    if pd.isnull(row.salary_from) and pd.isnull(row.salary_to):
        return nan
    elif not pd.isnull(row.salary_from) and pd.isnull(row.salary_to):
        salary = row.salary_from
    elif pd.isnull(row.salary_from) and not pd.isnull(row.salary_to):
        salary = row.salary_to
    else:
        salary = (row.salary_from + row.salary_to)/2
    currency = row.salary_currency
    if currency not in currency_list:
        return   False
    if currency != "RUR":
        if pd.isnull(row.published_at):
            return False
        date = row.published_at[:7]
        request = rf"select * from currency where date = '{date}'"
        currency_con.row_factory = sqlite3.Row
        currency_row = currency_con.execute(request).fetchone()
        if pd.isnull(currency_row[currency]):
            return False
        currency_to_rur = currency_row[currency] * salary
        return currency_to_rur
    return currency

df = pd.read_csv("vacancies_dif_currencies.csv")
parsed_df = pd.DataFrame(columns=["name", "salary", "area_name", "published_at"])
counter = 0
pd_currency = pd.read_csv('currency_rate.csv')
connection = sqlite3.connect("vacancies_db.db")
currency_list = list(pd_currency.columns)
data_dict = {"name": [], "salary": [], "area_name": [], "published_at": []}
for index, row in df.iterrows():
    salary = set_salary(row, connection)
    if salary == False:
        continue
    new_row = {"name": row["name"], "salary": salary, "area_name": row.area_name, "published_at": row.published_at}
    data_dict["name"].append(row["name"])
    data_dict['salary'].append(salary)
    data_dict['area_name'].append(row.area_name)
    data_dict['published_at'].append(row.published_at)
    if index%1000==0:
        print(index)
parsed_df = pd.DataFrame.from_dict(data_dict)
parsed_df.to_csv("parsed_salary.csv", index=False)
parsed_df.to_sql("parsed_salary", con=connection)
