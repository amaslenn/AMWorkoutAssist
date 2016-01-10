#!/usr/bin/env python
import unittest
import re


class MessageChecker:
    message = ''
    error_message = ''
    num_catch_ups = None

    def __init__(self, msg=''):
        self.message = ''
        self.error_message = ''
        self.num_catch_ups = None

        if msg:
            self.message = msg

    def set_message(self, msg):
        self.message = msg

    def check(self):
        if not self.message:
            self.error_message = 'Input message is empty'
            return False

        patterns = ['(\d+)\s+catch\s*ups', 'catch\s*ups\s+(\d+)',
                    '(\d+)\s+подтягиваний', 'подтягиваний\s+(\d+)']

        for p in patterns:
            res = re.match(p, self.message, re.IGNORECASE)
            if res:
                self.num_catch_ups = int(res.group(1))
                return True

        self.error_message = "Message '{}' is not supported".format(self.message)
        return False

    def get_num_catch_ups(self):
        return self.num_catch_ups

    def get_error_message(self):
        return self.error_message


class t_MessageChecker(unittest.TestCase):
    """Tests for MessageChecker"""
    def test_init(self):
        mc = MessageChecker('2 catch ups')
        self.assertEqual(True, mc.check(), msg='Check object initialization')
        self.assertEqual(2, mc.get_num_catch_ups(), msg='Check parsed number')

    def test_init2(self):
        mc = MessageChecker()
        mc.set_message('2 catchups')
        self.assertEqual(True, mc.check(), msg='Check object initialization 2')
        self.assertEqual(2, mc.get_num_catch_ups(), msg='Check parsed number')

    def test_init3(self):
        mc = MessageChecker('22 подтягиваний')
        self.assertEqual(True, mc.check(), msg='Check object initialization 3')
        self.assertEqual(22, mc.get_num_catch_ups(), msg='Check parsed number')

    def test_init4(self):
        mc = MessageChecker('подтягиваний 123')
        self.assertEqual(True, mc.check(), msg='Check object initialization 4')
        self.assertEqual(123, mc.get_num_catch_ups(), msg='Check parsed number')

    def test_init5(self):
        mc = MessageChecker('catchups 1')
        self.assertEqual(True, mc.check(), msg='Check object initialization 5')
        self.assertEqual(1, mc.get_num_catch_ups(), msg='Check parsed number')

    def test_negative(self):
        mc = MessageChecker('catchups')
        self.assertEqual(False, mc.check(), msg='Check object initialization (negative)')
        self.assertEqual(None, mc.get_num_catch_ups(), msg='Check parsed number')

if __name__ == '__main__':
    unittest.main()
