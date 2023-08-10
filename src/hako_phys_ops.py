#!/usr/bin/python
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod

class HakoPhysOps(ABC):
    @abstractmethod
    def initialize():
        pass
    @abstractmethod
    def get_phys():
        pass
    @abstractmethod
    def step():
        pass
    @abstractmethod
    def reset():
        pass
