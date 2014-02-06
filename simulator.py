__author__ = 'christue'

import random
import copy


class Server():
    global packetSize
    packetSize = 100

    def streamFile(self):
        network = Network()
        with open('pink_panther.au', 'rb') as musicFile:
            eof = False
            while not eof:
                bytes = []
                for i in range(packetSize):
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
    global threshold
    threshold = 75
    clients = []

    def connect(self, client):
        self.clients.append(client)

    def send(self, packet):
        loss = random.randint(1, 100)
        if loss <= threshold:
            for client in self.clients:
                client.receiveStream(packet)


class Client():
    global silence
    silence = True
    packets = []

    def connect(self):
        self.network = Network()
        self.network.connect(self)

    def receiveStream(self, packet):
        #packet.bytes = [255] * len(packet.bytes)
        if len(self.packets) > 0:
            lostPackets = (packet.number - self.packets[-1].number)-1
            print "Lost %s packets" % lostPackets
            for i in range(lostPackets):
                lastPacket = self.packets[-1]
                if silence:
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
        with open('received_file.au', 'wb') as musicFile:
            musicFile.write(bytearray(self.byteFile))
        musicFile.close()


client = Client()
server = Server()

client.connect()
server.streamFile()
client.writeFile()