"""

1. TOTAL NUMBER OF FACULTIES 
2. AVAERGAE NUMBER OF FACULTIES IN COLLEGE 
3. MOST NUMBER OF INTERNATIONAL STUDENTS. 
4. TOTAL NUMBER OF COLLEGES IN UNITED STATES

Columns needed - faculties, international students, countires, colleges

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

        international_students = 0
        max_international_students = 0
        max_intstud_uni_name = ''
        arr_international_students = []
        average_international_students = 0
        university_faculties = []
        avg_university_faculties = 0
        universities_usa = 0
        start_time = time.time()
        lines = 0

        for message in request:

            current_time = time.time()
            line = message.message
            print(line)

            lines += 1

            list_data = line.split(', ')
            if(list_data[5] == "United States"):
                universities_usa += 1

            list_len = len(list_data)

            if(list_data[list_len - 3] == 'nan'):
                data1_str = '0'
            else:
                data1_str = re.sub('[^A-Za-z0-9]+', '',
                                   list_data[list_len - 3])
                international_students = int(data1_str)

            if(list_data[list_len - 1] == 'nan'):
                data2_str = '0'
            else:
                data2_str = re.sub('[^A-Za-z0-9]+', '',
                                   list_data[list_len - 1])
                university_faculties.append(int(data2_str))

            arr_international_students.append(international_students)

            if(international_students > max_international_students):
                max_international_students = international_students
                max_intstud_uni_name = list_data[0]

            try:
                conn = redis.StrictRedis(host='redis', port=6379)
                conn.set("qs.log.average_international_students",
                         str(average_international_students))
                if(current_time - start_time >= 180):
                    average_international_students = np.mean(
                        arr_international_students)
                    arr_international_students.clear()
                elif(lines % 10 == 0):
                    avg_university_faculties = np.mean(university_faculties)
                    conn.set("qs.log.universities_usa", str(universities_usa))
                    conn.set("qs.log.avg_university_faculties",
                             str(avg_university_faculties))
                    conn.set("qs.log.max_international_students",
                             str(max_intstud_uni_name))
                    max_international_students = 0
                    universities_usa = 0
                    university_faculties.clear()

            except Exception as ex:
                print('Redis Error: ', ex)

        return bidirectional_pb2.Response(response=True)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    bidirectional_pb2_grpc.add_BidirectionalServicer_to_server(
        BidirectionalService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
