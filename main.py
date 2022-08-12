import sys
import time
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QLabel, QLineEdit, QTextEdit, \
    QGridLayout, QPushButton, QMainWindow, QFormLayout, QVBoxLayout, QHBoxLayout, QRadioButton, QGroupBox, QCheckBox, \
    QButtonGroup, \
    QMessageBox
from steam.client import SteamClient
from PyQt5.QtCore import QObject, pyqtSignal, QThread, pyqtRemoveInputHook, Qt
from dotenv import load_dotenv
import os
import requests
from datetime import datetime
from functools import partial
import schedule

import insert_db
from model_function import MopaModel
import gspread
import os

# load_dotenv()

# API_KEY = os.getenv('API_KEY')


class QWorker(QThread):
    show_message = pyqtSignal(str)
    error_msg = pyqtSignal(str)

    def __init__(self, model, parent=None):
        super(QWorker, self).__init__(parent=parent)
        self.active_thread = True
        self.model = model

        schedule.every(1).minutes.do(self.get_predicted_data)

    def get_predicted_data(self):
        self.model.get_match_info()
        info = self.model.info
        if info:
            if info.get('error') == 1:
                self.error_msg.emit('Could not connect. Please check your internet connection.')
            if info.get('error') == 3:
                self.error_msg.emit('Rate Limit Exceeded.')
            else:
                input_params = [34, info['hero_id'], info['item_0'], info['item_1'], info['item_2'], info['item_3'],
                                info['item_4'], info['item_5'],
                                info['gold']]
                y = MopaModel([input_params])
                if y:
                    self.show_message.emit('The predicted item is %s' % ''.join(y))
                else:
                    self.show_message.emit('The predicted item is %s' % ''.join(y))
        else:
            self.error_msg.emit('Unable to pull values.')

    def run(self):
        # try:
        while True:
            time.sleep(2)
            schedule.run_pending()
            '''
                The List of features are "time", "hero_id","item_0",
                "item_1","item_2","item_3","item_4","item_5","gold_t"
                '''

    def stop(self):
        self.active_thread = False
        self.wait()


