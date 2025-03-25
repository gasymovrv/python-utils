from datetime import timedelta
from urllib.parse import urlparse

import matplotlib.dates as mdates
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
SELECT DATE_TRUNC('hour', created_at) as "hour" FROM customer_request
WHERE created_at between '2024-09-11 00:00:00' and '2024-09-11 23:59:59'
and owner_group_id = '318b646c-cad6-41b2-824d-8a00522d72e5'
ORDER BY "hour"
LIMIT 500000
""")
rows = cursor.fetchall()
rows = [row[0] for row in rows]

fig, ax = plt.subplots()
ax.hist(rows, bins=24, edgecolor="black")
ax.set_title("Количество обращений создаваемых за 11.09.2024 сгруппированное по часам")
ax.set_xlim((rows[0], rows[-1]))
ax.set_xlabel('created_at truncated to hours')
ax.set_ylabel('count')

# Set custom x-tick labels
hours = [f'{hour:02d}' for hour in range(24)]
ax.set_xticks([mdates.date2num(rows[0] + timedelta(hours=i)) for i in range(24)])
ax.set_xticklabels(hours)

plt.show()
connection.close()
