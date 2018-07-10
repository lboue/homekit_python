#!/usr/bin/env python3

#
# Copyright 2018 Joachim Lusiardi
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os.path
import logging

from homekit import AccessoryServer
from homekit.model import Accessory
from homekit.model.services import LightBulbService, ThermostatService, OutletService, FanService
from homekit.model.characteristics import TargetTemperatureCharacteristic, TargetHeatingCoolingStateCharacteristic

def light_switched(new_value):
    print('=======>  light switched: {x}'.format(x=new_value))

def outlet_switched(new_value):
    print('=======>  outlet switched: {x}'.format(x=new_value))  
    
def fan_switched(new_value):
    print('=======>  fan switched: {x}'.format(x=new_value))  
    
def th_target_temperature(new_value):
    print('=======>  th target temperature: {x}'.format(x=new_value)) 

def th_target_state(new_value):
    print('=======>  th target state: {x}'.format(x=new_value))    
    
if __name__ == '__main__':
    # setup logger
    logger = logging.getLogger('accessory')
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(ch)
    logger.info('starting')

    config_file = os.path.expanduser('~/.homekit/demoserver.json')

    # create a server and an accessory an run it unless ctrl+c was hit
    try:
        httpd = AccessoryServer(config_file, logger)

        accessory = Accessory('lightBulb', 'lusiardi.de', 'Demoserver', '0001', '0.1')
        lightBulbService = LightBulbService()
        lightBulbService.set_on_set_callback(light_switched)
        accessory.services.append(lightBulbService)
        httpd.add_accessory(accessory)

        accessory2 = Accessory('thermostat', 'lusiardi.de', 'Demoserver', '0002', '0.1')
        thermostatService = ThermostatService()
        # Set callbacks
        thermostatService.set_target_temperature_set_callback(th_target_temperature)
        thermostatService.set_target_heating_cooling_state_set_callback(th_target_state)
        accessory2.services.append(thermostatService)
        httpd.add_accessory(accessory2)
        
        accessory3 = Accessory('outlet', 'lusiardi.de', 'Demoserver', '0003', '0.1')
        outletService = OutletService()
        outletService.set_on_set_callback(outlet_switched)
        accessory3.services.append(outletService)
        #  OutletInUseCharacteristic(AbstractCharacteristic):
        httpd.add_accessory(accessory3)
        
        accessory4 = Accessory('fan', 'lusiardi.de', 'Demoserver', '0003', '0.1')
        fanService = FanService()
        fanService.set_on_set_callback(outlet_switched)
        accessory4.services.append(fanService)
        #  OutletInUseCharacteristic(AbstractCharacteristic):
        httpd.add_accessory(accessory4)
        
        httpd.publish_device()
        
        logger.info('published lightBulb device and start serving')
        logger.info('published thermostat device and start serving')
        logger.info('published outlet device and start serving')
        logger.info('published fan device and start serving')
        
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass

    # unpublish the device and shut down
    logger.info('unpublish devices')
    httpd.unpublish_device()
    httpd.shutdown()

