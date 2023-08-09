#!/usr/bin/python
# -*- coding: utf-8 -*-
import pybullet as p
import pybullet_data
import numpy as np
import time

from hako_phys_ops import HakoPhysOps

class HakoPhysPybullet(HakoPhysOps):
    def __init__(self):
        self.physicsClient = p.connect(p.GUI)
        p.resetSimulation()
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0,0,-10)
        timestep = 1. / 60.
        p.setTimeStep(timestep)
        self.planeId = p.loadURDF("../bullet3/data/plane.urdf")
        StartPos = [0,0,0]  
        StartOrient = p.getQuaternionFromEuler([0,0,3.14]) 
        self.carId = p.loadURDF("../bullet3/data/racecar/racecar.urdf",StartPos, StartOrient)

    def initialize(self):
        pass

    def get_name(self):
        pass

    def step(self):
        p.setJointMotorControl2(self.carId, 2, p.VELOCITY_CONTROL, targetVelocity=10)
        p.setJointMotorControl2(self.carId, 3, p.VELOCITY_CONTROL, targetVelocity=40)
        p.setJointMotorControl2(self.carId, 5, p.VELOCITY_CONTROL, targetVelocity=10)
        p.setJointMotorControl2(self.carId, 7, p.VELOCITY_CONTROL, targetVelocity=40)
        p.stepSimulation()

    def reset(self):
        pass


if __name__ == "__main__":
    print("INITIALIZING")

    phys = HakoPhysPybullet()

    input("ENTER")
    print("START")

    while True:
        phys.step()
        time.sleep(1. / 60.)
    
    print("END")
