import grpc
import cv2
import stream_pb2_grpc, stream_pb2


def client_req(filename='test.jpeg'):
    channel = grpc.insecure_channel('localhost:50051')
    stub = stream_pb2_grpc.StreamImageStub(channel)
    response = stub.imageStreaming(generateImageBytes(filename=filename))
    print(response)

def generateImageBytes(filename):
    '''Yields the images one row at a time for all channels (b,g,r).
    '''
    image = cv2.imread(filename)
    for f in img:
        data = bytes(f)
        yield stream_pb2.imgReq(image=data)

if __name__=="__main__":
    client_req()