class Window3(QMainWindow):
    def __init__(self, steamid):
        super().__init__()
        self.steamid = steamid
        self.setWindowTitle("Survey Questions")
        self.init_gui()
        self.setFixedWidth(800)
        self.setFixedHeight(500)
        self.move(200, 200)
        self.show()
        self.survey = {
            'accountid': steamid,
            'question1': '',
            'question2': '',
            'question3': '',
            'question4': '',
            'comments': ''
        }

    def init_gui(self):
        wid = QWidget(self)
        self.setCentralWidget(wid)
        vbox = QVBoxLayout()
        group2 = QGroupBox('Survey')
        survey1 = QLabel('1. Did the tool help you improve your performance?')
        survey1.setStyleSheet('font-weight: bold')
        survey2 = QLabel('2. How relevant were the inputs you received during your game?')
        survey2.setStyleSheet('font-weight: bold')
        survey3 = QLabel('3. What’s your experience with MOBAs (League of Legends, Dota 2, Smite etc.)?')
        survey3.setStyleSheet('font-weight: bold')
        survey4 = QLabel('4. What’s your experience with Dota 2?')
        survey4.setStyleSheet('font-weight: bold')
        survey5 = QLabel('Comments (Optional)')
        survey5.setStyleSheet('font-weight: bold')
        self.submitbtn = QPushButton('Submit')
        self.submitbtn.setFixedWidth(300)
        self.submitbtn.setFixedHeight(50)
        self.submitbtn.clicked.connect(self.insert)
        self.comments = QTextEdit()
        self.comments.setFixedWidth(500)
        self.comments.setFixedHeight(100)
        self.radiobtn1 = QRadioButton('Strongly Disagree')
        self.radiobtn2 = QRadioButton('Disagree')
        self.radiobtn3 = QRadioButton('Neutral')
        self.radiobtn4 = QRadioButton('Agree')
        self.radiobtn5 = QRadioButton('Strongly Agree')

        self.radiobtn21 = QRadioButton('Very Irrelevant')
        self.radiobtn22 = QRadioButton('Irrelevant')
        self.radiobtn23 = QRadioButton('Neutral')
        self.radiobtn24 = QRadioButton('Relevant')
        self.radiobtn25 = QRadioButton('Very Relevant')

        self.radiobtn31 = QRadioButton('Beginner')
        self.radiobtn32 = QRadioButton('Intermediate')
        self.radiobtn33 = QRadioButton('Veteran')

        self.radiobtn34 = QRadioButton('Relevant')
        self.radiobtn35 = QRadioButton('Very Relevant')
        self.radiobtn34.setHidden(True)
        self.radiobtn35.setHidden(True)
        self.radiobtn41 = QRadioButton('Beginner')
        self.radiobtn42 = QRadioButton('Intermediate')
        self.radiobtn43 = QRadioButton('Veteran')
        self.radiobtn44 = QRadioButton('Relevant')
        self.radiobtn45 = QRadioButton('Very Relevant')
        self.radiobtn44.setHidden(True)
        self.radiobtn45.setHidden(True)

        self.radiobtngroup1 = QButtonGroup()
        function_1 = partial(self.button_click, 1)
        self.radiobtngroup1.buttonClicked.connect(function_1)
        self.radiobtngroup1.addButton(self.radiobtn1)
        self.radiobtngroup1.addButton(self.radiobtn2)
        self.radiobtngroup1.addButton(self.radiobtn3)
        self.radiobtngroup1.addButton(self.radiobtn4)
        self.radiobtngroup1.addButton(self.radiobtn5)
        self.radiobtngroup2 = QButtonGroup()
        function_2 = partial(self.button_click, 2)
        self.radiobtngroup2.buttonClicked.connect(function_2)
        self.radiobtngroup2.addButton(self.radiobtn21)
        self.radiobtngroup2.addButton(self.radiobtn22)
        self.radiobtngroup2.addButton(self.radiobtn23)
        self.radiobtngroup2.addButton(self.radiobtn24)
        self.radiobtngroup2.addButton(self.radiobtn25)

        self.radiobtngroup3 = QButtonGroup()
        function_3 = partial(self.button_click, 3)
        self.radiobtngroup3.buttonClicked.connect(function_3)
        self.radiobtngroup3.addButton(self.radiobtn31)
        self.radiobtngroup3.addButton(self.radiobtn32)
        self.radiobtngroup3.addButton(self.radiobtn33)
        self.radiobtngroup3.addButton(self.radiobtn34)
        self.radiobtngroup3.addButton(self.radiobtn35)

        self.radiobtngroup4 = QButtonGroup()
        function_4 = partial(self.button_click, 4)
        self.radiobtngroup4.buttonClicked.connect(function_4)
        self.radiobtngroup4.addButton(self.radiobtn41)
        self.radiobtngroup4.addButton(self.radiobtn42)
        self.radiobtngroup4.addButton(self.radiobtn43)
        self.radiobtngroup4.addButton(self.radiobtn44)
        self.radiobtngroup4.addButton(self.radiobtn45)
        hbox5 = QHBoxLayout()
        hbox6 = QHBoxLayout()
        hbox7 = QHBoxLayout()
        hbox8 = QHBoxLayout()
        hbox9 = QHBoxLayout()
        vbox2 = QVBoxLayout()
        vbox2.addWidget(survey1)
        hbox5.addWidget(self.radiobtn1)
        hbox5.addWidget(self.radiobtn2)
        hbox5.addWidget(self.radiobtn3)
        hbox5.addWidget(self.radiobtn4)
        hbox5.addWidget(self.radiobtn5)
        hbox6.addWidget(self.radiobtn21)
        hbox6.addWidget(self.radiobtn22)
        hbox6.addWidget(self.radiobtn23)
        hbox6.addWidget(self.radiobtn24)
        hbox6.addWidget(self.radiobtn25)
        hbox7.addWidget(self.radiobtn31)
        hbox7.addWidget(self.radiobtn32)
        hbox7.addWidget(self.radiobtn33)
        hbox7.addWidget(self.radiobtn34)
        hbox7.addWidget(self.radiobtn35)
        hbox8.addWidget(self.radiobtn41)
        hbox8.addWidget(self.radiobtn42)
        hbox8.addWidget(self.radiobtn43)
        hbox8.addWidget(self.radiobtn44)
        hbox8.addWidget(self.radiobtn45)
        # hbox9.addWidget(self.comments)
        # hbox9.addWidget(self.submitbtn)
        vbox2.addLayout(hbox5)
        vbox2.addWidget(survey2)
        vbox2.addLayout(hbox6)
        vbox2.addWidget(survey3)
        vbox2.addLayout(hbox7)
        vbox2.addWidget(survey4)
        vbox2.addLayout(hbox8)
        vbox2.addWidget(survey5)
        vbox2.addWidget(self.comments)
        vbox2.addWidget(self.submitbtn)
        group2.setLayout(vbox2)
        vbox.addWidget(group2)
        wid.setLayout(vbox)

    def button_click(self, val):
        self.survey.update({'question%d' % val: self.radiobtngroup1.checkedButton().text()})

    def insert(self):
        self.survey.update({'comments': self.comments.toPlainText()})
        values = [self.survey['accountid'], self.survey['question1'],
                  self.survey['question2'], self.survey['question3'],
                  self.survey['question4'], self.survey['comments']]
        insert_db.connect_to_db(values)


        # print('Writing to google sheet...')
        # scopes = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        #
        # secret_file = os.path.join(os.getcwd(), 'client_secret.json')
        # # spreadsheet_id = '1ijhVk-2QIZIAKDhcNYNn00Bvd5I0hNVkocRRBKqTGGI'
        # spreadsheet_id = '110114557187-l1hlgr7b9ul975sdl56h1macd7cv47ut'
        #
        # update_exception = True
        # exc_count = 0
        #
        # while update_exception and exc_count < 5:
        #     try:
        #         sa = gspread.service_account(filename=secret_file, scopes=scopes)
        #         sh = sa.open_by_key(spreadsheet_id)
        #         ws = sh.worksheet('Survey')
        #         ws.clear()
        #         ws.update(row_values)
        #         update_exception = False
        #     except Exception as e:
        #         print(e)
        #         update_exception = True
        #         exc_count += 1
        #         time.sleep(10)

        print(self.survey)


