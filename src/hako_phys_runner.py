#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
from hako_asset_controller import HakoAssetController
from hako_asset_pdu import HakoAssetPdu
from phys_impl.hako_phys_pybullet import HakoPhysPybullet

class HakoRoboPhysRunner:
    def __init__(self, asset_name, robo_name, offset_path, readers, writers):
        self.pdu = HakoAssetPdu(asset_name, robo_name, offset_path)
        self.pdu.create_pdu_lchannel(writers)
        self.pdu.subscribe_pdu_lchannel(readers)

    def set_phys(self, phys):
        self.phys = phys

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

    def start(self):
        pass

    def _run(self):
        pass

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



