#!/usr/bin/python
# -*- coding: utf-8 -*-

from hako_asset_pdu import HakoAssetPdu
from hako_apl_ops import HakoAplOps

class HakoAplSample(HakoAplOps):
    def __init__(self):
        pass

    def initialize(self, pdu: HakoAssetPdu):
        self.pdu = pdu
        self.read_channel = 1
        self.write_channel = 0

    def step(self):
        #GET PDU
        read_data = self.pdu.get_read_pdu_json(self.read_channel)
        write_data = self.pdu.get_write_pdu_json(self.write_channel)
        
        

        #WRITE PDU
        self.pdu.update_write_buffer(self.write_channel, write_data)

    def reset(self):
        #TODO
        pass

