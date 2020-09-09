import dotenv
import grpc
import logging
from api.mgmt import MgmtServicer
from concurrent import futures
from os import getenv

dotenv.load_dotenv(dotenv_path = '../.env')
logging.basicConfig(level = logging.DEBUG)

server = grpc.server(futures.ThreadPoolExecutor(max_workers = int(getenv('GRPC_MAX_WORKERS'))))

MgmtServicer(server)

server.add_insecure_port('[::]:50051')
server.start()
server.wait_for_termination()
