import sys
import time
from brewbar import bar


def test_default():
    print("\n--- default (ETA only) ---")
    for _ in bar(range(20)):
        time.sleep(0.1)


def test_elapsed_and_rate():
    print("\n--- elapsed + rate ---")
    for _ in bar(
        range(20),
        elapsed=True,
        rate=True,
    ):
        time.sleep(0.1)


def test_ascii_mode():
    print("\n--- ASCII mode ---")
    for _ in bar(
        range(20),
        elapsed=True,
        rate=True,
        ascii=True,
    ):
        time.sleep(0.1)


def test_fast_loop():
    print("\n--- fast loop (no sleep) ---")
    for _ in bar(
        range(500),
        rate=True,
    ):
        pass


def test_single_item():
    print("\n--- single-item iterable ---")
    for _ in bar(
        range(1),
        elapsed=True,
        rate=True,
    ):
        time.sleep(0.2)


def test_empty_iterable():
    print("\n--- empty iterable ---")
    for _ in bar(range(0)):
        pass


def test_disable():
    print("\n--- disable=True ---")
    for _ in bar(range(20), disable=True):
        time.sleep(0.05)


def test_stderr():
    print("\n--- output to stderr ---")
    for _ in bar(range(20), rate=True, file=sys.stderr):
        time.sleep(0.05)


if __name__ == "__main__":
    test_default()
    test_elapsed_and_rate()
    test_ascii_mode()
    test_fast_loop()
    test_single_item()
    test_empty_iterable()
    test_disable()
    test_stderr()
