from __future__ import print_function

import grpc
import bidirectional_pb2_grpc as bidirectional_pb2_grpc
import bidirectional_pb2 as bidirectional_pb2
import time
import logging
import pandas as pd


def create_message():

    df = pd.read_csv("client/qs-world-university-rankings-2017-to-2022.csv")
    index = 0
    i = 0
    while index <= 1:
        # Get the first row in the dataframe
        line = [str(x) for x in df.iloc[i, :]]
        # Split the data and cast the first row as a string
        line_str = ", ".join(str(x) for x in line)
        msg = bidirectional_pb2.Message(message=line_str)
        yield msg
        i += 1

        if (index+1) % 2 == 0:
            time.sleep(1)
            index = 0

        index += 1


def run():
    with grpc.insecure_channel('grpc-server:50051') as channel:
        stub = bidirectional_pb2_grpc.BidirectionalStub(channel)
        response = stub.GetServerResponse(create_message())
        print("There server has completed =  %s" % response.response)


if __name__ == '__main__':
    logging.basicConfig()
    run()
