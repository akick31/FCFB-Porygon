import gspread
import xlrd
import pathlib
xlrd.xlsx.ensure_elementtree_imported(False, None)
xlrd.xlsx.Element_has_iter = True
from oauth2client.service_account import *

"""
Handle contacting Google Sheets and getting information from the document

@author: apkick
"""

proj_dir = str(pathlib.Path(__file__).parent.absolute().parent.absolute())

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name(proj_dir + '/configuration/FCFBRollCallBot-2d263a255851.json', scope)
gc = gspread.authorize(credentials)
sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1ZFi4MqxWX84-VdIiWjJmuvB8f80lfKNkffeKcdJKtAU/edit#gid=1106595477')
fbs_worksheet = sh.worksheet("Season 8 Rankings (All-Time)")

file_location = proj_dir + "/configuration/FCSElo.xlsx"
fcs_excel = xlrd.open_workbook(file_location)
sheet = fcs_excel.sheet_by_name('sheet')

def get_elo_data():
    """
    Get Elo data from both FBS and FCS sheets

    :return:
    """

    try:
        team_elo_column = []
        elo_data_column = []
        fbs_column = fbs_worksheet.col_values(2)
        fbs_column.pop(0)
        fcs_column = get_excel_data(3)
        fcs_column.pop(0)
        team_elo_column.extend(fbs_column)
        team_elo_column.extend(fcs_column)

        fbs_elo_column = fbs_worksheet.col_values(3)
        fbs_elo_column.pop(0)
        fcs_elo_column = get_excel_data(0)
        fcs_elo_column.pop(0)
        elo_data_column.extend(fbs_elo_column)
        elo_data_column.extend(fcs_elo_column)
        
        return {1: team_elo_column, 2: elo_data_column}
    except Exception as e:
        return_statement = "The following error occured: " + str(e)
        return return_statement


def get_excel_data(column):
    """
    Get a column from the excel spreadsheet

    :param column:
    :return:
    """

    column_vals = []
    for row_num in range(sheet.nrows):
        column_vals.append(str(sheet.cell(row_num, column).value))
    return column_vals


