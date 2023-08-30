generate docs-source from docstring
```bash
sphinx-apidoc -o ./source ..
```

generate html docs from sources
```bash
sphinx-build -b html ./source/ ./build/html
```