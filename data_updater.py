#!/usr/bin/env python
from datetime import datetime
import unittest
import os
import json
import gspread
from oauth2client.client import SignedJwtAssertionCredentials


OAUTH2TOKEN_FILE = 'oauth2token.json'
START_CELL = 'B3'


class DataUpdater:
    """Updater for Google spreadsheet"""

    def __init__(self):
        self.book = None
        self.gc = None
        self.error_message = ''
        self.initialized = False
        self.current_cell = ''

    def __del__(self):
        del self.book
        del self.gc

    def _set_current_cell(self, cell):
        """This function is for testing only"""
        self.current_cell = cell

    def _get_current_cell(self, date):
        if self.current_cell:
            return self.current_cell

        d = datetime.now()
        if date:
            d = date

        ww = self.get_cell_value(START_CELL)
        curr_ww = "ww{:02d}".format(d.isocalendar()[1])
        if ww != curr_ww:
            self.error_message = "Invalid week: {}, expected {}".format(ww, curr_ww)
            return None

        row, col = self.work_sheet.get_int_addr(START_CELL)
        col += 1    # data starts next to ww name

        col += d.weekday()
        cell = self.work_sheet.get_addr_int(row, col)
        return cell

    def init(self):
        token = os.environ.get('GSHEET_TOKEN')
        if token:
            json_key = json.loads(token)
        else:
            f = open(OAUTH2TOKEN_FILE)
            json_key = json.load(f)
            f.close()
        scope = ['https://spreadsheets.google.com/feeds']
        credentials = SignedJwtAssertionCredentials(json_key['client_email'],
                                                    json_key['private_key'].encode(), scope)

        gc = gspread.authorize(credentials)
        if not gc:
            return None

        book = gc.open('Catch ups')
        if not book:
            return None

        work_sheet = book.worksheet('CatchUps')
        if not work_sheet:
            return None

        self.initialized = True
        self.gc = gc
        self.book = book
        self.work_sheet = work_sheet

        return True

    def get_cell_value(self, cell):
        if not self.initialized:
            self.error_message = "DataUpdater is not initialized"
            return ''

        return self.work_sheet.acell(cell).value

    def add_value(self, value, date):
        if not self.initialized:
            self.error_message = "DataUpdater is not initialized"
            return False

        cell = self._get_current_cell(date)
        if not cell:
            self.error_message = "Error defining cell for updating"
            return False

        # input_value return text representation of cell data
        # for formula in would be like '=2+3+5'
        curr_value = self.work_sheet.acell(cell).input_value
        if not curr_value:
            curr_value = '='
        else:
            curr_value += '+'
        self.work_sheet.update_acell(cell, curr_value + str(value))

        return int(self.work_sheet.acell(cell).value)

    def get_error_message(self):
        return self.error_message


class t_DataUpdater(unittest.TestCase):
    """Tests for DataUpdater"""
    def test_init(self):
        du = DataUpdater()
        du.init()
        self.assertNotEqual(None, du, msg='Check object initialization')

    def test_init_err_msg(self):
        du = DataUpdater()
        du.init()
        self.assertEqual('', du.get_error_message(), msg='Check initial error message')

    def test_get_cell_value(self):
        du = DataUpdater()
        du.init()
        self.assertEqual('ww/day', du.get_cell_value('B2'), msg='Check get_cell_value()')

    def test_add_value(self):
        du = DataUpdater()
        du.init()
        inc = 3
        du._set_current_cell('N1')
        curr = int(du.get_cell_value('N1'))
        self.assertEqual(curr + inc, du.add_value(inc, None),
                         msg='Check add_value()')

if __name__ == '__main__':
    unittest.main()
