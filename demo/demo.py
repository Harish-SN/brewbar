import sys
import time
from brewbar import bar, BrewBar


def test_default():
    print("\n--- default (ETA only) ---")
    for _ in bar(range(20)):
        time.sleep(0.1)


def test_elapsed_and_rate():
    print("\n--- elapsed + rate ---")
    for _ in bar(range(20), elapsed=True, rate=True):
        time.sleep(0.1)


def test_ascii_mode():
    print("\n--- ASCII mode (CI-safe) ---")
    for _ in bar(range(20), elapsed=True, rate=True, ascii=True):
        time.sleep(0.1)


def test_fast_loop():
    print("\n--- fast loop (no sleep) ---")
    for _ in bar(range(500), rate=True):
        pass


def test_single_item():
    print("\n--- single-item iterable ---")
    for _ in bar(range(1), elapsed=True, rate=True):
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


def test_manual_mode():
    print("\n--- manual update mode ---")
    with BrewBar(total=25, elapsed=True, rate=True) as b:
        for _ in range(25):
            time.sleep(0.08)
            b.update()


def test_unknown_total():
    print("\n--- unknown total (spinner mode) ---")

    def endless():
        while True:
            yield None

    for i, _ in enumerate(bar(endless())):
        time.sleep(0.05)
        if i > 30:
            break


def test_nested_bars():
    print("\n--- nested bars ---")
    for _ in bar(range(3), elapsed=True):
        time.sleep(0.2)
        for _ in bar(range(10), rate=True):
            time.sleep(0.05)


def test_color_mode():
    print("\n--- color mode (default beer color) ---")
    for _ in bar(range(20), elapsed=True, color=True):
        time.sleep(0.08)


def test_color_variants():
    print("\n--- color variants ---")
    for color in ("red", "green", "blue", "yellow"):
        print(f"\ncolor={color}")
        for _ in bar(range(10), color=color):
            time.sleep(0.05)


def test_ci_safe():
    print("\n--- CI-safe / non-TTY simulation ---")
    disable = not sys.stdout.isatty()
    for _ in bar(range(10), ascii=True, disable=disable):
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
    test_manual_mode()
    test_unknown_total()
    test_nested_bars()
    test_color_mode()
    test_color_variants()
    test_ci_safe()

    print("\n🍺 All brewbar tests completed.\n")