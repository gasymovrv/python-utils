from urllib.parse import urlparse

import psycopg2 as ps
from pylab import *

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
SELECT DATE_TRUNC('day', created_at) as d, count(1) FROM customer_request
WHERE status = 'IN_PROGRESS' 
and created_at > '2024-09-01 00:00:00'
and owner_group_id = '318b646c-cad6-41b2-824d-8a00522d72e5'
GROUP BY d
ORDER BY d
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
ax.set_xlabel('created_at truncated to days')
ax.set_ylabel('count')
ax.set_title('Количество открытых обращений на текущий момент сгруппированное по дням создания')

plt.show()
connection.close()
