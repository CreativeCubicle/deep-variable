# Deep Variable 🚀

[![CI](https://github.com/CreativeCubicle/deep-variable/actions/workflows/ci.yml/badge.svg)](https://github.com/CreativeCubicle/deep-variable/actions)
[![PyPI version](https://badge.fury.io/py/deep-variable.svg)](https://badge.fury.io/py/deep-variable)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Versions](https://img.shields.io/pypi/pyversions/deep-variable.svg)](https://pypi.org/project/deep-variable/)

**Deep Variable** is a lightweight, zero-dependency Python utility designed to eliminate `KeyError` and `TypeError` crashes when working with deeply nested data structures.

---

## ✨ Features

* **Safe Traversal**: Access deeply nested keys without worrying about missing parents.
* **Intelligent List Navigation**: Treat string indices (e.g., `"0"`) as list offsets automatically.
* **Zero Dependencies**: Pure Python Standard Library implementation—fast and secure.
* **Fully Type-Hinted**: Optimized for IDE IntelliSense and `mypy` strict mode.
* **Custom Separators**: Use dots, slashes, or any delimiter that fits your data.

---

## 🚀 The Difference

### The Old Way (Standard Python)
```python
# This is fragile and hard to read
email = None
if data and "users" in data and len(data["users"]) > 0:
    profile = data["users"][0].get("profile")
    if profile:
        email = profile.get("email", "default@site.com")
```

### The Deep Variable Way

```
from deep_variable import DeepVariable

# Flat, clean, and crash-proof
email = DeepVariable.get(data, "users.0.profile.email", default="default@site.com")
```
### 📦 Installation
Install the latest version using pip or uv:

```
pip install deep-variable
# OR
uv add deep-variable
```

### 🛠 Usage Examples
1. Safe Reading (Getter)
```
Python
data = {"org": {"teams": [{"name": "Engineering"}]}}
```

### Navigate through mixed Dicts and Lists
```
name = DeepVariable.get(data, "org.teams.0.name") # Returns "Engineering"
```
### Safe default on missing path
```
role = DeepVariable.get(data, "org.teams.0.role", default="Developer") # Returns "Developer"
```
### 2. Existence Checking
```
Python
data = {"status": {"active": False}}
```
### Returns True even if the value is Falsy
```
DeepVariable.has(data, "status.active") # True
DeepVariable.has(data, "status.missing") # False
```
### 3. Safe Writing (Setter)
```
Python
data = {}
```
#####  Automatically creates intermediate dictionaries
```
DeepVariable.set(data, "meta.tags.primary", "python")
print(data) # {'meta': {'tags': {'primary': 'python'}}}
```
### 🛡 Performance & Safety
Iterative Logic: Unlike recursive utilities, deep-variable uses loops, making it safe for exceptionally deep JSON structures without risking a RecursionError.

Strict Typing: Built with mypy --strict compliance