import psycopg2 as ps
from pylab import *
from urllib.parse import urlparse

# TODO: change connection url
result = urlparse("postgresql://user:pass@host1:5435,host2:5435,host3:5435/dbname")
username = result.username
password = result.password
database = result.path[1:]
hostname = result.hostname

connection = ps.connect(
    host=hostname,
    port=5435,
    user=username,
    password=password,
    database=database
)

cursor = connection.cursor()

cursor.execute("""
SELECT DATE_TRUNC('hour', created_at) as "hour", count(1) FROM customer_request
WHERE created_at between '2024-10-01 00:00:00' and '2024-10-06 23:59:59'
and owner_group_id = '318b646c-cad6-41b2-824d-8a00522d72e5'
GROUP BY "hour"
ORDER BY "hour"
""")

rows = cursor.fetchall()

# Dates
x = []
# Counts
y = []

for row in rows:
    x.append(row[0])
    y.append(row[1])

fig, ax = plt.subplots()
ax.plot(x, y)
ax.set_xlabel('created_at truncated to hours')
ax.set_ylabel('count')
ax.set_title('Количество обращений создаваемых за период с 01.10.2024 по 06.10.2024 сгруппированное по часам')

plt.show()
connection.close()
