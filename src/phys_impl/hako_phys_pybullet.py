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
        p.setGravity(0,0,-9.81)
        timestep = 0.01
        p.setTimeStep(timestep)
        self.planeId = p.loadURDF("../bullet3/data/plane.urdf")

    def initialize(self):
        pass

    def get_phys(self):
        return p

    def step(self):
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
        time.sleep(0.01)
    
    print("END")
