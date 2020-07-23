import unittest

from jina.main.parser import set_pea_parser, set_pod_parser, set_gateway_parser
from jina.peapods.gateway import GatewayPea
from jina.peapods.pea import BasePea
from jina.peapods.pod import BasePod
from tests import JinaTestCase


class PeaTestCase(JinaTestCase):

    def test_pea_context(self):
        def _test_pea_context(runtime):
            args = set_pea_parser().parse_args(['--runtime', runtime])
            with BasePea(args):
                pass

            BasePea(args).start().close()

        for j in ('process', 'thread'):
            with self.subTest(runtime=j):
                _test_pea_context(j)

    def test_address_in_use(self):
        args1 = set_pea_parser().parse_args(['--port-ctrl', '55555'])
        args2 = set_pea_parser().parse_args(['--port-ctrl', '55555'])
        with BasePea(args1), BasePea(args2):
            pass

        args1 = set_pea_parser().parse_args(['--port-ctrl', '55555', '--runtime', 'thread'])
        args2 = set_pea_parser().parse_args(['--port-ctrl', '55555', '--runtime', 'thread'])
        with BasePea(args1), BasePea(args2):
            pass

        print('everything should quit gracefully')

    def test_gateway_pea(self):
        def _test_gateway_pea(runtime):
            args = set_gateway_parser().parse_args(['--runtime', runtime])
            with GatewayPea(args):
                pass

            GatewayPea(args).start().close()

        for j in ('process', 'thread'):
            with self.subTest(runtime=j):
                _test_gateway_pea(j)

    def test_peas_naming_with_parallel(self):
        args = set_pod_parser().parse_args(['--name', 'pod',
                                            '--parallel', '2',
                                            '--max-idle-time', '5',
                                            '--shutdown-idle'])
        with BasePod(args) as bp:
            self.assertEqual(bp.peas[0].name, 'pod-head')
            self.assertEqual(bp.peas[1].name, 'pod-tail')
            self.assertEqual(bp.peas[2].name, 'pod-1')
            self.assertEqual(bp.peas[3].name, 'pod-2')

if __name__ == '__main__':
    unittest.main()
