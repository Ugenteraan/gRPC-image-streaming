from concurrent import futures
import cv2
import grpc
import numpy as np
import stream_pb2, stream_pb2_grpc


class StreamImage(stream_pb2_grpc.StreamImageServicer):

    def imageStreaming(self, image_iterator, context):

        for data in image_iterator:
            print(image_iterator) 

        return 2


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    stream_pb2_grpc.add_StreamImageServicer_to_server(StreamImage(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__=="__main__":
    serve()


