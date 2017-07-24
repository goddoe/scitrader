import sys
import time
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QAxContainer import *

from db_model.model_stock import ModelStock
from libs.various_utils import generate_id_with_date

def preprocess_stock_raw(data):
    result = ""
    if '--' in data :
        result = data.replace('--','-')
    elif '-' in data:
        result = data.replace('-','')
    elif data == '':
        result = None
    else:
        result = data
    return result
        

def convert_stock_data_raw_amount(stock_data):
    target_dict = {}
    field_list = ['date','open','high','low',
                    'close','diff_last','change','volume',
                    'money','credit_rate','individual_amount', 'corporation_amount',
                    'foreign_amount', 'foreign_side_amount','program_amount', 'foreign_rate',
                    'volume_power', 'foreign_rate_2', 'foreign_rate_3','foreign_amount_2',
                    'corporation_2','individual_2', 'credit_balance_rate']
    
    for i, data  in enumerate(stock_data):
        target_dict[field_list[i]] = preprocess_stock_raw(data)

    return target_dict

def convert_stock_data_raw_money(stock_data):
    target_dict = {}
    field_list = ['date','open','high','low',
                    'close','diff_last','change','volume',
                    'money','credit_rate','individual_money', 'corporation_money',
                    'foreign_amount', 'foreign_side_money','program_money', 'foreign_rate',
                    'volume_power', 'foreign_rate_2', 'foreign_rate_3','foreign_amount_2',
                    'corporation_2','individual_2', 'credit_balance_rate']
    for i, data  in enumerate(stock_data):
        target_dict[field_list[i]] = preprocess_stock_raw(data)
    
    return target_dict

def convert_stock_data_raw_amount_list_to_dict_list(stock_data_list_amount):
    stock_data_list = []
    for stock_data_amount in stock_data_list_amount:
        stock_data = convert_stock_data_raw_amount(stock_data_amount)
        stock_data_list.append(stock_data)
    return stock_data_list

