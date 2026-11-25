import pytest

from qr_payload import build_payload, parse_payload


def test_round_trip():
    payload = build_payload(42, 1700000000)
    assert parse_payload(payload) == (42, 1700000000)


def test_different_inputs_different_payload():
    assert build_payload(1, 100) != build_payload(1, 101)


def test_tampered_signature_rejected():
    payload = build_payload(5, 200)
    tampered = payload[:-1] + ("0" if payload[-1] != "0" else "1")
    with pytest.raises(ValueError):
        parse_payload(tampered)


def test_garbage_rejected():
    with pytest.raises(ValueError):
        parse_payload("garbage")


def test_negative_rejected():
    with pytest.raises(ValueError):
        build_payload(-1, 100)