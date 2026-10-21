from __future__ import annotations

import random
import struct
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from rnp1 import (
    HEADER,
    MAGIC,
    MAX_PAYLOAD,
    Frame,
    FrameParser,
    MessageType,
    ProtocolError,
    ServerSession,
    decode_frame,
    encode_frame,
)


class Rnp1Tests(unittest.TestCase):
    def test_known_hello_vector(self) -> None:
        encoded = encode_frame(Frame(MessageType.HELLO, b"lab"))
        self.assertEqual(encoded.hex(), "524e503101010000000000036c6162")
        self.assertEqual(decode_frame(encoded), Frame(MessageType.HELLO, b"lab"))

    def test_incremental_parser_every_split(self) -> None:
        encoded = encode_frame(Frame(MessageType.DATA, b"abcdef"))
        for split in range(len(encoded) + 1):
            parser = FrameParser()
            frames = parser.feed(encoded[:split]) + parser.feed(encoded[split:])
            parser.finish()
            self.assertEqual(frames, [Frame(MessageType.DATA, b"abcdef")])

    def test_multiple_frames_in_one_chunk(self) -> None:
        parser = FrameParser()
        frames = parser.feed(encode_frame(Frame(MessageType.PING, b"x")) + encode_frame(Frame(MessageType.PONG, b"x")))
        self.assertEqual([frame.message_type for frame in frames], [MessageType.PING, MessageType.PONG])

    def test_rejects_oversized_declared_length_before_payload(self) -> None:
        header = HEADER.pack(MAGIC, 1, int(MessageType.DATA), 0, 0, MAX_PAYLOAD + 1)
        with self.assertRaises(ProtocolError):
            FrameParser().feed(header)

    def test_rejects_reserved_flags_unknown_type_and_utf8(self) -> None:
        invalid_frames = [
            HEADER.pack(MAGIC, 1, int(MessageType.DATA), 1, 0, 0),
            HEADER.pack(MAGIC, 1, 99, 0, 0, 0),
            HEADER.pack(MAGIC, 1, int(MessageType.HELLO), 0, 0, 1) + b"\xff",
        ]
        for raw in invalid_frames:
            with self.assertRaises(ProtocolError):
                decode_frame(raw)

    def test_partial_eof_is_error(self) -> None:
        parser = FrameParser()
        parser.feed(encode_frame(Frame(MessageType.DATA, b"x"))[:-1])
        with self.assertRaises(ProtocolError):
            parser.finish()

    def test_server_state_machine(self) -> None:
        session = ServerSession()
        self.assertEqual(session.handle(Frame(MessageType.HELLO, b"client"))[0].message_type, MessageType.WELCOME)
        self.assertEqual(session.handle(Frame(MessageType.PING, b"42"))[0], Frame(MessageType.PONG, b"42"))
        self.assertEqual(session.handle(Frame(MessageType.DATA, b"event")), [])
        self.assertEqual(session.handle(Frame(MessageType.CLOSE, b"done"))[0].message_type, MessageType.CLOSE)
        self.assertEqual(session.state, "CLOSED")

    def test_out_of_order_closes_session(self) -> None:
        session = ServerSession()
        response = session.handle(Frame(MessageType.DATA, b"early"))[0]
        self.assertEqual(response.message_type, MessageType.ERROR)
        self.assertEqual(session.state, "CLOSED")

    def test_bounded_random_round_trips(self) -> None:
        generator = random.Random(20261001)
        for _ in range(200):
            payload = generator.randbytes(generator.randrange(0, 257))
            frame = Frame(MessageType.DATA, payload)
            self.assertEqual(decode_frame(encode_frame(frame)), frame)

    def test_wrong_length_is_rejected(self) -> None:
        raw = HEADER.pack(MAGIC, 1, int(MessageType.DATA), 0, 0, 2) + b"x"
        with self.assertRaises(ProtocolError):
            decode_frame(raw)


if __name__ == "__main__":
    unittest.main()
