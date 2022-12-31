import pandas as pd
import sqlite3

con = sqlite3.connect("currency.db")
currency_df = pd.read_csv("currency_rate.csv")
currency_df.to_sql("currency", con=con)
