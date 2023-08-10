#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import time
from hako_asset_controller import HakoAssetController
from hako_asset_pdu import HakoAssetPdu
from phys_impl.hako_phys_pybullet import HakoPhysPybullet
from apl_impl.hako_apl_sample import HakoAplSample
from phys_robo_impl.hako_phys_robo_sample import HakoPhysRoboSample

class HakoRoboPhysRunner:
    def __init__(self, asset_name, robo_name, offset_path, readers, writers):
        self.pdu = HakoAssetPdu(asset_name, robo_name, offset_path)
        self.pdu.create_pdu_lchannel(writers)
        self.pdu.subscribe_pdu_lchannel(readers)
        self.robo_phys = HakoPhysRoboSample()
        self.robo_phys.initialize()
    
    def sync_read_pdus(self):
        self.pdu.sync_read_buffers()
    
    def sync_write_pdus(self):
        self.pdu.sync_write_buffers()

    def do_actuation(self):
        self.robo_phys.do_actuation()

    def copy_sensing_data2pdu(self):
        self.robo_phys.copy_sensing_data2pdu()

class HakoAplRunner:
    def __init__(self, asset_name, robo_name, offset_path, readers, writers):
        self.pdu = HakoAssetPdu(asset_name, robo_name, offset_path)
        self.pdu.create_pdu_lchannel(writers)
        self.pdu.subscribe_pdu_lchannel(readers)
        self.apl = HakoAplSample()
        self.apl.initialize(self.pdu)
    
    def sync_read_pdus(self):
        self.pdu.sync_read_buffers()
    
    def sync_write_pdus(self):
        self.pdu.sync_write_buffers()

    def step(self):
        self.apl.step()

    def reset(self):
        #TODO
        pass


class HakoRunner:
    def __init__(self, filepath):
        with open(filepath, 'r') as file:
            self.config = json.load(file)

        with open(self.config['robot_config_path'], 'r') as file:
            self.robo_config = json.load(file)

        with open(self.config['apl_config_path'], 'r') as file:
            self.apl_config = json.load(file)

        self.phys = HakoPhysPybullet()
        self.controller = HakoAssetController(self.config['delta_msec'] * 1000)

    def initialize(self):
        self.phys.initialize()
        self.controller.initialize()

        # ROBOTS FOR PHYS
        self.robots = []
        for entry in self.robo_config['robots']:
            print("robo:", entry['name'])
            readers = entry['shm_pdu_readers']
            writers = entry['shm_pdu_writers']
            robo = HakoRoboPhysRunner(self.controller.asset_name, entry['name'], self.config['offset_path'],readers, writers)
            self.robots.append(robo)

        # ROBOTS FOR APPLICATIONS
        self.apls = []
        for entry in self.apl_config['robots']:
            print("apl:", entry['name'])
            readers = entry['shm_pdu_readers']
            writers = entry['shm_pdu_writers']
            robo = HakoAplRunner(self.controller.asset_name, entry['name'], self.config['offset_path'],readers, writers)
            self.apls.append(robo)

    def do_actuation(self):
        for entry in self.robots:
            entry.do_actuation()

    def copy_sensing_data2pdu(self):
        for entry in self.robots:
            entry.copy_sensing_data2pdu()

    def sync_read_pdus(self):
        for entry in self.robots:
            entry.sync_read_pdus()

    def sync_write_pdus(self):
        for entry in self.robots:
            entry.sync_write_pdus()

    def apl_sync_write_pdus(self):
        for entry in self.apls:
            entry.sync_write_pdus()

    def apl_sync_read_pdus(self):
        for entry in self.apls:
            entry.sync_read_pdus()

    def apl_step(self):
        for entry in self.apls:
            entry.step()

    def run(self):
        while True:
            print("WAIT START:")
            self.controller.wait_event(HakoAssetController.HakoEvent.START)
            print("WAIT RUNNING:")
            self.controller.wait_state(HakoAssetController.HakoState.RUNNING)
            print("WAIT PDU CREATED:")
            self.controller.wait_pdu_created()

            print("GO:")
            while True:
                if self.controller.execute() == False:
                    if self.controller.state() != HakoAssetController.HakoState.RUNNING:
                        print("WAIT_STOP")
                        self.controller.wait_event(HakoAssetController.HakoEvent.STOP)
                        print("WAIT_RESET")
                        self.controller.wait_event(HakoAssetController.HakoEvent.RESET)
                        print("DONE")
                        #TODO simulation phys reset
                        break
                    else:
                        if self.controller.is_pdy_sync_mode():
                            #FOR PHYS
                            self.copy_sensing_data2pdu()
                            self.sync_write_pdus()
                            #FOR APPLS
                            self.apl_sync_write_pdus()
                        time.sleep(0.01)
                        continue

                #FOR PHYS
                self.sync_read_pdus()
                self.do_actuation()
                self.phys.step()
                self.copy_sensing_data2pdu()
                self.sync_write_pdus()

                #FOR APLS
                self.apl_sync_read_pdus()
                self.apl_step()
                self.apl_sync_write_pdus()
                time.sleep(0.01)
 
    def _reset(self):
        pass


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: <config.json>")
        sys.exit(1)
    
    filepath = sys.argv[1]
    print("filepath=", filepath)

    runner = HakoRunner(filepath)
    runner.initialize()

    runner.run()





