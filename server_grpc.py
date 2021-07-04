'''Server script to receive image bytes in stream.
'''

from concurrent import futures
import cv2
import grpc
import numpy as np
import stream_pb2, stream_pb2_grpc


class StreamImage(stream_pb2_grpc.StreamImageServicer):

    def imageStreaming(self, image_iterator, context):
        '''
        Receive image streams. Recall that image pixels are arranged by rows, columns, channels. Therefore,
        since the incoming stream is by rows, it would contain the column and channel information. 
        Args:
            image_iterator : iterator object containing a row of image data.
        '''
        rows = []
        for data in image_iterator:
            row = np.array(list(data.image), dtype=np.uint8) #convert the list of row stream to np array.
            index = int(row.shape[0]/3) #the incoming row data is flattened. In other words, the length of the data is columns (width) x channels (3 channels).
            row = np.reshape(row, (index,3)) #reshape the row back into columns x channels.
            rows.append(row)

        image = np.asarray(rows, dtype=np.uint8) #image reconstruction.
        cv2.imshow('img', image)
        cv2.waitKey(0)
        
        #dummy response
        return stream_pb2.imgResponse(response=2)


def serve():
    #server conf.
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    stream_pb2_grpc.add_StreamImageServicer_to_server(StreamImage(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__=="__main__":
    serve()


