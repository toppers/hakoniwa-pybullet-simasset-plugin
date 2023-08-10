#!/usr/bin/python
# -*- coding: utf-8 -*-

import pybullet as p
import pybullet_data

from hako_asset_pdu import HakoAssetPdu
from hako_phys_robo_ops import HakoPhysRoboOps

class HakoPhysRoboSample(HakoPhysRoboOps):
    def __init__(self):
        pass

    def initialize(self, pdu):
        self.pdu = pdu
        self.read_channel = 0
        self.write_channel = 1

        StartPos = [0,0,0]  
        StartOrient = p.getQuaternionFromEuler([0,0,3.14]) 
        self.carId = p.loadURDF("../bullet3/data/racecar/racecar.urdf", StartPos, StartOrient)

    def get_name(self):
        return str("Robo-" + str(self.carId))

    def do_actuation(self):
        #GET PDU
        cmd_vel = self.pdu.get_read_pdu_json(self.read_channel)
        #print(str(cmd_vel))

        vel1 = 10 * (int)(cmd_vel['linear']['x'])
        vel2 = 10 * (int)(cmd_vel['linear']['y'])
        #print("vel1=", vel1)
        #print("vel2=", vel2)

        p.setJointMotorControl2(self.carId, 2, p.VELOCITY_CONTROL, targetVelocity=vel1)
        p.setJointMotorControl2(self.carId, 5, p.VELOCITY_CONTROL, targetVelocity=vel1)
        p.setJointMotorControl2(self.carId, 3, p.VELOCITY_CONTROL, targetVelocity=vel2)
        p.setJointMotorControl2(self.carId, 7, p.VELOCITY_CONTROL, targetVelocity=vel2)


    def copy_sensing_data2pdu(self):
        #WRITE PDU
        write_data = self.pdu.get_write_pdu_json(self.write_channel)
        write_data['data'] = "HELLO WORLD!!"
        self.pdu.update_write_buffer(self.write_channel, write_data)
