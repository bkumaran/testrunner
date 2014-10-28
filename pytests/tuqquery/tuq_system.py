from tuqquery.tuq import QueryTests
from remote.remote_util import RemoteMachineShellConnection
from membase.api.rest_client import RestConnection
from membase.api.exception import CBQError

class SysCatalogTests(QueryTests):

    def setUp(self):
        super(SysCatalogTests, self).setUp()

    def suite_setUp(self):
        super(SysCatalogTests, self).suite_setUp()

    def tearDown(self):
        super(SysCatalogTests, self).tearDown()

    def suite_tearDown(self):
        super(SysCatalogTests, self).suite_tearDown()

    def test_sites(self):
        self.query = "SELECT * FROM :system.stores"
        result = self.run_cbq_query()
        host = ('localhost', self.input.tuq_client)[self.input.tuq_client and "client" in self.input.tuq_client]
        for res in result['resultset']:
            self.assertEqual(res['stores']['id'], res['stores']['url'],
                             "Id and url don't match")
            self.assertTrue(res['stores']['url'].find(host) != -1,
                            "Expected: %s, actual: %s" % (host, result))

    def test_pools(self):
        self.query = "SELECT * FROM system:namespaces"
        result = self.run_cbq_query()

        host = ('localhost', self.input.tuq_client)[self.input.tuq_client and "client" in self.input.tuq_client]
        for res in result['resultset']:
            self.assertEqual(res['namespaces']['id'], res['namespaces']['name'],
                        "Id and url don't match")
            self.assertTrue(res['namespaces']['store_id'].find(host) != -1,
                            "Expected: %s, actual: %s" % (host, result))

    def test_buckets(self):
        self.query = "SELECT * FROM system:keyspaces"
        result = self.run_cbq_query()
        buckets = [bucket.name for bucket in self.buckets]
        self.assertFalse(set(buckets) - set([b['keyspaces']['id'] for b in result['resultset']]),
                        "Expected ids: %s. Actual result: %s" % (buckets, result))
        self.assertFalse(set(buckets) - set([b['name'] for b in result['results']]),
                        "Expected names: %s. Actual result: %s" % (buckets, result))
        pools = self.run_cbq_query(query='SELECT * FROM system:namespaces')
        self.assertFalse(set([b['keyspaces']['namespace_id'] for b in result['resultset']]) -\
                        set([p['namespaces']['id'] for p in pools['resultset']]),
                        "Expected pools: %s, actual: %s" % (pools, result))
        self.assertFalse(set([b['keyspaces']['store_id'] for b in result['resultset']]) -\
                        set([p['keyspaces']['store_id'] for p in pools['resultset']]),
                        "Expected site_ids: %s, actual: %s" % (pools, result))
