import sqlite3

import grpc

from proto import MigrationService_pb2_grpc, MigrationService_pb2


def run():
    with open('server.crt', 'rb') as f:
        creds = grpc.ssl_channel_credentials(root_certificates=f.read())
    channel = grpc.secure_channel('localhost:8443', creds)

    conn = sqlite3.connect('./biathlon-lite.db')
    conn.row_factory = sqlite3.Row
    db = conn.cursor()
    rows = db.execute('SELECT * from t_biathlon').fetchall()
    conn.commit()
    conn.close()

    #channel = grpc.insecure_channel('localhost:8443')
    stub = MigrationService_pb2_grpc.MigrationGRPCServiceStub(channel)
    for row in rows:
        response = stub.MigrateData(MigrationService_pb2.Request(
            sex=row[0],
            raceDate=row[1],
            startTime=row[2],
            stageName=row[3],
            trackLocation=row[4],
            trackLength=row[5],
            discName=row[6],
            discLines=row[7],
            discFines=row[8],
            stageStart=row[9],
            stageEnd=row[10],
            champName=row[11],
            champStart=row[12],
            champEnd=row[13],
            cityName=row[14],
            countryName=row[15]
        ))
        print("From Server: " + response.message)
    channel.close()


if __name__ == '__main__':
    run()
