import sys
import time

STAGES = [
    "mashing",
    "boiling",
    "fermenting",
    "conditioning",
    "cheers 🍻"
]


def _fmt_time(seconds: float) -> str:
    if seconds is None or seconds <= 0:
        return "00:00"

    seconds = int(round(seconds))
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)

    if h > 0:
        return f"{h:02}:{m:02}:{s:02}"
    return f"{m:02}:{s:02}"


class BrewBar:
    def __init__(
        self,
        iterable,
        width=8,
        *,
        eta=True,
        elapsed=False,
        rate=False,
        ascii=False,
    ):
        self.iterable = iterable
        self.width = width
        self.eta_enabled = eta
        self.elapsed_enabled = elapsed
        self.rate_enabled = rate
        self.ascii = ascii

        self.start_time = None
        self._last_len = 0

        try:
            self.total = len(iterable)
        except TypeError:
            self.total = None

    def __iter__(self):
        if self.total == 0:
            return iter(())

        for i, item in enumerate(self.iterable, 1):
            if self.total is None or i < self.total:
                self._render(i)
            yield item

        if self.total is not None:
            self._render(self.total)
            sys.stdout.write("\n")
            sys.stdout.flush()

    def _render(self, current):
        if self.total is None:
            return

        now = time.monotonic()

        if self.start_time is None:
            self.start_time = now

        percent = current / self.total
        filled = int(self.width * percent)
        empty = self.width - filled

        stage_index = min(
            int(percent * len(STAGES)),
            len(STAGES) - 1,
        )
        stage = STAGES[stage_index]

        bar = (
            "#" * filled + "-" * empty
            if self.ascii
            else "🍺" * filled + "░" * empty
        )

        pct = int(percent * 100)
        parts = [f"{bar}  {pct}%  {stage}"]

        elapsed = now - self.start_time
        rate = current / elapsed if elapsed > 0 else 0

        if self.elapsed_enabled:
            parts.append(f"{_fmt_time(elapsed)} elapsed")

        if self.rate_enabled and rate > 0:
            parts.append(f"{rate:.1f} it/s")

        if (
            self.eta_enabled
            and rate > 0
            and current < self.total
        ):
            remaining = (self.total - current) / rate
            parts.append(f"ETA {_fmt_time(remaining)}")

        line = "  |  ".join(parts)

        padding = max(0, self._last_len - len(line))
        sys.stdout.write("\r" + line + (" " * padding))
        sys.stdout.flush()

        self._last_len = len(line)


def bar(
    iterable,
    width=8,
    *,
    eta=True,
    elapsed=False,
    rate=False,
    ascii=False,
):
    return BrewBar(
        iterable,
        width=width,
        eta=eta,
        elapsed=elapsed,
        rate=rate,
        ascii=ascii,
    )