def convert_stock_data_raw_money_list_to_dict_list(stock_data_list_money):
    stock_data_list = []
    for stock_data_money in stock_data_list_money:
        stock_data = convert_stock_data_raw_money(stock_data_money)
        stock_data_list.append(stock_data)
    return stock_data_list


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.set_ui()
        self.login()
        self.set_controller()

    def set_controller(self):
        self.model_stock = ModelStock()

    def login(self):
        self.kiwoom = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.kiwoom.CommConnect()

        self.kiwoom.OnEventConnect.connect(self.event_connect)
        self.kiwoom.OnReceiveTrData.connect(self.receive_trdata)

    def set_ui(self):
        # connect to kiwoom
        self.setWindowTitle("Robo Trader")
        self.setGeometry(150, 150 ,600,600)

        ## geting
        # stock code
        self.label = QLabel("종목코드: ")

        self.code_edit = QLineEdit()
        self.code_edit.setText("039490")

        # get
        self.btn1 = QPushButton("조회")
        self.btn1.clicked.connect(self.btn1_clicked)
        self.text_edit = QTextEdit()
        self.text_edit.setEnabled(False)

        layout_get_stock_info = QVBoxLayout()
        layout_get_stock_info.addWidget(self.label)
        layout_get_stock_info.addWidget(self.code_edit)
        layout_get_stock_info.addWidget(self.btn1)
        layout_get_stock_info.addWidget(self.text_edit)

        ## get account info 
        self.account_label = QLabel("account info")
        self.btn_account = QPushButton("get account")
        self.btn_account.clicked.connect(self.btn_account_clicked)
        self.text_edit_account = QTextEdit()
        self.text_edit_account.setEnabled(False)
        layout_get_account_info = QVBoxLayout()
        layout_get_account_info.addWidget(self.account_label)
        layout_get_account_info.addWidget(self.btn_account)
        layout_get_account_info.addWidget(self.text_edit_account)

        ## get stock names
        self.label_stock = QLabel("stock names")
        self.btn_stock = QPushButton("get stock names")
        self.btn_stock.clicked.connect(self.btn_clicked_stock)
        self.list_widget_stock = QListWidget()
        layout_get_stock = QVBoxLayout()
        layout_get_stock.addWidget(self.label_stock)
        layout_get_stock.addWidget(self.btn_stock)
        layout_get_stock.addWidget(self.list_widget_stock)

        ## get stock data
        self.label_stock_data = QLabel("stock data")
        self.text_edit_code_stock_data = QLineEdit('005930')
        self.text_edit_date_stock_data = QLineEdit('20170525')
        self.text_edit_flag_stock_data = QLineEdit()
        self.btn_stock_data = QPushButton("get stock data")
        self.btn_stock_data.clicked.connect(self.btn_clicked_stock_data)

        layout_get_stock = QVBoxLayout()
        layout_get_stock.addWidget(self.label_stock_data)
        layout_get_stock.addWidget(self.text_edit_code_stock_data)
        layout_get_stock.addWidget(self.text_edit_date_stock_data)
        layout_get_stock.addWidget(self.text_edit_flag_stock_data)
        layout_get_stock.addWidget(self.btn_stock_data)

        ## Global layout
        layout_main = QHBoxLayout()
        layout_main.addLayout(layout_get_stock_info)
        layout_main.addLayout(layout_get_account_info)
        layout_main.addLayout(layout_get_stock)
        self.setLayout(layout_main)

    def event_connect(self, err_code):
        if err_code == 0:
            self.text_edit.append("login success")
    
    def btn_clicked_stock_data(self):

        code = self.text_edit_code_stock_data.text()
        date = self.text_edit_date_stock_data.text()
        
        self.req_stock_data(code, date, 'amount')


    def req_stock_data(self, code, date, flag='amount'):
        flag_num = 0
        if flag == 'amount':
            flag_num = 0
        elif flag == 'money':
            flag_num = 1
        else:
            print("flag is wrong : you set flag like [{}] ".format(flag))

        self.kiwoom.SetInputValue("종목코드", code)
        self.kiwoom.SetInputValue("조회일자", date)
        self.kiwoom.SetInputValue("표시구분", str(flag_num))
        self.kiwoom.CommRqData("opt10086_{}_req".format(flag), "opt10086", 0, "0101")


    def btn_clicked_stock(self):
        ret = self.kiwoom.GetCodeListByMarket('0')
        kospi_code_list = ret.split(';')
        kospi_code_name_list = []

        for x in kospi_code_list:
            name = self.kiwoom.GetMasterCodeName(x)
            kospi_code_name_list.append(x + " : " + name)
        self.list_widget_stock.addItems(kospi_code_name_list)
    
    def btn_account_clicked(self):
        account_num = self.kiwoom.GetLoginInfo("ACCNO")
        self.text_edit_account.setText(str(account_num))

    def btn1_clicked(self):
        code = self.code_edit.text()

        self.text_edit.append("종목 코드"+ code)
        self.kiwoom.SetInputValue("종목코드", code)
        self.kiwoom.CommRqData("opt10001_req", "opt10001",0,"0101")

    def receive_trdata(self, screen_no, rqname, trcode, recordname, prev_next, data_len, err_code, msg1, msg2):
        if rqname == 'opt10001_req':
            name = self.kiwoom.CommGetData(trcode, "", rqname, 0, "종목명")
            volume = self.kiwoom.CommGetData(trcode, "", rqname, 0, "거래량")
            self.text_edit.append("종목명: "+name.strip())
            self.text_edit.append("거래량: "+volume.strip())
        if rqname == 'opt10086_amount_req':
            stock_data_list_amount_raw = self.kiwoom.GetCommDataEx(trcode, "일별주가")
            stock_data_list_amount = convert_stock_data_raw_amount_list_to_dict_list(stock_data_list_amount_raw)
            self.model_stock.insert_stock_dict_list_amount(stock_data_list_amount)

            code = self.text_edit_code_stock_data.text()
            first_date = stock_data_list_amount[0]['date']
            self.req_stock_data(code, first_date, 'money')

        if rqname =='opt10086_money_req':
            stock_data_list_money_raw = self.kiwoom.GetCommDataEx(trcode, "일별주가")
            print(stock_data_list_money_raw[0])
            stock_data_list_money = convert_stock_data_raw_money_list_to_dict_list(stock_data_list_money_raw)
            self.model_stock.update_stock_dict_list_money(stock_data_list_money)
            
    

if __name__=='__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    app.exec_()
