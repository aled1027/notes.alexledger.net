---
title: "Til How to Use Lit and sql-js"
date: 2023-08-23T15:31:43-07:00
draft: false
tags: [frontend,html,lit,sqlite]
---

Today I did a little project with lit and querying sqlite client-side. The idea was to search a sqlite database with full-text search and render the results in a table.

## The SQLite Database

I built the database by using a version Simon Willison's TIL `build_database.py`` [script](https://github.com/simonw/til/blob/main/build_database.py). My variation of the script crawls for markdown files in a directory and creates a sqlite table using [sqlite-utils](https://sqlite-utils.datasette.io/) and enables full-text search (specifically FTS4 because it's compatible with sql-js). The script is below.

### build_database.py

```python
import pathlib
import sqlite_utils
import dataclasses
import datetime
import pandoc
import yaml


@dataclasses.dataclass
class MarkdownMetadata:
    tags: list[str]
    date: datetime.date | None
    title: str | None


class MarkdownContent:
    metadata_marker = "---"

    def __init__(self, filename: str, contents: str) -> None:
        self.filename = filename
        self.contents = contents
        self.metadata = self.parse_metadata(contents)
        self.body = self.parse_body(contents)

    def parse_body(self, contents: str) -> str:
        if not contents.startswith(self.metadata_marker):
            return contents

        end_idx = contents.find(self.metadata_marker, len(self.metadata_marker))
        if end_idx < 0:
            raise ValueError("Unable to find end of metadata section")

        body = self.contents[end_idx + len(self.metadata_marker) :]
        return body

    def parse_metadata(self, contents: str) -> MarkdownMetadata:
        if not contents.startswith(self.metadata_marker):
            return MarkdownMetadata(title="", tags=[], date=None)

        start_idx = len(self.metadata_marker)
        end_idx = contents.find(self.metadata_marker, len(self.metadata_marker))

        if end_idx < 0:
            raise ValueError("Unable to find end of metadata section")

        metadata_section = self.contents[start_idx:end_idx]
        try:
            metadata = yaml.safe_load(metadata_section)
        except Exception as e:
            print("Error reading metadata of %s" % self.filename)
            metadata = {} 

        if metadata is None:
            metadata = {}

        metadata = {k.lower(): v for k, v in metadata.items()}
        return MarkdownMetadata(
            title=metadata.get("title", ""),
            tags=metadata.get("tags", []),
            date=metadata.get("date", None),
        )

    def to_html(self) -> str:
        """https://boisgera.github.io/pandoc/api/"""
        try:
            doc = pandoc.read(self.body)
            html_body: str = pandoc.write(doc, format="html")

            # render_in: dict[str, str] = {"title": self.metadata.title, "body": html_body}
            # content = self.post_template.render(render_in)
            return html_body
        except:
            return "" 


def build_database():
    root = pathlib.Path("/path/to/files/")
    db = sqlite_utils.Database("database.db")
    table = db.table("notes", pk="path")

    if not table.exists():
        table.create({"slug": str, "title": str, "body": str, "html": str, "path": str, "metadata": dict})

    for filepath in root.glob("**/*.md"):
        path = str(filepath.relative_to(root))
        path_slug = path.replace("/", "_")
        with open(filepath) as fp:
            body = fp.read().strip()
        slug = filepath.stem

        markdown_content = MarkdownContent(str(filepath), body)
        metadata_dict = dataclasses.asdict(markdown_content.metadata)
        if metadata_dict.get("date") is not None:
            metadata_dict["date"] = metadata_dict["date"].isoformat()

        title = metadata_dict.get("title")
        if not title:
            title = slug

        record = {
            "slug": slug,
            "title": title,
            "body": body,
            "html": markdown_content.to_html(),
            "path": path_slug,
            "metadata": metadata_dict,
        }

        with db.conn:
            table.upsert(record, alter=True)

    # FTS4 works with sql-js. FTS5 (the default) does not work with sql-ls.
    table.enable_fts(
        ["title", "body", "html"], fts_version="FTS4", tokenize="porter", create_triggers=True, replace=True
    )


if __name__ == "__main__":
    build_database()


```


## Using sql-js

