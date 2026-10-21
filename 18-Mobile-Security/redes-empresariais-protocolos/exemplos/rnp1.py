#!/usr/bin/env python3
"""Codec e máquina de estados do protocolo didático RNP/1."""

from __future__ import annotations

import enum
import socket
import struct
from dataclasses import dataclass

MAGIC = b"RNP1"
VERSION = 1
MAX_PAYLOAD = 4096
HEADER = struct.Struct("!4sBBBBI")


class ProtocolError(ValueError):
    """Frame ou transição inválida."""


class MessageType(enum.IntEnum):
    HELLO = 1
    WELCOME = 2
    DATA = 3
    PING = 4
    PONG = 5
    CLOSE = 6
    ERROR = 7


@dataclass(frozen=True)
class Frame:
    message_type: MessageType
    payload: bytes = b""


def _validate_payload(message_type: MessageType, payload: bytes) -> None:
    if len(payload) > MAX_PAYLOAD:
        raise ProtocolError("payload excede 4096 bytes")
    text_limits = {
        MessageType.HELLO: (1, 64),
        MessageType.WELCOME: (1, 128),
        MessageType.CLOSE: (0, 128),
    }
    if message_type in text_limits:
        minimum, maximum = text_limits[message_type]
        if not minimum <= len(payload) <= maximum:
            raise ProtocolError("tamanho de texto inválido")
        try:
            text = payload.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ProtocolError("texto não é UTF-8") from exc
        if "\x00" in text:
            raise ProtocolError("texto contém NUL")
    elif message_type in {MessageType.PING, MessageType.PONG} and len(payload) > 32:
        raise ProtocolError("token excede 32 bytes")
    elif message_type is MessageType.ERROR:
        if not 2 <= len(payload) <= 258:
            raise ProtocolError("payload ERROR inválido")
        try:
            message = payload[2:].decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ProtocolError("mensagem ERROR não é UTF-8") from exc
        if "\x00" in message:
            raise ProtocolError("mensagem ERROR contém NUL")


def encode_frame(frame: Frame) -> bytes:
    if not isinstance(frame.payload, bytes):
        raise ProtocolError("payload deve ser bytes")
    try:
        message_type = MessageType(frame.message_type)
    except ValueError as exc:
        raise ProtocolError("tipo desconhecido") from exc
    _validate_payload(message_type, frame.payload)
    return HEADER.pack(MAGIC, VERSION, int(message_type), 0, 0, len(frame.payload)) + frame.payload


def decode_frame(data: bytes) -> Frame:
    if len(data) < HEADER.size:
        raise ProtocolError("header truncado")
    magic, version, raw_type, flags, reserved, length = HEADER.unpack(data[: HEADER.size])
    if magic != MAGIC or version != VERSION or flags != 0 or reserved != 0:
        raise ProtocolError("header inválido")
    if length > MAX_PAYLOAD:
        raise ProtocolError("comprimento excede limite")
    if len(data) != HEADER.size + length:
        raise ProtocolError("tamanho do frame não corresponde ao header")
    try:
        message_type = MessageType(raw_type)
    except ValueError as exc:
        raise ProtocolError("tipo desconhecido") from exc
    payload = data[HEADER.size:]
    _validate_payload(message_type, payload)
    return Frame(message_type, payload)


class FrameParser:
    """Parser incremental limitado para um fluxo de bytes."""

    def __init__(self) -> None:
        self._buffer = bytearray()
        self._expected: int | None = None

    def feed(self, chunk: bytes) -> list[Frame]:
        if not isinstance(chunk, bytes):
            raise ProtocolError("chunk deve ser bytes")
        self._buffer.extend(chunk)
        frames: list[Frame] = []
        while True:
            if self._expected is None:
                if len(self._buffer) < HEADER.size:
                    break
                magic, version, raw_type, flags, reserved, length = HEADER.unpack(self._buffer[: HEADER.size])
                if magic != MAGIC or version != VERSION or flags != 0 or reserved != 0:
                    raise ProtocolError("header inválido")
                if raw_type not in {item.value for item in MessageType}:
                    raise ProtocolError("tipo desconhecido")
                if length > MAX_PAYLOAD:
                    raise ProtocolError("comprimento excede limite")
                self._expected = HEADER.size + length
            if len(self._buffer) < self._expected:
                break
            raw = bytes(self._buffer[: self._expected])
            del self._buffer[: self._expected]
            self._expected = None
            frames.append(decode_frame(raw))
        return frames

    def finish(self) -> None:
        if self._buffer or self._expected is not None:
            raise ProtocolError("EOF com frame parcial")


def error_payload(code: int, message: str) -> bytes:
    if isinstance(code, bool) or not 0 <= code <= 65535:
        raise ProtocolError("código de erro inválido")
    encoded = message.encode("utf-8")
    payload = struct.pack("!H", code) + encoded
    _validate_payload(MessageType.ERROR, payload)
    return payload


class ServerSession:
    def __init__(self) -> None:
        self.state = "WAIT_HELLO"

    def handle(self, frame: Frame) -> list[Frame]:
        if self.state == "CLOSED":
            raise ProtocolError("sessão encerrada")
        if self.state == "WAIT_HELLO":
            if frame.message_type is not MessageType.HELLO:
                self.state = "CLOSED"
                return [Frame(MessageType.ERROR, error_payload(1001, "HELLO esperado"))]
            _validate_payload(frame.message_type, frame.payload)
            self.state = "OPEN"
            return [Frame(MessageType.WELCOME, b"rnp1-ready")]
        if frame.message_type is MessageType.PING:
            return [Frame(MessageType.PONG, frame.payload)]
        if frame.message_type is MessageType.DATA:
            return []
        if frame.message_type is MessageType.CLOSE:
            self.state = "CLOSED"
            return [Frame(MessageType.CLOSE, b"closed")]
        self.state = "CLOSED"
        return [Frame(MessageType.ERROR, error_payload(1001, "mensagem fora de ordem"))]


def read_exact(sock: socket.socket, length: int) -> bytes:
    chunks = bytearray()
    while len(chunks) < length:
        chunk = sock.recv(length - len(chunks))
        if not chunk:
            raise ProtocolError("EOF inesperado")
        chunks.extend(chunk)
    return bytes(chunks)


def read_frame(sock: socket.socket) -> Frame:
    header = read_exact(sock, HEADER.size)
    magic, version, raw_type, flags, reserved, length = HEADER.unpack(header)
    if magic != MAGIC or version != VERSION or flags != 0 or reserved != 0 or length > MAX_PAYLOAD:
        raise ProtocolError("header inválido")
    return decode_frame(header + read_exact(sock, length))
