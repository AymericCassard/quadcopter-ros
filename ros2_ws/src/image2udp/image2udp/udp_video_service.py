# All credits to Anthonin Brauer
# https://gitlab.emi.u-bordeaux.fr/abrauer/pfe-2026-suspension-system/-/blob/master/src/control/backend/udp_video_service.py?ref_type=heads

import socket
import struct

from cv2 import imencode

#:TRICKY:08/03/2026:Antonin: Compute the size of the header packed struct
# (! means network endianess, I means unsigned int, H means unsigned short)
# This represent the following C struct:
# struct __attribute__((packed)) header {
#   unsigned int    frame_id
#   unsigned short  chunk_count
#   unsigned short  chunk_idx
# }
HEADER_FORMAT = "!IHH"
HEADER_SIZE = struct.calcsize(HEADER_FORMAT)
MAX_PACKET_SIZE = 60_000 #TODO: Mettre un comment (60_000 parce que teste manuel = ">65000 => Crash")
MAX_CHUNK_SIZE = MAX_PACKET_SIZE - HEADER_SIZE


class UdpVideoService:
    host: str
    port: int
    sock: socket.socket
    frame_id: int

    def __init__(self, host: str = "0.0.0.0", port: int = 8554):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setblocking(False)
        self.frame_id = 0

    def close(self):
        self.sock.close()

    def send(self, image):
        (success, payload) = imencode(".jpg", image)
        if not success:
            print("WARNING: Failed to encode image")
            return

        payload_bytes = payload.tobytes()
        payload_len = len(payload_bytes)
        chunk_count = (payload_len + MAX_CHUNK_SIZE - 1) // MAX_CHUNK_SIZE
        if chunk_count > 65_535: #TODO:Mettre un tricky parce chunk_count est unsigned short
            print("WARNING: image too large even for chunked transfer")
            return

        current_frame_id = self.frame_id
        self.frame_id = (self.frame_id + 1)

        for chunk_idx in range(chunk_count):
            start = chunk_idx * MAX_CHUNK_SIZE
            end = min(start + MAX_CHUNK_SIZE, payload_len)
            chunk = payload_bytes[start:end]
            header = struct.pack(HEADER_FORMAT, current_frame_id, chunk_count, chunk_idx)
            packet = header + chunk
            try:
                self.sock.sendto(packet, (self.host, self.port))
            except:
                pass

