# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 20:27:57 2019

@author: ryans
"""

from threading import Timer

class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer     = None
        self.function   = function
        self.interval   = interval
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)
    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True
    def stop(self):
        self.is_running = False
        self._timer.cancel()
