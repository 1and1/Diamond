#!/usr/bin/python
# coding=utf-8
################################################################################

from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from mock import Mock
from mock import patch

from diamond.collector import Collector
from memcached import MemcachedCollector

################################################################################


class TestMemcachedCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('MemcachedCollector', {
            'interval': 10,
            'hosts': ['localhost:11211'],
        })

        self.collector = MemcachedCollector(config, None)

    def test_import(self):
        self.assertTrue(MemcachedCollector)

    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data(self, publish_mock):
        patch_raw_stats = patch.object(
            MemcachedCollector,
            'get_raw_stats',
            Mock(return_value=self.getFixture(
                'stats').getvalue()))

        patch_raw_stats.start()
        self.collector.collect()
        patch_raw_stats.stop()

        metrics = {
            '11211.reclaimed': 0.000000,
            '11211.expired_unfetched': 0.000000,
            '11211.hash_is_expanding': 0.000000,
            '11211.cas_hits': 0.000000,
            '11211.uptime': 0,
            '11211.touch_hits': 0.000000,
            '11211.delete_misses': 0.000000,
            '11211.listen_disabled_num': 0.000000,
            '11211.cas_misses': 0.000000,
            '11211.decr_hits': 0.000000,
            '11211.cmd_touch': 0.000000,
            '11211.incr_hits': 0.000000,
            '11211.auth_cmds': 0.000000,
            '11211.limit_maxbytes': 67108864.000000,
            '11211.bytes_written': 0.000000,
            '11211.incr_misses': 0.000000,
            '11211.rusage_system': 0.195071,
            '11211.total_items': 0.000000,
            '11211.cmd_get': 0.000000,
            '11211.curr_connections': 10.000000,
            '11211.touch_misses': 0.000000,
            '11211.threads': 4.000000,
            '11211.total_connections': 0,
            '11211.cmd_set': 0.000000,
            '11211.curr_items': 0.000000,
            '11211.conn_yields': 0.000000,
            '11211.get_misses': 0.000000,
            '11211.reserved_fds': 20.000000,
            '11211.bytes_read': 0,
            '11211.hash_bytes': 524288.000000,
            '11211.evicted_unfetched': 0.000000,
            '11211.cas_badval': 0.000000,
            '11211.cmd_flush': 0.000000,
            '11211.evictions': 0.000000,
            '11211.bytes': 0.000000,
            '11211.connection_structures': 11.000000,
            '11211.hash_power_level': 16.000000,
            '11211.auth_errors': 0.000000,
            '11211.rusage_user': 0.231516,
            '11211.delete_hits': 0.000000,
            '11211.decr_misses': 0.000000,
            '11211.get_hits': 0.000000,
            '11211.repcached_qi_free': 0.000000,
        }

        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=metrics,
                           defaultpath=self.collector.config['path'])
        self.assertPublishedMany(publish_mock, metrics)

################################################################################
if __name__ == "__main__":
    unittest.main()
