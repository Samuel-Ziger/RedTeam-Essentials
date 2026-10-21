#!/usr/bin/env python3
"""Executa uma sessão RNP/1 real sobre socketpair, sem abrir portas."""

from __future__ import annotations

import json
import socket

from rnp1 import Frame, FrameParser, MessageType, ServerSession, decode_frame, encode_frame, read_frame


def exchange(client: socket.socket, server: socket.socket, session: ServerSession, frame: Frame) -> list[Frame]:
    client.sendall(encode_frame(frame))
    received = read_frame(server)
    responses = session.handle(received)
    for response in responses:
        server.sendall(encode_frame(response))
    return [read_frame(client) for _ in responses]


def exchange_in_memory(session: ServerSession, frame: Frame) -> list[Frame]:
    """Fallback para sandboxes que proíbem até sockets locais."""
    raw = encode_frame(frame)
    parser = FrameParser()
    midpoint = min(5, len(raw))
    received = parser.feed(raw[:midpoint]) + parser.feed(raw[midpoint:])
    parser.finish()
    responses = session.handle(received[0])
    return [decode_frame(encode_frame(response)) for response in responses]


def run_sequence(sequence: list[Frame], *, use_sockets: bool) -> list[dict[str, object]]:
    session = ServerSession()
    transcript: list[dict[str, object]] = []
    client: socket.socket | None = None
    server: socket.socket | None = None
    if use_sockets:
        client, server = socket.socketpair()
    try:
        for request in sequence:
            responses = (
                exchange(client, server, session, request)
                if client is not None and server is not None
                else exchange_in_memory(session, request)
            )
            transcript.append({
                "request": request.message_type.name,
                "responses": [response.message_type.name for response in responses],
            })
    finally:
        if client is not None:
            client.close()
        if server is not None:
            server.close()
    return transcript


def main() -> int:
    sequence = [
        Frame(MessageType.HELLO, b"course-client"),
        Frame(MessageType.DATA, b"link-state=healthy"),
        Frame(MessageType.PING, b"42"),
        Frame(MessageType.CLOSE, b"done"),
    ]
    transport = "socketpair"
    try:
        transcript = run_sequence(sequence, use_sockets=True)
    except OSError:
        transport = "in-memory-fragmented-stream"
        transcript = run_sequence(sequence, use_sockets=False)
    print(json.dumps({"protocol": "RNP/1", "transport": transport, "transcript": transcript}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
