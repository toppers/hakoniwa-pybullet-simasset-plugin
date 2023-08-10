#!/usr/bin/python
# -*- coding: utf-8 -*-

import pybullet as p
import pybullet_data

from hako_robo_ops import HakoRoboOps

class HakoRoboSample(HakoRoboOps):
    def __init__(self):
        pass

    def initialize(self):
        StartPos = [0,0,0]  
        StartOrient = p.getQuaternionFromEuler([0,0,3.14]) 
        self.carId = p.loadURDF("../bullet3/data/racecar/racecar.urdf", StartPos, StartOrient)

    def get_name(self):
        pass

    def do_actuation(self):
        p.setJointMotorControl2(self.carId, 2, p.VELOCITY_CONTROL, targetVelocity=10)
        p.setJointMotorControl2(self.carId, 3, p.VELOCITY_CONTROL, targetVelocity=40)
        p.setJointMotorControl2(self.carId, 5, p.VELOCITY_CONTROL, targetVelocity=10)
        p.setJointMotorControl2(self.carId, 7, p.VELOCITY_CONTROL, targetVelocity=40)

    def copy_sensing_data2pdu(self):
        pass