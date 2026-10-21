from contract_lab.signatures import ReplayGuard, sign, verify


def test_signature_checks_body_and_time() -> None:
    secret = b"local-lab-secret"
    signature = sign(b'{"event":"created"}', secret, 1000)
    assert verify(b'{"event":"created"}', secret, 1000, signature, now=1100)
    assert not verify(b'{"event":"changed"}', secret, 1000, signature, now=1100)
    assert not verify(b'{"event":"created"}', secret, 1000, signature, now=1400)


def test_short_secret_is_rejected() -> None:
    try:
        sign(b"event", b"short", 1000)
    except ValueError as error:
        assert "16 bytes" in str(error)
    else:
        raise AssertionError("segredo curto deveria falhar")


def test_malformed_signature_is_rejected() -> None:
    secret = b"local-lab-secret"
    assert not verify(b"event", secret, 1000, "invalid", now=1000)
    assert not verify(b"event", secret, True, "v1=" + "0" * 64, now=1000)


def test_replay_guard_accepts_event_only_once_inside_window() -> None:
    guard = ReplayGuard()
    assert guard.accept("evt_01", 1000, now=1000)
    assert not guard.accept("evt_01", 1000, now=1001)
    assert not guard.accept("invalid event", 1000, now=1001)
    assert not guard.accept("evt_old", 1000, now=1400)
