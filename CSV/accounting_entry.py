import sqlite3
import logging
import logging.handlers

db_path = r'D:\Database\test_db/accounting.db'

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


query_acc = 'SELECT * FROM accounts'
cursor.execute(query_acc)
acc = cursor.fetchall()

logger.info(f'accounts is {acc}')

def selectAccRest(acc):

    sel_exp = 'SELECT accRest FROM accounts where account = \'' + acc + '\''
    cursor.execute(sel_exp)

    accRest_val = cursor.fetchone()[0]
    logger.info(f'adeline   {accRest_val}')
    # print('adeline ', accRest_val)
    print(f'sel_exp {sel_exp}')
    return accRest_val

def updateAccRest(new_val, acc):

    up_exp = 'UPDATE accounts SET accRest = ' + str(new_val) + ' WHERE account = \'' + acc + '\''

    try:
        cursor.execute(up_exp)
        conn.commit()
        return 1
    except Exception as e:
        logger.error(f' errrrrrr {e}')
        return 0

query_doc = 'SELECT * FROM documents'
cursor.execute(query_doc)
docs = cursor.fetchall()

logger.info(f'documents is {docs}')

bank_acc = '10101972000100000001'
try:
    for d in docs:

        if d[2] == bank_acc:
            print('Приход на кассу')

            # получаем значение accRest для accCredit
            accRest = selectAccRest(d[3])
            accRestBank = selectAccRest(d[2])

            newValBank = accRestBank + d[4]
            updateAccRest(newValBank, d[2])


            newVal = accRest + d[4]
            updateAccRest(newVal, d[3])

            print('old val ', accRest)
            print('sum is ', d[4])
            print('new val ', newVal)

        elif d[2][-4:] == d[3][-4:]:
            print('Между своими счетами')


            frstAccRest = selectAccRest(d[2])
            secAccRest = selectAccRest(d[3])

            new_value_frst = frstAccRest - d[4]
            updateAccRest(new_value_frst, d[2])

            new_val_sec = secAccRest + d[4]
            updateAccRest(new_val_sec, d[3])

            print('sum is', d[4])
            print('old val firstAcc ', frstAccRest)
            print('new val firstAcc', new_value_frst)
            print('\n')
            print('old val secAcc ', secAccRest)
            print('new val srcAcc ', new_val_sec)



        elif d[3] == bank_acc:
            print('Расход через кассу')

            accRest = selectAccRest(d[2])
            accRestBank = selectAccRest(d[3])

            newVal = accRest - d[4]
            updateAccRest(newVal, d[2])

            newValBank = accRestBank - d[4]
            updateAccRest(newValBank, d[3])

            print('sum is', d[4])
            print('old val accRest ', accRest)
            print('new val accRest', newVal)
            print('\n')
            print('old val accRestBank ', accRestBank)
            print('new val accRestBank ', newValBank)

            print('stop')
except Exception as e:
    logger.error(e)
    print(e)