[sql-js](https://sql.js.org/#/) is a javascript sqlite database. In my use-case, I loaded in the database from a url, `/database.db`, then queried it with a SQL query to get the results.

In `dist/` I have a copy of the wasm sql-js file from a CDN.

The basic code for this to work is the following[^1]. Since this was a quick project, I didn't worry about performance or blocking, and I ran into a few funny things with Lit that I didn't resolve.

Also, note that the entire database is readable to the client, so I didn't worry about SQL injection or anything like that.


```javascript
const searchTerm = this.input.value;

let config = {};

initSqlJs(config)
    .then(async function (SQL) {
        const buf = await fetch("/database.db").then((res) =>
            res.arrayBuffer()
        );
        const db = new SQL.Database(new Uint8Array(buf));

        // fts4 works with sql-js!
        const limit = 50;
        const query = `
        with original as (
            select
              rowid,
              *
            from
              [notes]
          )
          SELECT
            DISTINCT original.title,
            LENGTH(snippet(notes_fts)) AS score,
            snippet(notes_fts) as snippet,
            original.html
          FROM
            original
            join notes_fts on original.rowid = [notes_fts].rowid
          where
            notes_fts.html MATCH '${searchTerm}'
          ORDER BY
            LENGTH(snippet(notes_fts)) ASC
          LIMIT
            ${limit}
        `

        const stmt = db.prepare(query);

        let items = [];
        while(stmt.step()) {
            const row = stmt.getAsObject();
            items.push({
                rank: items.length,
                title: row.title,
                score: row.score,
                snippet: row.snippet,
                html: row.html,
            });
        }

        return items;
    })
    .then((items) => {
        // for some reason I don't understand, _listItems isn't accessible in the async function
        this._listItems = items;
    });
```

[^1]: Since this was a quick project, I didn't worry about performance or blocking, and I ran into a few funny things with Lit that I didn't resolve.

## Using Lit

I followed the [Intro to Lit](https://lit.dev/tutorials/intro-to-lit/) tutorial and modified the todo app inside of it for this.

A key thing was how to get Lit to work without using node. The best way I found was documented [here]( https://lit.dev/docs/getting-started/#use-bundles) and was to import with

```
import {LitElement, html, unsafeHTML } from 'https://cdn.jsdelivr.net/gh/lit/dist@2/all/lit-all.min.js'
```

The rest of the app contained the following:

### index.html
```html

<meta charset="utf8" />
<html>
<head>
  <script src='/dist/sql-wasm.js'></script>
  <script type="module" src="script.js"></script>
</head>
<body>
  <search-element></search-element>
</body>
</html>
```

### script.js

```javascript
import {LitElement, html, unsafeHTML } from 'https://cdn.jsdelivr.net/gh/lit/dist@2/all/lit-all.min.js'

export class SearchElement extends LitElement {
    static properties = {
        _listItems: { state: true },
    };

    constructor() {
        super();
        this._listItems = [];
    }

    render() {
        return html`
            <h2>Search Notes</h2>
            <input id="searchterm" aria-label="Search" />
            <button @click=${this.searchFromDatabase}>Search</button>
            <table border="1">
                <thead>
                    <th>Rank</th>
                    <th>Title</th>
                    <th>Score</th>
                    <th>Snippet</th>
                    <th>Note</th>
                </thead>
                <tbody>
                    ${this._listItems.map(
                        (row) => html` <tr>
                            <td>${row.rank}</td>
                            <td>${row.title}</td>
                            <td>${row.score}</td>
                            <td>${unsafeHTML(row.snippet)}</td>
                            <td>${unsafeHTML(row.html)}</td>
                        </tr>`
                    )}
                </tbody>
            </table>
        `;
    }

    get input() {
        return this.renderRoot?.querySelector("#searchterm") ?? null;
    }

    searchFromDatabase() {
        const searchTerm = this.input.value;

        let config = {
            locateFile: (filename) => `/dist/${filename}`,
        };

        initSqlJs(config)
            .then(async function (SQL) {
                const buf = await fetch("/database.db").then((res) =>
                    res.arrayBuffer()
                );
                const db = new SQL.Database(new Uint8Array(buf));

                // fts4 works with sql-js!
                const limit = 50;
                const query = `
                with original as (
                    select
                      rowid,
                      *
                    from
                      [notes]
                  )
                  SELECT
                    DISTINCT original.title,
                    LENGTH(snippet(notes_fts)) AS score,
                    snippet(notes_fts) as snippet,
                    original.html
                  FROM
                    original
                    join notes_fts on original.rowid = [notes_fts].rowid
                  where
                    notes_fts.html MATCH '${searchTerm}'
                  ORDER BY
                    LENGTH(snippet(notes_fts)) ASC
                  LIMIT
                    ${limit}
                `

                const stmt = db.prepare(query);
                let items = [];
                while(stmt.step()) {
                    const row = stmt.getAsObject();
                    items.push({
                        rank: items.length,
                        title: row.title,
                        score: row.score,
                        snippet: row.snippet,
                        html: row.html,
                    });
                }

                return items;
            })
            .then((items) => {
                // for some reason I don't understand, _listItems isn't accessible in the async function
                this._listItems = items;
            });
    }
}
customElements.define("search-element", SearchElement);
```