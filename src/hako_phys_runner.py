#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import time
from hako_asset_controller import HakoAssetController
from hako_asset_pdu import HakoAssetPdu
from phys_impl.hako_phys_pybullet import HakoPhysPybullet
from robo_impl.hako_robo_sample import HakoRoboSample

class HakoRoboPhysRunner:
    def __init__(self, asset_name, robo_name, offset_path, readers, writers):
        self.pdu = HakoAssetPdu(asset_name, robo_name, offset_path)
        self.pdu.create_pdu_lchannel(writers)
        self.pdu.subscribe_pdu_lchannel(readers)
        self.robo_phys = HakoRoboSample()
        self.robo_phys.initialize()

    def do_actuation(self):
        self.robo_phys.do_actuation()

    def copy_sensing_data2pdu(self):
        self.robo_phys.copy_sensing_data2pdu()

class HakoPhysRunner:
    def __init__(self, filepath):
        with open(filepath, 'r') as file:
            self.config = json.load(file)

        with open(self.config['robot_config_path'], 'r') as file:
            self.robo_config = json.load(file)
        
        self.phys = HakoPhysPybullet()
        self.controller = HakoAssetController(self.config['delta_msec'] * 1000)

    def initialize(self):
        self.phys.initialize()
        self.controller.initialize()
        self.robots = []
        for entry in self.robo_config['robots']:
            print("robo:", entry['name'])
            readers = entry['shm_pdu_readers']
            writers = entry['shm_pdu_writers']
            robo = HakoRoboPhysRunner(self.controller.asset_name, entry['name'], self.config['offset_path'],readers, writers)
            self.robots.append(robo)

    def do_actuation(self):
        for entry in self.robots:
            entry.do_actuation()

    def copy_sensing_data2pdu(self):
        for entry in self.robots:
            entry.copy_sensing_data2pdu()

    def run(self):
        print("WAIT START:")
        self.controller.wait_event(HakoAssetController.HakoEvent.START)
        print("WAIT RUNNING:")
        self.controller.wait_state(HakoAssetController.HakoState.RUNNING)
        print("WAIT PDU CREATED:")
        self.controller.wait_pdu_created()

        print("GO:")
        while True:
            self.copy_sensing_data2pdu()
            self.phys.step()
            self.do_actuation()
            time.sleep(1. / 60.)

    def _reset(self):
        pass


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: <config.json>")
        sys.exit(1)
    
    filepath = sys.argv[1]
    print("filepath=", filepath)

    runner = HakoPhysRunner(filepath)
    runner.initialize()

    runner.run()





