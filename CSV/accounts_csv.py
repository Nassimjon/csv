import sqlite3
import csv
import logging
import logging.handlers

db_path = r'D:\Database\test_db\accounting.db'
file_path = r'D:\Nassim\csv\accounts_202602040056.csv'

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

logger = logging.getLogger('accounts')
logger.setLevel(logging.INFO)

log_handler = logging.handlers.RotatingFileHandler(
    "Logs\load_from_csv.log",
    maxBytes=1000000
)

log_format = logging.Formatter(
    "%(asctime)s %(levelname)s %(message)s"
)

log_handler.setFormatter(log_format)
logger.addHandler(log_handler)

file_csv = open(file_path, 'r', encoding='UTF-8')
reader = csv.reader(file_csv)
header = next(reader)

create_table = '''
  CREATE TABLE IF NOT EXISTS accounts
  (
  account TEXT,
  customer_id INTEGER,
  accType TEXT,
  accRest REAL
  );
  '''

try:
    cursor.execute(create_table)
    conn.commit()
    logger.info("Table accounts successfully created")
except Exception as e:
    logger.error("Error creating table", exc_info=True)


insert_exp = '''
             INSERT INTO accounts
             (
             account,
             customer_id,
             accType,
             accRest
             )
             VALUES(?, ?, ?, ?)'''

data_to_insert = []

try:
    for rec in reader:
        rec_data = ([
            rec[0],
            rec[1],
            rec[2],
            rec[3]
        ])
        logger.info(rec_data)
        data_to_insert.append(rec_data)

    cursor.executemany(insert_exp, data_to_insert)
    conn.commit()

except Exception as e:
    print(e)
    logger.error(e)




