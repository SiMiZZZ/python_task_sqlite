import pandas as pd
import sqlite3

vacancie_name = input("Введите название профессии: ")
con = sqlite3.connect("vacancies_db.db")

salary_by_years = pd.read_sql("""SELECT substr(published_at, 0, 5) AS year, AVG(salary) AS average_price 
FROM parsed_salary
GROUP BY substr(published_at, 0, 5)
LIMIT 17 OFFSET 1
""", con)
print(f"Динамика уровня зарплат по годам: \n{salary_by_years}")

quantity_by_years = pd.read_sql("""SELECT substr(published_at, 0, 5) AS year, COUNT(*) as quantity
FROM parsed_salary
GROUP BY substr(published_at, 0, 5)
LIMIT 17 OFFSET 1
""", con)

print(f"Динамика количества вакансий по годам: \n{quantity_by_years}")

salary_by_years_for_vacancy_name = pd.read_sql(f"""SELECT substr(published_at, 0, 5) AS year, ROUND(AVG(salary)) AS average_price
FROM parsed_salary
WHERE name LIKE '{vacancie_name}'
GROUP BY substr(published_at, 0, 5)
LIMIT 17 OFFSET 1
""", con)

print(f"Динамика уровня зарплат по годам для выбранной профессии: \n {salary_by_years_for_vacancy_name}")

quantity_by_years_for_vacancy_name = pd.read_sql(f"""SELECT substr(published_at, 0, 5) AS year, COUNT(*) as quantity
FROM parsed_salary
WHERE name LIKE '{vacancie_name}'
GROUP BY substr(published_at, 0, 5)
LIMIT 10
""", con)

print(f"Динамика уровня зарплат по годам для выбранной профессии: \n {quantity_by_years_for_vacancy_name}")

salary_by_cities = pd.read_sql(f"""SELECT area_name, AVG(salary)
FROM parsed_salary
GROUP BY area_name
ORDER BY AVG(salary) DESC 
LIMIT 10
""", con)

print(f"Уровень зарплат по городам: \n {salary_by_cities}")


share_by_cities = pd.read_sql(f"""SELECT area_name, COUNT(*)/{float(con.execute("SELECT COUNT(*) FROM parsed_salary").fetchone()[0])}*100 as share
FROM parsed_salary
GROUP BY area_name 
HAVING share>1
ORDER BY share DESC 
""", con)

print(f"Доля вакансий по городам : \n {share_by_cities}")
