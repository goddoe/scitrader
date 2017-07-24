from pprint import pprint
import time
import pymysql
import pickle
import configparser
from datetime import datetime
from config.db_config import mysql_config as db_conf

def get_connection(auto_commit=True):
    """
    with SSHTunnelForwarder(('127.0.0.2'\n22)\nssh_password='SERVER_PASSWORD'\nssh_username='root'\nremote_bind_address=('127.0.0.3'\n3306)) as server:
        conn = MySQLdb.connect(host='127.0.0.1'\nport=server.local_bind_port\nuser='MYSQL_USER'\npasswd='MYSQL_PASSWORD')
        cursor = conn.cursor()
    """

    conn = pymysql.connect(host=db_conf['host'],
                                user=db_conf['user'],
                                password=db_conf['passwd'],
                                db=db_conf['db'],
                                charset=db_conf['charset'],
                                cursorclass=pymysql.cursors.DictCursor,
                                autocommit=auto_commit)

    return conn


class ModelStock(object):

    def __init__(self):
        for i in range(10):
            self.conn = get_connection()
            if self.conn != None:
                break
            time.sleep(1)
    
    def __del__(self):
        self.conn.close()

    def insert_stock_dict_list_amount(self, stock_dict_list ):
        sql = """
                INSERT INTO stock(`date`,
                                  `open` , `high` , `low` , `close` , 
                                  `volume` , `diff_last` , `change` , `money` , 
                                  `credit_rate` , `individual_amount` , `corporation_amount` , `foreign_amount`, 
                                  `foreign_side_amount`, `program_amount`, `foreign_rate`, `volume_power`, 
                                  `credit_balance_rate`)
                VALUES (%s, 
                        %s,%s,%s,%s,
                        %s,%s,%s,%s,
                        %s,%s,%s,%s,
                        %s,%s,%s,%s,
                        %s)
                
        """
        try:
            with self.conn.cursor() as cursor:
                for stock_dict in stock_dict_list:
                    cursor.execute(sql, (stock_dict['date'],
                                            stock_dict['open'], stock_dict['high'], stock_dict['low'],stock_dict['close'], 
                                            stock_dict['volume'], stock_dict['diff_last'],stock_dict['change'], stock_dict['money'], 
                                            stock_dict['credit_rate'], stock_dict['individual_amount'], stock_dict['corporation_amount'],stock_dict['foreign_amount'], 
                                            stock_dict['foreign_side_amount'], stock_dict['program_amount'], stock_dict['foreign_rate'], stock_dict['volume_power'], 
                                            stock_dict['credit_balance_rate']
                                        ))

        except Exception as e:
            print(e)

    
    def update_stock_dict_list_money(self, stock_dict_list ):
        sql = """
                UPDATE stock
                SET `individual_money`= %s, `corporation_money`=%s, `foreign_side_money`=%s, `program_money`=%s        
                WHERE `date` = %s
                """

        try:
            with self.conn.cursor() as cursor:
                for stock_dict in stock_dict_list:
                    cursor.execute(sql, (
                                            stock_dict['individual_money'], stock_dict['corporation_money'], 
                                            stock_dict['foreign_side_money'], stock_dict['program_money'],
                                            stock_dict['date'],  
                                        ))
        except Exception as e:
            print("="*30)
            print("update sotck_dict list money error")
            print(e)
 
                
if __name__ == '__main__':

    stock_dict_list = [{
        'open':10, 'high':10, 'low':10, 'close':10, 
                                  'volume':10, 'diff_last':10, 'change':10, 'money':10, 
                                  'credit_rate':10, 'individual_money':10, 'individual_amount':10, 'corporation_money':10, 
                                  'corporation_amount':10, 'foreign_amount':10, 'foreign_side_money':10, 'foreign_side_amount':10, 
                                  'program_money':10, 'program_amount':10, 'foreign_rate':10, 'volume_power':10, 
                                  'corporation_net_buying_money':10, 'corporation_net_buying_amount':10, 'individual_net_buying_money':10, 'individual_net_buying_amount':10, 
                                  'credit_balance_rate':10
    }]


    model_stock = ModelStock()
    model_stock.insert_stock_by_day_dict_list(stock_dict_list)
