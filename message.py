#!/usr/bin/env python
import unittest
from datetime import datetime

class Message:
    text = ''
    date = None
    error_message = ''

    def __init__(self):
        self.text = ''
        self.date = None
        self.error_message = ''

    def init(self, text='', date=None):
        if not text:
            self.error_message = 'Text is not defined'
            return False

        if not date:
            self.error_message = 'Date is not defined'
            return False
        elif not isinstance(date, datetime):
            self.error_message = 'Date is not an instance of datetime'
            return False

        self.text = text
        self.date = date

        return True

    def get_text(self):
        return self.text

    def get_date(self):
        return self.date

    def get_error_message(self):
        return self.error_message


class t_Message(unittest.TestCase):
    """Tests for Message"""
    def test_init(self):
        m = Message()
        ret = m.init()
        self.assertEqual(False, ret, msg='Check object initialization')

    def test_init_text(self):
        m = Message()
        ret = m.init(date=datetime.now())
        self.assertEqual(False, ret, msg='Check text verification')
        self.assertEqual('Text is not defined', m.get_error_message(),
                         msg='Check text verification: error message')

    def test_init_date(self):
        m = Message()
        ret = m.init(text='fake message')
        self.assertEqual(False, ret, msg='Check date initialization')
        self.assertEqual('Date is not defined', m.get_error_message(),
                         msg='Check text verification: error message')

    def test_init_date2(self):
        m = Message()
        ret = m.init(text='fake message', date='invalid type of date')
        self.assertEqual(False, ret, msg='Check date initialization 2')
        self.assertEqual('Date is not an instance of datetime', m.get_error_message(),
                         msg='Check text verification: error message')

    def test_ok(self):
        m = Message()
        d = datetime.now()
        t = 'Test'
        ret = m.init(text=t, date=d)
        self.assertEqual(True, ret, msg='Init OK')
        self.assertEqual(t, m.get_text())
        self.assertEqual(d, m.get_date())

if __name__ == '__main__':
    unittest.main()
