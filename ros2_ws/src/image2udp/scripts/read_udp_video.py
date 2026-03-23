# All credits to Anthonin Brauer
# https://gitlab.emi.u-bordeaux.fr/abrauer/pfe-2026-suspension-system/-/blob/master/src/scripts/debug_udp_video_receiver.py?ref_type=heads

import socket
import struct
from time import time

import cv2
import numpy as np

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
FRAME_TIMEOUT_S = 1.0


if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("127.0.0.1", 8554))
    frames: dict[int, dict[str, object]] = {}

    print("Listening for UDP video on 127.0.0.1:8554")
    print("Press 'q' in the video window to quit.")

    try:
        while True:
            packet, _ = sock.recvfrom(65535)
            now_s = time()

            if len(packet) < HEADER_SIZE:
                continue

            (frame_id, chunk_count, chunk_idx) = struct.unpack(
                HEADER_FORMAT, packet[:HEADER_SIZE]
            )
            chunk = packet[HEADER_SIZE:]

            frame_entry = frames.get(frame_id)
            if frame_entry is None:
                frame_entry = {"total": chunk_count, "chunks": {}, "updated_at": now_s}
                frames[frame_id] = frame_entry

            chunks = frame_entry["chunks"]
            assert isinstance(chunks, dict)
            chunks[chunk_idx] = chunk
            frame_entry["updated_at"] = now_s

            total = frame_entry["total"]
            assert isinstance(total, int)
            if len(chunks) != total:
                stale_ids = []
                for fid, value in frames.items():
                    updated_at = value["updated_at"]
                    assert isinstance(updated_at, float)
                    if now_s - updated_at > FRAME_TIMEOUT_S:
                        stale_ids.append(fid)
                for stale_id in stale_ids:
                    del frames[stale_id]
                continue

            assembled = b"".join(chunks[idx] for idx in range(total))
            del frames[frame_id]

            frame_buffer = np.frombuffer(assembled, dtype=np.uint8)
            frame = cv2.imdecode(frame_buffer, cv2.IMREAD_COLOR)
            if frame is None:
                continue

            cv2.imshow("UDP Video Receiver", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        sock.close()
        cv2.destroyAllWindows()
