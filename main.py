import grpc
import sqlite3
import json

from proto import MigrationService_pb2_grpc, MigrationService_pb2


def get_data():
    conn = sqlite3.connect('./biathlon-lite.db')
    conn.row_factory = sqlite3.Row
    db = conn.cursor()
    rows = db.execute('SELECT * from t_biathlon').fetchall()
    conn.commit()
    conn.close()
    return json.dumps([dict(ix) for ix in rows])


def run():
    with open('server.crt', 'rb') as f:
        creds = grpc.ssl_channel_credentials(root_certificates=f.read())
    channel = grpc.secure_channel('10.242.0.1:9092', credentials=creds)
    stub = MigrationService_pb2_grpc.MigrationGRPCServiceStub(channel)
    response = stub.migrateData(MigrationService_pb2.Request(message=get_data()))
    print("From Server: " + response.message)
    channel.close()


if __name__ == '__main__':
    run()
