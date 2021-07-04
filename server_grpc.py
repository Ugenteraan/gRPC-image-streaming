from concurrent import futures
import cv2
import grpc
import numpy as np
import stream_pb2, stream_pb2_grpc


class StreamImage(stream_pb2_grpc.StreamImageServicer):

    def imageStreaming(self, image_iterator, context):
        
        rows = []
        for data in image_iterator:
            row = np.array(list(data.image), dtype=np.uint8)
            print(row.shape)
            index = int(row.shape[0]/3)
            row = np.reshape(row, (index,3))
            rows.append(row)
        image = np.asarray(rows, dtype=np.uint8)
        cv2.imshow('img', image)
        cv2.waitKey(0)


        return stream_pb2.imgResponse(response=2)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    stream_pb2_grpc.add_StreamImageServicer_to_server(StreamImage(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__=="__main__":
    serve()


