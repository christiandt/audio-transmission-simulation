audio-transmission-simulation
=============================

The audio-trnsmission-simulation is a simulator for simulating packet loss in a network. The program use au-files, and can be configured with varying packet-loss, and packet length. Audio is sent from the server class to the client class using the network-class to insert packet loss. The packet class is used for simulating packets.

the two ways to handle packet-loss is either to replay the lost package, or keep silent for the duration of the lost packet. Thr way to handle packet-loss can be changed in the client-class using the silence-boolean. True = silence, False = replay. Different methods will work better with some types of audio than others. Play with the simulator and find out for yourself.

### The following is variable in each class
- Server: packetSize (size of the packet)
- Network: threshold (the threshold for dropping package)
- Client: silence (how to handle packet-loss)

### Running the simulator
Create one or more clients, create a server, connect clients to server, stream file from server, write file in client. This can be done the following way:

    client = Client()
    server = Server()
    client.connect()
    server.streamFile()
    client.writeFile()
