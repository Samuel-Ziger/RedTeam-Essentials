from __future__ import annotations

import unittest

from contract_lab.domain import Principal
from contract_lab.errors import AppError
from contract_lab.service import ItemService, decode_cursor, encode_cursor
from contract_lab.store import InMemoryStore


class ServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.service = ItemService(InMemoryStore())
        self.writer = Principal("ana", "tenant-a", "writer")
        self.reader = Principal("bia", "tenant-a", "reader")

    def test_create_is_idempotent_for_same_command(self) -> None:
        first, created = self.service.create(self.writer, "  Item   seguro  ", "create-001")
        replay, created_again = self.service.create(self.writer, "Item seguro", "create-001")
        self.assertTrue(created)
        self.assertFalse(created_again)
        self.assertEqual(first, replay)

    def test_key_reuse_with_different_command_conflicts(self) -> None:
        self.service.create(self.writer, "Primeiro item", "create-001")
        with self.assertRaises(AppError) as raised:
            self.service.create(self.writer, "Outro item", "create-001")
        self.assertEqual(raised.exception.status, 409)

    def test_reader_cannot_write(self) -> None:
        with self.assertRaises(AppError) as raised:
            self.service.create(self.reader, "Item seguro", "create-001")
        self.assertEqual(raised.exception.status, 403)

    def test_tenant_isolation_uses_not_found(self) -> None:
        item, _ = self.service.create(self.writer, "Item seguro", "create-001")
        outsider = Principal("carla", "tenant-b", "writer")
        with self.assertRaises(AppError) as raised:
            self.service.get(outsider, item.item_id)
        self.assertEqual(raised.exception.status, 404)

    def test_etag_prevents_lost_update(self) -> None:
        item, _ = self.service.create(self.writer, "Item seguro", "create-001")
        updated = self.service.update(
            self.writer,
            item.item_id,
            item.etag,
            title="Item revisado",
            status=None,
        )
        self.assertEqual(updated.version, 2)
        with self.assertRaises(AppError) as raised:
            self.service.update(
                self.writer,
                item.item_id,
                item.etag,
                title=None,
                status="archived",
            )
        self.assertEqual(raised.exception.status, 412)

    def test_cursor_pages_without_overlap(self) -> None:
        for number in range(3):
            self.service.create(self.writer, f"Item numero {number}", f"create-00{number}")
        first, cursor = self.service.list_items(self.writer, after=None, limit=2, status=None)
        second, final_cursor = self.service.list_items(self.writer, after=cursor, limit=2, status=None)
        self.assertEqual(len(first), 2)
        self.assertEqual(len(second), 1)
        self.assertIsNone(final_cursor)
        self.assertTrue(set(first).isdisjoint(second))

    def test_invalid_cursor_is_rejected(self) -> None:
        with self.assertRaises(AppError) as raised:
            decode_cursor("not+a+cursor")
        self.assertEqual(raised.exception.status, 400)

    def test_cursor_round_trip(self) -> None:
        self.assertEqual(decode_cursor(encode_cursor(42)), 42)

    def test_cursor_rejects_tampering_and_filter_change(self) -> None:
        cursor = encode_cursor(42, status="active")
        with self.assertRaises(AppError):
            decode_cursor(cursor[:-1] + ("0" if cursor[-1] != "0" else "1"), status="active")
        with self.assertRaises(AppError):
            decode_cursor(cursor, status="archived")

    def test_list_cursor_is_bound_to_filter(self) -> None:
        for number in range(3):
            self.service.create(self.writer, f"Item numero {number}", f"create-00{number}")
        _, cursor = self.service.list_items(
            self.writer,
            after=None,
            limit=1,
            status="active",
        )
        with self.assertRaises(AppError) as raised:
            self.service.list_items(
                self.writer,
                after=cursor,
                limit=1,
                status="archived",
            )
        self.assertEqual(raised.exception.code, "invalid-cursor")

    def test_events_follow_writes(self) -> None:
        item, _ = self.service.create(self.writer, "Item seguro", "create-001")
        self.service.update(
            self.writer,
            item.item_id,
            item.etag,
            title=None,
            status="archived",
        )
        self.assertEqual(
            [event.event_type for event in self.service.events(self.writer)],
            ["item.created", "item.updated"],
        )


if __name__ == "__main__":
    unittest.main()
