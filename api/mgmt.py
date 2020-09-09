import logging
import api.stubs.mgmt_pb2 as pb2
import api.stubs.mgmt_pb2_grpc as pb2_grpc

class MgmtServicer(pb2_grpc.MgmtServicer):
    """
    NS Management service implementation
    """

    def __init__(self, grpc_server):
        logging.debug('Mgmt Services started')
        pb2_grpc.add_MgmtServicer_to_server(self, grpc_server)

    def SetPrefix(self, request, context):
        logging.debug('MGMT SETPREFIX!')
        return pb2.Empty()
