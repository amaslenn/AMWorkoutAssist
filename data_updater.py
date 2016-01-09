#!/usr/bin/env python
from datetime import datetime
import unittest
import json
import gspread
from oauth2client.client import SignedJwtAssertionCredentials


OAUTH2TOKEN_FILE = 'oauth2token.json'
START_CELL = 'B3'


class DataUpdater:
    """Updater for Google spreadsheet"""
    gc = None
    book = None
    work_sheet = None
    error_message = ''
    initialized = False
    current_cell = ''

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

    def _get_current_cell(self):
        if self.current_cell:
            return self.current_cell

        ww = self.get_cell_value(START_CELL)
        now = datetime.now()
        curr_ww = now.isocalendar()[1]
        if ww != "ww{}".format(curr_ww):
            self.error_message = "Invalid week: {}, expected ww{}".format(ww, curr_ww)
            return None

        col, row = self.work_sheet.get_int_addr(START_CELL)
        col += 1    # data starts next to ww name

        col += now.weekday() + 1
        cell = self.work_sheet.get_addr_int(col, row)
        return cell

    def init(self):
        f = open(OAUTH2TOKEN_FILE)
        json_key = json.load(f)
        f.close()
        scope = ['https://spreadsheets.google.com/feeds']
        credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'].encode(), scope)

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

    def get_cell_value(self, cell):
        if not self.initialized:
            self.error_message = "DataUpdater is not initialized"
            return ''

        return self.work_sheet.acell(cell).value

    def add_value(self, value):
        if not self.initialized:
            self.error_message = "DataUpdater is not initialized"
            return False

        cell = self._get_current_cell()
        if not cell:
            return 0

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
        du._set_current_cell('N3')
        curr = int(du.get_cell_value('N3'))
        self.assertEqual(curr + inc, du.add_value(inc),
                         msg='Check add_value()')

if __name__ == '__main__':
    unittest.main()