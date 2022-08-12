# import schedule
import pymysql


def connect_to_db(values):
    db = pymysql.connect(host='sql5.freemysqlhosting.net',
                         port=3306,
                         user='sql5512433',
                         password='t5C64F47sP',
                         db='sql5512433',
                         charset='utf8mb4',
                         autocommit=True,
                         cursorclass=pymysql.cursors.DictCursor
                         )
    cursor = db.cursor()
    query = '''insert into `survey` (`account_id`, `Did the tool help you improve your performance`, `How relevant were the inputs you received during your game`, `What your experience with MOBAs`, `What your experience with Dota 2`,
     `Comment`) values (%s,%s,%s,%s,%s,%s) '''
    cursor.execute(query, values)
    db.commit()
