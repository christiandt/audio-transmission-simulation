__author__ = 'christue'

import random
import copy


class Server():
    global header
    header = []
    packetSize = 30

    def readHeader(self):
        global header
        with open('poe.au', 'rb') as musicFile:
            for i in range(24):
                byte = musicFile.read(1).encode('hex')
                header.append(int(byte, 16))
        musicFile.close()

    def streamFile(self):
        network = Network()
        self.readHeader()
        with open('poe.au', 'rb') as musicFile:
            eof = False
            while not eof:
                bytes = []
                for i in range(self.packetSize):
                    byte = musicFile.read(1).encode('hex')
                    if not byte:
                        eof = True
                        break
                    bytes.append(int(byte, 16))
                packet = Packet(bytes)
                network.send(packet)
        musicFile.close()


class Packet():
    global counter
    counter = 0

    def __init__(self, bytes):
        global counter
        self.bytes = bytes
        self.number = counter
        counter += 1


class Network():
    threshold = 80
    clients = []

    def connect(self, client):
        self.clients.append(client)

    def send(self, packet):
        loss = random.randint(1, 100)
        if loss <= self.threshold:
            for client in self.clients:
                client.receiveStream(packet)


class Client():
    silence = False
    packets = []

    def connect(self):
        self.network = Network()
        self.network.connect(self)

    def receiveStream(self, packet):
        if len(self.packets) > 0:
            lostPackets = (packet.number - self.packets[-1].number)-1
            for i in range(lostPackets):
                lastPacket = self.packets[-1]
                if self.silence:
                    silentPacket = copy.deepcopy(lastPacket)
                    silentPacket.bytes = [255] * len(lastPacket.bytes)
                    self.packets.append(silentPacket)
                else:
                    self.packets.append(lastPacket)

        self.packets.append(packet)

    def writeFile(self):
        self.byteFile = []
        for packet in self.packets:
            for byte in packet.bytes:
                self.byteFile.append(byte)
        for i in range(len(header)):
            self.byteFile[i] = int(header[i])
        with open('received_file.au', 'wb') as musicFile:
            musicFile.write(bytearray(self.byteFile))
        musicFile.close()


client = Client()
server = Server()

client.connect()
server.streamFile()
client.writeFile()