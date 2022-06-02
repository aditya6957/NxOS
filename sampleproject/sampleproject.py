'''
sampleproject.py

'''
# see https://pubhub.devnetcloud.com/media/pyats/docs/aetest/index.html
# for documentation on pyATS test scripts

# optional author information
# (update below with your contact information if needed)
__author__ = 'Cisco Systems Inc.'
__copyright__ = 'Copyright (c) 2019, Cisco Systems Inc.'
__contact__ = ['pyats-support-ext@cisco.com']
__credits__ = ['list', 'of', 'credit']
__version__ = 1.0

import logging
import re

from pyats import aetest

# create a logger for this module
logger = logging.getLogger(__name__)

class CommonSetup(aetest.CommonSetup):

    @aetest.subsection
    def connect(self, testbed):
        '''
        establishes connection to all your testbed devices.
        '''
        # make sure testbed is provided
        assert testbed, 'Testbed is not provided!'

        # connect to all testbed devices
        testbed.connect()


class GetRunningConfig(aetest.Testcase):
    '''get_running_config

    < docstring description of this testcase >

    '''

    # testcase groups (uncomment to use)
    # groups = []

    @aetest.setup
    def prerequisite(self):
        pass

    # you may have N tests within each testcase
    # as long as each bears a unique method name
    # this is just an example
    @aetest.test
    def test(self, testbed, devices=["Whatever"]):
	final = {}
	for node in devices:
	    device = testbed.devices(node)
	    device.connect()
	    output = device.execute("show running-config")
	    final[node] = output
        print(final)

    @aetest.cleanup
    def cleanup(self):
        pass
    
class ShowVrf:
    """Parser for show vrf"""

    cli_command = ['show vrf', 'show vrf {vrf}']

    def test(self, testbed, vrf='', output=None):
	device = testbed.devices["Whatever"]
        if output is None:
            if vrf:
                out = device.execute(self.cli_command[1].format(vrf=vrf))
            else:
                out = device.execute(self.cli_command[0])
        else:
            out = output

        # Init vars
        vrf_dict = {}

        for line in out.splitlines():
            line = line.rstrip()

            # VRF2                                    4 Up      --
            # default                                 1 Up      --
            # VRF                                     5 Down    Admin Down
            p1 = re.compile(r'^\s*(?P<vrf_name>\S+)\s+(?P<vrf_id>[0-9]+)\s+'
                            r'(?P<vrf_state>(Up|Down))\s+(?P<reason>.*)$')
            m = p1.match(line)
            if m:
                if 'vrfs' not in vrf_dict:
                    vrf_dict['vrfs'] = {}
                vrf_name = str(m.groupdict()['vrf_name'])
                if vrf_name not in vrf_dict['vrfs']:
                    vrf_dict['vrfs'][vrf_name] = {}
                vrf_dict['vrfs'][vrf_name]['vrf_id'] = \
                    int(m.groupdict()['vrf_id'])
                vrf_dict['vrfs'][vrf_name]['vrf_state'] = \
                    str(m.groupdict()['vrf_state'])
                vrf_dict['vrfs'][vrf_name]['reason'] = \
                    str(m.groupdict()['reason'])
                continue

        return vrf_dict

class ShowVlan:
    """Parser for show vlan"""

    cli_command = ['show vlan', 'show vrf id {vlan}']

    def test(self, testbed, vlan='', output=None):
	device = testbed.devices["Whatever"]        
	if output is None:
            if vlan:
                out = device.execute(self.cli_command[1].format(vlan=vlan))
            else:
                out = device.execute(self.cli_command[0])
        else:
            out = output

        # Init vars
        vlan_dict = {}

        for line in out.splitlines():
            line = line.rstrip()

	    #1    default                          active    Po100, Po2223
	    #20   VLAN0020                         active    Po100
	    #30   VLAN0030                         active    Po100
	    #40   VLAN0040                         active    Po100
	    #50   VLAN0050                         active    Po100
	    #60   VLAN0060                         active    Po100
	    #70   VLAN0070                         active    Po100
	    #80   VLAN0080                         active    Po100
	    #90   VLAN0090                         active    Po100
	    #100  VLAN0100                         active    Po100


            p1 = re.compile(r'^\s*(?P<VLAN>\d+)\s+(?P<Name>\S+)\s+(?' 	                    r'P<Status>active|down|suspended)\s+(?P<Ports>.*)$') 	   
            m = p1.match(line)
            if m:
                if 'vlans' not in vlan_dict:
                    vlan_dict['vlan'] = {}
                vlan_name = str(m.groupdict()['vlan_name'])
                if vlan_name not in vlan_dict['vlans']:
                    vlan_dict['vlans'][vlan_name] = {}
                vlan_dict['vlans'][vlan_name]['vlan_id'] = \
                    int(m.groupdict()['vlan_id'])
                vlan_dict['vlans'][vlan_name]['vlan_state'] = \
                    str(m.groupdict()['vlan_state'])
                vlan_dict['vlans'][vlan_name]['reason'] = \
                    str(m.groupdict()['reason'])
                continue

        logger.info(vlan_dict)

class CommonCleanup(aetest.CommonCleanup):
    @aetest.subsection
    def disconnect(self, testbed):
        '''
        establishes connection to all your testbed devices.
        '''
        # make sure testbed is provided
        assert testbed, 'Testbed is not provided!'

        # connect to all testbed devices
        testbed.disconnect()



