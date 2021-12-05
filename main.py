import grpc

import MigrationService_pb2
import MigrationService_pb2_grpc


def run():
    channel = grpc.insecure_channel('10.242.0.2:9092')
    stub = MigrationService_pb2_grpc.MigrationGRPCServiceStub(channel)
    response = stub.migrateData(MigrationService_pb2.Request(message='12'))
    print("From Server: " + response.message)
    channel.close()


if __name__ == '__main__':
    run()
