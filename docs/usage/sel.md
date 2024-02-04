---
title: sel
---

Use `-q` or `--query` to select classifiers based on a description:

```sh
classipypi -q "3D scientific visualisation tool"
```

```
usage: classipypi sel [-h] [-q QUERY] [-s SOURCE] [-t] [-g]

Configure source and y.

options:
  -h, --help            show this help message and exit
  -q QUERY, --query QUERY
                        The query string.
                        (default: None)
  -s SOURCE, --source SOURCE
                        The source code.
                        (default: None)
  -t, --toml            Whether to display the tags as a TOML-compatible list.
                        (default: False)
  -g, --group           Whether to display tags grouped by section.
                        (default: False)
```

Use `-s` or `--source` to select classifiers based on source code:

```sh
classipypi --source ./local_package_repo/
```
