# sysinfo

Collect the facts about a computer that you want attached to a bug report: operating system, memory, disks, processor, and the Python interpreter itself. [Accessible Apps](https://getaccessibleapps.com) uses it in [issue_reporter](https://github.com/accessibleapps/issue_reporter), so problem reports arrive with the details already filled in.

## Install

```bash
pip install git+https://github.com/accessibleapps/sysinfo.git
```

Needs Python 3.8 or newer and [psutil](https://pypi.org/project/psutil/). The `sysinfo` package on PyPI is a different project, so install from GitHub as shown.

## Use it

```python
import sysinfo

info = sysinfo.system_info()
info["operating_system"]["name"]   # "Windows"
info["memory"]["free"]             # bytes
info["interpreter"]["bit_width"]   # 32 or 64
```

`system_info()` returns a plain dictionary with these sections:

| Key | What's in it |
|---|---|
| `operating_system` | name, bit width, kernel version and release |
| `memory` | total, free and used RAM, in bytes |
| `storage` | each fixed disk partition (device, mount point, filesystem, size and usage), plus the total size |
| `processor` | name, and user, system and idle CPU times |
| `interpreter` | bit width, Python version, byte order, API version, recursion limit, memory used, number of live objects, Python threads and OS threads |
| `network` | the machine's fully qualified host name |
| `current_user` | the user name |

Each section also has its own function (`memory()`, `storage()`, `processor()` and so on) if you only need one.

Some values are only filled in on certain systems. The operating system bit width is only known for `x86` and `AMD64` machines (it's `None` elsewhere), and `storage` only lists partitions that psutil marks as `fixed`, which is a Windows option.

Be careful what you send: the result includes the user name and the host name.
