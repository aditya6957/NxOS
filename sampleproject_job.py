'''
sampleproject_job.py

'''
# see https://pubhub.devnetcloud.com/media/pyats/docs/easypy/jobfile.html
# for how job files work

# optional author information
# (update below with your contact information if needed)
__author__ = 'Cisco Systems Inc.'
__copyright__ = 'Copyright (c) 2019, Cisco Systems Inc.'
__contact__ = ['pyats-support-ext@cisco.com']
__credits__ = ['list', 'of', 'credit']
__version__ = 1.0

import os
from pyats.easypy import run
from genie.harness.main import gRun

def main():
    gRun(
	pdb=False,
	TriggerGetRunningConfig="sampleproject_data.yaml",
	trigger_uids=[
	    "TriggerGetRunningConfig"
	]
	)
