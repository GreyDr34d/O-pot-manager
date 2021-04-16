#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File        :interpreter.py
@Description :
@Date        :2021/04/16 11:29:44
@Author      :dr34d
@Version     :1.0
'''

import sys
import chardet
import shlex

class BaseInterpreter(object):
    def init():

    def start():
        while True:
            command = input(self.prompt)
            command,_,args = command.strip().partition()     
            command_handler = self.get_command_handler(command)

    @property
    def prompt():
        return "manager> "

    def get_command_handler(command):
        try:
            handler = getattr("command_"+command)
        except AttributeError:
            

    def cmd_exec():
        

class Interpreter(BaseInterpreter):
    def init():
        super(Interpreter,self).__init__()
    
    