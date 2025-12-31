import sys
import time
import shutil
import threading

STAGES = [
    "mashing",
    "boiling",
    "fermenting",
    "conditioning",
    "cheers 🍻"
]

SPINNER = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"


def _fmt_time(seconds: float) -> str:
    if not seconds or seconds < 0:
        return "00:00"

    seconds = int(seconds)
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)

    return f"{h:02}:{m:02}:{s:02}" if h else f"{m:02}:{s:02}"


class BrewBar:
    """Minimal, fun, beer-brewing progress bar 🍺"""

    _lock = threading.Lock()
    _active_bars = 0

    def __init__(
        self,
        iterable=None,
        total=None,
        *,
        width=12,
        eta=True,
        elapsed=False,
        rate=False,
        ascii=False,
        disable=False,
        file=None,
        color=False,
        refresh=1/20,  # 20fps max
    ):
        self.file = file or sys.stdout
        self.iterable = iterable
        self.disable = disable
        self.ascii = ascii
        self.color = color
        self.refresh = refresh

        self.width = width
        self.eta_enabled = eta
        self.elapsed_enabled = elapsed
        self.rate_enabled = rate

        self.start_time = None
        self.last_render = 0
        self._last_len = 0
        self._spinner_index = 0
        self._rate_window = []

        # nesting depth
        self.level = BrewBar._active_bars

        # detect total
        if total is not None:
            self.total = total
        else:
            try:
                self.total = len(iterable)
            except Exception:
                self.total = None

        self.current = 0

    # -------- Context Manager -------- #

    def __enter__(self):
        BrewBar._active_bars += 1
        return self

    def __exit__(self, *_):
        self.close()

    # -------- Manual Mode -------- #

    def update(self, n=1):
        if self.disable:
            return

        if self.start_time is None:
            self.start_time = time.monotonic()

        self.current += n
        self._render()

    def close(self):
        if not self.disable:
            self._render(final=True)
            self.file.write("\n")
            self.file.flush()

        BrewBar._active_bars = max(0, BrewBar._active_bars - 1)

    # -------- Iterator API -------- #

    def __iter__(self):
        if self.disable:
            yield from self.iterable
            return

        if self.total == 0:
            return iter(())

        self.start_time = time.monotonic()

        for item in self.iterable:
            self.current += 1
            self._render()
            yield item

        self.close()

    # -------- Core Rendering -------- #

    def _render(self, final=False):
        now = time.monotonic()

        # refresh throttle
        if not final and (now - self.last_render) < self.refresh:
            return

        self.last_render = now

        if self.start_time is None:
            self.start_time = now

        with BrewBar._lock:

            indent = "  " * self.level

            # Unknown length → spinner mode
            if self.total is None:
                frame = SPINNER[self._spinner_index % len(SPINNER)]
                self._spinner_index += 1
                line = f"{indent}{frame} brewing..."
                self._write(line)
                return

            percent = min(1, self.current / self.total)
            filled = int(self.width * percent)
            empty = self.width - filled

            stage = STAGES[min(int(percent * len(STAGES)), len(STAGES) - 1)]

            bar = (
                "#" * filled + "-" * empty
                if self.ascii
                else "🍺" * filled + "░" * empty
            )

            pct = int(percent * 100)

            parts = [f"{bar} {pct:3d}% {stage}"]

            elapsed = now - self.start_time
            rate = self.current / elapsed if elapsed > 0 else 0

            self._rate_window.append(rate)
            self._rate_window = self._rate_window[-10:]
            smooth_rate = sum(self._rate_window) / len(self._rate_window)

            if self.elapsed_enabled:
                parts.append(f"{_fmt_time(elapsed)} elapsed")

            if self.rate_enabled and smooth_rate > 0:
                parts.append(f"{smooth_rate:.1f} it/s")

            if (
                self.eta_enabled
                and smooth_rate > 0
                and self.current < self.total
            ):
                remaining = (self.total - self.current) / smooth_rate
                parts.append(f"ETA {_fmt_time(remaining)}")

            text = "  |  ".join(parts)

            # auto clamp to terminal width
            term_width = shutil.get_terminal_size((80, 20)).columns
            text = text[: term_width - len(indent) - 2]

            if self.color:
                text = f"\033[91m{text}\033[0m"

            self._write(indent + text)

    def _write(self, line):
        padding = max(0, self._last_len - len(line))
        self.file.write("\r" + line + (" " * padding))
        self.file.flush()
        self._last_len = len(line)


def bar(*args, **kwargs):
    return BrewBar(*args, **kwargs)