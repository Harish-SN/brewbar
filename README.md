# 🍺 brewbar

A progress bar for Python that **brews beer while your code runs**

No configuration | No dependencies | Just beer

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
![brewbar demo](https://raw.githubusercontent.com/Harish-SN/brewbar/main/images/demo.png)

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
import time

for _ in bar(range(100)):
    time.sleep(0.1)
```

## ✨ Features

- 🍺 Beer-brewing themed progress bar
- 🧠 Simple API (`bar(iterable)`)
- ⚡ Lightweight (no dependencies)
- 🖥 Works in standard terminals
- 🎭 Meme-friendly, screenshot-ready

## What’s new in v1.2.0
### ETA & Speed
```
ETA 00:08  |  12.5 it/s
```
### ASCII mode (CI-safe)
```python
bar(range(100), ascii=True)
```
```
Output:
    ##########  100%  cheers 🍻
```
### Disable output completely
```python
bar(range(100), disable=True)
```
### Log to stderr
```python
bar(range(100), file=sys.stderr)
```
### Manual update mode
For non-iterable workflows:
```python
from brewbar import BrewBar
import time

with BrewBar(total=10, elapsed=True, rate=True) as b:
    for _ in range(10):
        time.sleep(0.2)
        b.update()
```
### Unknown total = spinner mode
```python
for _ in bar(iter(int, 1)):
    time.sleep(0.05)
```
```
Displays:
    ⠙ brewing...
```
### Nested progress bars
```python
for _ in bar(range(3), elapsed=True):
    for _ in bar(range(10), rate=True):
        ...
```
### Beer-color mode
```python
bar(range(50), color=True)
```
## 🛠 Requirements

- Python 3.8+

## ❓ Why brewbar?

Because sometimes you don't want:
- ❌ giant APIs
- ❌ heavy deps
- ❌ walls of logs

You just want to know when your code is done…  
and have a beer while waiting. 🍻

## Example with timing options

```python
from brewbar import bar
import time

for _ in bar(
    range(200),
    eta=True,
    elapsed=True,
    rate=True,
    ascii=True,
):
    time.sleep(0.05)
```