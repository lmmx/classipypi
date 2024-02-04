---
title: ls
---

```
usage: classipypi ls [-h] [-i [INCLUDE ...]] [-e [EXCLUDE ...]] [-t] [-g]

Configure input filtering and output display.

options:
  -h, --help            show this help message and exit
  -i [INCLUDE ...], --include [INCLUDE ...]
                        Strings to filter tags for.
                        (default: [])
  -e [EXCLUDE ...], --exclude [EXCLUDE ...]
                        Strings to filter tags against.
                        (default: [])
  -t, --toml            Whether to display the tags as a TOML-compatible list.
                        (default: False)
  -g, --group           Whether to display tags grouped by section.
                        (default: False)
```

For example, to show the _Development Status_ tags (but skip any with "Alpha" in):

```sh
classipypi ls -i "Development Status" -e Alpha
```

```
Development Status :: 1 - Planning
Development Status :: 4 - Beta
Development Status :: 5 - Production/Stable
Development Status :: 6 - Mature
Development Status :: 7 - Inactive
```
