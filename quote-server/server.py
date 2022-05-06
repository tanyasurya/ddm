"""

1. QUOTE 
2. AUTHOR 

Columns needed - Quote, Author

"""

from concurrent import futures
import time
import logging

import grpc
import bidirectional_pb2_grpc as bidirectional_pb2_grpc
import bidirectional_pb2 as bidirectional_pb2

import redis
import numpy as np
import re
import pandas as pd


class BidirectionalService(bidirectional_pb2_grpc.BidirectionalServicer):

    def GetServerResponse(self, request, context):

        start_time = time.time()
        lines = 0

        for message in request:

            current_time = time.time()
            quote_line = message.message
            print('Quote Line', quote_line)

            lines += 1

            list_data = quote_line.split(', ')
        
            list_len = len(list_data)
            print("Quote Lines: ", list_len)

            try:
                conn = redis.StrictRedis(host='redis', port=6379)
                conn.set("qs.log.quote_text", str(list_data[0]))
                conn.set("qs.log.quote_author", str(list_data[1]))
                
            except Exception as ex:
                print('Redis Error: ', ex)

        return bidirectional_pb2.Response(response=True)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    bidirectional_pb2_grpc.add_BidirectionalServicer_to_server(
        BidirectionalService(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
