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

def selectAccRest( acc ):

    sel_exp = 'SELECT accRest FROM accounts where account = \'' + acc + '\''
    cursor.execute(sel_exp)

    accRest_val = cursor.fetchone()[0]
    logger.info(f'adeline   {accRest_val}')
    print('adeline ', accRest_val)
    return accRest_val


query_doc = 'SELECT * FROM documents'
cursor.execute(query_doc)
docs = cursor.fetchall()

logger.info(f'documents is {docs}')


bank_acc = '10101972000100000001'
try:
    for d in docs:

        if d[2] == bank_acc:

            # print('first acc is bank ')
            # accRest = 'SELECT accRest FROM accounts where account = \'' + d[3] + '\''


            accRest = selectAccRest(d[3])
            print('selecr_row  ', accRest)

            # cursor.execute(accRest)
            # accRest_tulpe = cursor.fetchone()
            # accRest_val = accRest_tulpe[0]

            new_value = accRest + d[4]
            print('old val ', accRest)
            print('sum is ', d[4])
            print('new val ', new_value)
            update_exp = 'UPDATE accounts SET accRest = ' + str(new_value) + ' WHERE account = \'' + d[3] + '\''
            # print(update_exp)
            cursor.execute(update_exp)
            conn.commit()

            logger.info(accRest)

        elif d[2][-4:] == d[3][-4:]:
            print('d2 is', d[2][-4:])
            print('sum is', d[4])
            print('d3 is', d[3][-4:])
            frstAccRest = 'SELECT accRest FROM accounts where account = \'' + d[2] + '\''
            secAccRest  = 'SELECT accRest FROM accounts where account = \'' + d[3] + '\''
            print('secAccRest', secAccRest)
            cursor.execute(frstAccRest)

            accRest_tulpe = cursor.fetchone()
            frstAccRest_val = accRest_tulpe[0]
            new_value = frstAccRest_val - d[4]
            print('old val ', frstAccRest_val)
            print('new val ', new_value)
            upFrstAcc = 'UPDATE accounts SET accRest = ' + str(new_value) + ' WHERE account = \'' + d[2] + '\''
            print('update_first_account  ', upFrstAcc)
            cursor.execute(upFrstAcc)

            cursor.execute(secAccRest)
            secAccRest_tulpe = cursor.fetchone()
            secAccRest_val = secAccRest_tulpe[0]
            print('secAccRest_val is  ', secAccRest_val)
            new_val_sec = secAccRest_val + d[4]
            upSectAcc = 'UPDATE accounts SET accRest = ' + str(new_val_sec) + ' WHERE account = \'' + d[3] + '\''
            print('second account ', upSectAcc)
            cursor.execute(upSectAcc)
            conn.commit()

            print('here is nothing')
        elif d[3] == bank_acc:

            print('stop')
except Exception as e:
    logger.error(e)
    print(e)




