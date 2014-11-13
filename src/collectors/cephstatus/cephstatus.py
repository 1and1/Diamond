try:
    import json
except ImportError:
    import simplejson as json

import subprocess
import re
import os
import sys
import diamond.collector

"""
Get status info from the ceph cluster.
Collect epochs, pg version, pg and osd state summaries
vvoigt 20141112
"""

class CephStatusCollector(diamond.collector.Collector):

    def collect(self):

        try:
            """
            Unfortunately the dumpling "ceph" cli tool does not (yet) support a timeout feature. Starting with Emporer it is possible...
            """
            params = ['ceph', '-s', '--format=json']

            if self.config['ceph_user'] != '':
                params.append( '--name=' + self.config['ceph_user'] )

            if self.config['ceph_keyring'] != '':
                params.append( '--keyring=' + self.config['ceph_keyring'] )

            output = subprocess.check_output(params)

        except subprocess.CalledProcessError, err:
            self.log.info( 'Could not get stats: %s' % err)
            self.log.exception('Could not get stats')
            return False

        try:
            jsonData = json.loads(output)
        except Exception, err:
            self.log.info('Could not parse stats from ceph df: %s', err)
            self.log.exception('Could not parse stats from ceph df')
            return False

        status = jsonData["health"]

        self.publish('mon.election_epoch', jsonData["health"]["timechecks"]["epoch"], metric_type='COUNTER')
        self.publish('mon.map_epoch', jsonData["monmap"]["epoch"], metric_type='COUNTER')
        self.publish('osd.map_epoch', jsonData["osdmap"]["osdmap"]["epoch"], metric_type='COUNTER')

        self.publish('osd.total', jsonData["osdmap"]["osdmap"]["num_osds"], metric_type='GAUGE')
        self.publish('osd.up', jsonData["osdmap"]["osdmap"]["num_up_osds"], metric_type='GAUGE')
        self.publish('osd.in', jsonData["osdmap"]["osdmap"]["num_in_osds"], metric_type='GAUGE')

        self.publish('pg.version', jsonData["pgmap"]["version"], metric_type='COUNTER')

	if "degrated_ratio" in jsonData["pgmap"]:
        	self.publish('pg.degraded_ratio', float(jsonData["pgmap"]["degrated_ratio"]), precision=3, metric_type='GAUGE') # The typo in "degratet" is present in dumpling's ceph -s json output...
	else:
		self.publish('pg.degraded_ratio', 0.000, precision=3, metric_type='GAUGE')

        self.publish('pg.total', jsonData["pgmap"]["num_pgs"], metric_type='GAUGE')

        for pgstate in jsonData["pgmap"]["pgs_by_state"]:
            self.publish('pg.states.' + pgstate["state_name"].replace('+',':'), pgstate["count"], metric_type='GAUGE')

        return True