class Window2(QWidget):
    def __init__(self, api_key, steam_id):
        super().__init__()
        self.setWindowTitle("Steam")
        self.api_key = api_key
        self.steamid = steam_id
        self.set_window()


    def get_match_info(self):
        API_KEY = self.api_key
        self.info = {}
        steamid = self.steamid

        response = None
        error = 2
        try:
            url = f'https://api.opendota.com/api/matches/{steamid}?api_key={API_KEY}'.format(steamid, API_KEY)
            response = requests.get(url)
        except requests.exceptions.ConnectionError:
            error = 1

        game_mode = ''
        start_time = ''
        item_0 = ''
        item_1 = ''
        item_2 = ''
        item_3 = ''
        item_4 = ''
        item_5 = ''
        hero_id = ''
        gold = ''

        if response:
            data = response.json()
            if 'error' not in data:
                game_mode = data.get('game_mode')
                start_time = datetime.fromtimestamp(data.get('start_time')).strftime('%Y-%m-%d %H:%M:%S %p')
                if 'players' in data:
                    players = data.get('players')
                    if players:
                        players = players[0]
                        item_0 = players.get('item_0')
                        item_1 = players.get('item_1')
                        item_2 = players.get('item_2')
                        item_3 = players.get('item_3')
                        item_4 = players.get('item_4')
                        item_5 = players.get('item_5')
                        hero_id = players.get('hero_id')
                        gold = players.get('gold')
            else:
                error = 3

        self.info = {
            'steamid': steamid,
            'game_mode': game_mode,
            'start_time': start_time,
            'item_0': item_0,
            'item_1': item_1,
            'item_2': item_2,
            'item_3': item_3,
            'item_4': item_4,
            'item_5': item_5,
            'hero_id': hero_id,
            'gold': gold,
            'error': error
        }
        return self.info

    def refresh_data(self):
        players = self.get_match_info()
        game_mode = str(players.get('game_mode'))
        start_time = str(players.get('start_time'))
        item_0 = str(players.get('item_0'))
        item_1 = str(players.get('item_1'))
        item_2 = str(players.get('item_2'))
        item_3 = str(players.get('item_3'))
        item_4 = str(players.get('item_4'))
        item_5 = str(players.get('item_5'))
        hero_id = str(players.get('hero_id'))
        gold = str(players.get('gold'))
        self.line_edit1.setText(str(players.get('steamid')))
        self.line_edit2.setText(start_time)
        self.line_edit3.setText(hero_id)
        self.line_edit4.setText(item_0)
        self.line_edit5.setText(item_1)
        self.line_edit6.setText(item_2)
        self.line_edit7.setText(item_3)
        self.line_edit8.setText(item_4)
        self.line_edit11.setText(item_5)
        self.line_edit10.setText(game_mode)
        self.line_edit9.setText(gold)
        if players.get('error') == 1:
            self.error_msg.setText('Could not connect. Please check your internet connection.')
        if players.get('error') == 3:
            self.error_msg.setText('Rate Limit Exceeded.')

    def remove_session(self):

        self.w1 = Window3(self.steamid)

        self.w1.init_gui()

    def set_window(self):
        max_width = 300
        max_height = 40
        win = QWidget()
        # self.steamid = '1419600384'
        players = self.get_match_info()
        self.steamid = str(players.get('steamid'))
        game_mode = str(players.get('game_mode'))
        start_time = str(players.get('start_time'))
        item_0 = str(players.get('item_0'))
        item_1 = str(players.get('item_1'))
        item_2 = str(players.get('item_2'))
        item_3 = str(players.get('item_3'))
        item_4 = str(players.get('item_4'))
        item_5 = str(players.get('item_5'))
        hero_id = str(players.get('hero_id'))
        gold = str(players.get('gold'))

        vbox = QVBoxLayout()
        hbox1 = QHBoxLayout()
        hbox2 = QHBoxLayout()
        group1 = QGroupBox()
        group1.setFixedWidth(600)
        # group3 = QGroupBox()
        hbox3 = QHBoxLayout()
        hbox4 = QHBoxLayout()

        hbox3.addWidget(group1)
        # hbox4.addWidget(group3)
        hbox1.addLayout(hbox3)
        hbox1.addLayout(hbox4)

        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)

        self.show_not = QCheckBox('Show')

        self.show_not.setChecked(False)

        self.show_not.clicked.connect(self.toggle_check)

        self.error_msg = QLabel('')
        self.error_msg.setStyleSheet('color: red; font-weight: bold')
        self.msg = QMessageBox()
        form1 = QFormLayout()
        label = QLabel('Match ID')
        label1 = QLabel('Hero ID')
        label1.setStyleSheet("color: black; font-weight: bold")
        label2 = QLabel('Item 0')
        label2.setStyleSheet("color: black; font-weight: bold")
        label3 = QLabel('Item 1')
        label3.setStyleSheet("color: black; font-weight: bold")
        label4 = QLabel('Item 2')
        label4.setStyleSheet("color: black; font-weight: bold")
        label5 = QLabel('Item 3')
        label5.setStyleSheet("color: black; font-weight: bold")
        label6 = QLabel('Item 4')
        label6.setStyleSheet("color: black; font-weight: bold")
        label7 = QLabel('Gold')
        label7.setStyleSheet("color: black; font-weight: bold")
        label8 = QLabel('Game Mode')
        label8.setStyleSheet("color: black; font-weight: bold")
        label9 = QLabel('Item 5')
        label9.setStyleSheet("color: black; font-weight: bold")
        self.line_edit3 = QLineEdit(hero_id)
        self.line_edit3.setStyleSheet("color: black;  border-radius: 2px; font-size: 16px")
        self.line_edit3.setFixedWidth(max_width)
        self.line_edit3.setFixedHeight(max_height)
        self.line_edit4 = QLineEdit(item_0)
        self.line_edit4.setStyleSheet("color: black;  border-radius: 2px; font-size: 16px")
        self.line_edit4.setFixedWidth(max_width)
        self.line_edit4.setFixedHeight(max_height)
        self.line_edit5 = QLineEdit(item_1)
        self.line_edit5.setStyleSheet("color: black;  border-radius: 2px; font-size: 16px")
        self.line_edit5.setFixedWidth(max_width)
        self.line_edit5.setFixedHeight(max_height)
        self.line_edit6 = QLineEdit(item_2)
        self.line_edit6.setStyleSheet("color: black;  border-radius: 2px; font-size: 16px")
        self.line_edit6.setFixedWidth(max_width)
        self.line_edit6.setFixedHeight(max_height)
        self.line_edit7 = QLineEdit(item_3)
        self.line_edit7.setStyleSheet("color: black;  border-radius: 2px; font-size: 16px")
        self.line_edit7.setFixedWidth(max_width)
        self.line_edit7.setFixedHeight(max_height)
        self.line_edit8 = QLineEdit(item_4)
        self.line_edit8.setStyleSheet("color: black;  border-radius: 2px; font-size: 16px")
        self.line_edit8.setFixedWidth(max_width)
        self.line_edit8.setFixedHeight(max_height)
        self.line_edit9 = QLineEdit(gold)
        self.line_edit9.setStyleSheet("color: black;  border-radius: 2px; font-size: 16px")
        self.line_edit9.setFixedWidth(max_width)
        self.line_edit9.setFixedHeight(max_height)
        self.line_edit10 = QLineEdit(game_mode)
        self.line_edit10.setStyleSheet("color: black;  border-radius: 2px; font-size: 16px")
        self.line_edit10.setFixedWidth(max_width)
        self.line_edit10.setFixedHeight(max_height)
        self.line_edit11 = QLineEdit(item_5)
        self.line_edit11.setStyleSheet("color: black;  border-radius: 2px; font-size: 16px")
        self.line_edit11.setFixedWidth(max_width)
        self.line_edit11.setFixedHeight(max_height)
        self.line_edit1 = QLineEdit(str(self.steamid))
        self.line_edit1.setFixedWidth(max_width)
        self.line_edit1.setStyleSheet("color: black;  border-radius: 2px; font-size: 16px")
        self.line_edit1.setFixedHeight(max_height)
        self.line_edit2 = QLineEdit(start_time)
        self.line_edit2.setStyleSheet("color: black; border-radius: 2px; font-size: 16px")
        self.line_edit2.setFixedWidth(max_width)
        self.line_edit2.setFixedHeight(max_height)
        start_time = QLabel('Start Time')
        start_time.setStyleSheet("color: black; font-weight: bold")
        label.setStyleSheet("color: black; font-weight: bold")
        self.refresh = QPushButton('Refresh')
        self.refresh.clicked.connect(self.refresh_data)

        self.refresh.setFixedHeight(40)
        form1.addRow(label, self.line_edit1)
        form1.addRow(start_time, self.line_edit2)
        form1.addRow(label1, self.line_edit3)
        form1.addRow(label2, self.line_edit4)
        form1.addRow(label3, self.line_edit5)
        form1.addRow(label4, self.line_edit6)
        form1.addRow(label5, self.line_edit7)
        form1.addRow(label6, self.line_edit8)
        form1.addRow(label9, self.line_edit11)
        form1.addRow(label7, self.line_edit9)
        form1.addRow(label8, self.line_edit10)
        self.logout = QPushButton('Logout')
        self.logout.setFixedHeight(40)
        self.logout.setFixedWidth(200)
        self.logout.clicked.connect(self.remove_session)

        form1.addRow(self.refresh, self.logout)
        form1.addRow(self.show_not)
        form1.addRow(self.error_msg)
        form2 = QFormLayout()
        # group3.setFixedHeight(500)

        if players.get('error') == 1:
            self.error_msg.setText('Unable to connect. Please check your internet connection.')

        if players.get('error') == 3:
            self.error_msg.setText('Rate Limit Exceeded.')

        # self.estEdit = QTextEdit()
        # self.estEdit.setEnabled(False)
        # form2.addRow(self.show_not)
        # form2.addRow(self.estEdit)
        # form2.addRow(self.error_msg)
        # form2.addRow(self.logout)
        # group3.setLayout(form2)
        group1.setLayout(form1)

        self.setLayout(vbox)

    def estimate_items(self, message):
        self.msg.setText(message)
        self.msg.exec_()

    def display_error(self, message):
        self.error_msg.setText(message)

    def toggle_check(self):
        if self.show_not.isChecked():
            # self.estEdit.setEnabled(True)
            self.worker = QWorker(self)
            self.worker.get_predicted_data()
            self.worker.start()
            self.worker.show_message.connect(self.estimate_items)
            self.worker.error_msg.connect(self.display_error)
            self.worker.get_predicted_data()
            '''
            Run ML algo
            '''
        else:
            self.error_msg.setText('Prediction Pop up Stopped.')
            schedule.clear()
            # self.estEdit.setEnabled(False)


