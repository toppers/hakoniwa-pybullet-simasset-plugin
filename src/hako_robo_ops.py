#!/usr/bin/python
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod

class HakoRoboOps(ABC):
    @abstractmethod
    def initialize():
        pass
    @abstractmethod
    def get_name():
        pass
    @abstractmethod
    def do_actuation():
        pass
    @abstractmethod
    def copy_sensing_data2pdu():
        pass