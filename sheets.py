import gspread
import datetime
from oauth2client.service_account import ServiceAccountCredentials


def make_state(ident_num, man_num):
    link = ['https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive']
    my_creds = ServiceAccountCredentials.from_json_keyfile_name('uncommited/creds.json', link)
    client = gspread.authorize(my_creds)
    sheet = client.open('States').sheet1
    transaction = [str(datetime.datetime.now()), ident_num, man_num]
    sheet.append_row(transaction)