class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Login')
        self.resize(500, 350)
        self.center()
        self.add_widgets()
        self.show()

    def add_widgets(self):

        user = QLabel('Username')
        password = QLabel('Password')
        self.error = QLabel()
        self.userEdit = QLineEdit()
        self.userEdit.setFixedHeight(40)
        self.passEdit = QLineEdit()
        self.passEdit.setFixedHeight(40)
        self.email_code = QLabel('API Key')
        self.emailEdit = QLineEdit()
        self.emailEdit.setFixedHeight(40)
        self.api_key = None
        if os.path.exists('api_key.txt'):
            self.api_key = open('api_key.txt', 'r', encoding='utf-8').read()
            self.api_key = self.api_key.strip()

        if self.api_key:
            self.emailEdit.setText(self.api_key)

        self.submit = QPushButton('Login')
        self.submit.setFixedWidth(100)
        self.submit.clicked.connect(self.window2)
        grid = QGridLayout()
        grid.setSpacing(1)

        grid.addWidget(user, 1, 0)
        grid.addWidget(self.userEdit, 1, 1)

        grid.addWidget(password, 2, 0)
        grid.addWidget(self.passEdit, 2, 1)

        # grid.addWidget(submit, 3, 0)

        grid.addWidget(self.email_code, 3, 0)
        grid.addWidget(self.emailEdit, 3, 1)
        grid.addWidget(self.submit, 4, 1)
        grid.addWidget(self.error, 5, 1)

        self.setLayout(grid)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def user_login(self):
        self.w = Window2(api_key=self.emailEdit.text(), steam_id='')
        self.w.setFixedWidth(800)
        self.w.setFixedHeight(800)
        self.w.move(500, 100)
        self.w.show()
        # self.w.api_key = self.emailEdit.text()
        print(self.emailEdit.text())
        if self.emailEdit.text() != '':
            with open('api_key.txt', 'w', encoding='utf-8') as f:
                f.write(self.emailEdit.text())

        if self.userEdit.text() != '' and self.passEdit.text() != '':
            client = SteamClient()
            try:
                client.cli_login(username=self.userEdit.text(), password=self.passEdit.text())
                self.w.steamid = client.steam_id.id
            except:
                self.error.setText('Could not connect.')
        else:
            self.error.setText('Fields Missing.')
        self.hide()

    def window2(self):
        # print(self.emailEdit.text())
        # self.thread = QWorker(self)
        # self.thread.start()
        # self.thread.login.connect(self.user_login)
        # try:

        self.user_login()
        # except:
        #     self.error.setWordWrap(True)
        #     self.error.setStyleSheet('color: red; font-weight: bold')
        #     self.error.setText('Unable to Connect. Please check your internet connection.')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    pyqtRemoveInputHook()
sys.exit(app.exec_())
