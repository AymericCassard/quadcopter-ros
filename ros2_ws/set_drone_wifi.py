from djitellopy import Tello

tello = Tello(host="192.168.1.22")
tello.connect()
version = tello.query_sdk_version
print(f"{version=}")
# tello.TELLO_IP = "10.42.0.2"
# tello.connect_to_wifi("Freebox-210A8C","bs9nvqzvmvqt562dqvxbhx")
# print(f"Tello connecting to network...")
