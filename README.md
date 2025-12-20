# 🍺 brewbar

A progress bar for Python that **brews beer while your code runs**.

No configuration.  
No dependencies.  
Just beer.

---

## 🍻 Demo
```python
from brewbar import bar
import time

for _ in bar(range(50)):
    time.sleep(0.05)
```

**Output:**
```
🍺🍺🍺🍺░░░░  50%  fermenting
```

As progress increases, the beer fills and the brew stage changes:

- mashing
- boiling
- fermenting
- conditioning
- cheers 🍻

## 📦 Installation
```bash
pip install brewbar
```

## 🍺 Usage
```python
from brewbar import bar

for _ in bar(range(100)):
    time.sleep(0.1)
```

## ✨ Features

- 🍺 Beer-brewing themed progress bar
- 🧠 Simple API (`bar(iterable)`)
- ⚡ Lightweight (no dependencies)
- 🖥 Works in standard terminals
- 🎭 Meme-friendly, screenshot-ready

## 🛠 Requirements

- Python 3.8+

## ❓ Why brewbar?

Because sometimes you don't want:
- 20 configuration options
- nested progress bars
- noisy output

You just want to know when your code is done…  
and have a beer while waiting. 🍻

## ⏱ Timing Metrics (v1.0.0)

brewbar can optionally show:

- ETA (estimated time remaining)
- Elapsed runtime
- Processing speed (items/sec)
- ASCII fallback for CI / logs

```python
from brewbar import bar

for _ in bar(
    range(200),
    eta=True,
    elapsed=True,
    rate=True,
    ascii=True
):
    work()
```