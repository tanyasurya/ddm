from __future__ import print_function
from email import message

import grpc
import bidirectional_pb2_grpc as bidirectional_pb2_grpc
import bidirectional_pb2 as bidirectional_pb2
import time
import logging
import csv
import json


def create_message():

    quote = ''
    author = ''
    message = ''

    with open('quote-client/inspiration_quotes.csv') as csvFileObj:
        reader = csv.DictReader(csvFileObj, delimiter=',', quotechar='"')
        # csv.reader requires bytestring input in python2, unicode input in python3
        quote_text = ''
        quote_author = ''
        for record in reader:
            # record is a dictionary of the csv record
            quote_text = str({record["Quote"]})
            quote_author =  str({record["Author"]})
            quote = processString(quote_text)
            author = processString(quote_author)
            time.sleep(10)
            message = bidirectional_pb2.Message(message=quote+','+author)
            yield message

def processString(txt):
    specialChars = "{'“”'}" 
    for specialChar in specialChars:
        txt = txt.replace(specialChar, '')
    txt = txt.replace(',', '$')
    return txt 


def run():
    with grpc.insecure_channel('grpc-quote-server:50052') as channel:
        stub = bidirectional_pb2_grpc.BidirectionalStub(channel)
        response = stub.GetServerResponse(create_message())
        print("The quote server message has completed =  %s" % response.response)


if __name__ == '__main__':
    logging.basicConfig()
    run()
