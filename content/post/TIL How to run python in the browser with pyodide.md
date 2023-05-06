---
date: 2023-04-09
tags:
    - python
    - til
    - pyodide
title: TIL How to run python in the browser with pyodide
---

# TIL How to run python in the browser with pyodide

[Pyodide](https://pyodide.org)  is a Python distribution for the browser that's based on WebAssembly.

I've been meaning to try it for a while, so I gave it whirl when I wanted to create a simple site that given a JSON file with nested objects would flatten the data and output a CSV file.

The flattener that I made can be found here: https://flattener.netlify.app/.

And here's the index.html that drives everything:

```
<!doctype html>
<html>

<head>
  <script src="https://cdn.jsdelivr.net/pyodide/v0.22.1/full/pyodide.js"></script>
</head>

<body>
  <div>
    <h1>JSON Flattener</h1>
    <div>
      Provide a JSON file. The File will be processed, all in your browser, into a CSV file that can be loaded.
      <br>
      <br>
      Keys in the json file will be flattened with two underscores, "__", as the separator.
      <br>
      <br>
      For example:
      <br>
      JSON Input: [{"foo1": 3, "foo2": {"bar": "meow"}]
      <br>
      CSV Output Columns: "foo1" and "foo2__bar"
    </div>
    <div>
      <br>
      JSON file:
      <button>Select file</button>
    </div>
    <br>
    <br>
  </div>

  <script type="text/javascript">
    async function main() {
      // Get the file contents into JS
      const [fileHandle] = await showOpenFilePicker();
      const fileData = await fileHandle.getFile();
      const contents = await fileData.text();

      // Create the Python convert toy function
      let pyodide = await loadPyodide();
      await pyodide.loadPackage("pandas")

      let process = pyodide.runPython(`
from pyodide.ffi import to_js
import json
import pandas as pd
def process(contents):
    print(contents)
    deserialized = json.loads(contents)
    print(deserialized)
    df = pd.json_normalize(deserialized, sep="__")
    csv_str = df.to_csv(index=False)
    return to_js(csv_str)
process
      `);

      let result = process(contents);
      console.log(result);

      const blob = new Blob([result], { type: 'text/csv' });

      let url = window.URL.createObjectURL(blob);

      var downloadLink = document.createElement("a");
      downloadLink.href = url;
      downloadLink.text = "Download CSV";
      downloadLink.download = "out.csv";
      document.body.appendChild(downloadLink);

    }
    const button = document.querySelector('button');
    button.addEventListener('click', main);
  </script>
</body>

</html>
```

## Resources

- [Pyodide quickstart](https://pyodide.org/en/stable/usage/quickstart.html)
- [A good stackoverflow question with inputs and outputs](https://stackoverflow.com/questions/75860805/pass-dropdown-menu-selection-to-pyodide)
- [Datasette-lite](https://simonwillison.net/2022/May/4/datasette-lite/) uses pyodide with a webworker.



