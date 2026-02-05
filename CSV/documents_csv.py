import sqlite3
import csv
import logging
import logging.handlers

db_path = r'D:\Database\test_db/accounting.db'
file_path = r'D:\Nassim\csv\documents_202602040115.csv'

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

insert_exp = '''
             INSERT INTO documents
             (
             date,
             accDebit,
             accCredit,
             docSum,
             docNote,
             docStatus
             )
             VALUES(?, ?, ?, ?, ?, ?)'''

data_to_insert = []

try:
    for rec in reader:
        rec_data = ([
            rec[1],
            rec[2],
            rec[3],
            rec[4],
            rec[5],
            rec[6]
        ])
        logger.info(rec_data)
        data_to_insert.append(rec_data)

    cursor.executemany(insert_exp, data_to_insert)
    conn.commit()

except Exception as e:
    logger.error(e)
    print()




