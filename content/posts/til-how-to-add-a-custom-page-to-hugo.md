---
title: "TIL How to Add a Custom Page to Hugo"
date: 2023-08-15T12:56:16-07:00
draft: false
tags: [hugo, websites]
---

## Making the Page

I actually already knew how to do this, but it took my brain a bit to recall the keystrokes, so writing up a TIL.

In this example, I'm going to make a projects page that'll be at the url `/projects`.

1. Create a content directory: `mkdir -p content/projects`
2. Add a default page: `touch -p content/projects/_default.md`
3. Add metadata to the `content/projects/_default.md` that's used in the generated html.
    ```md
    ---
    title: Projects
    ---
    ``` 
3. Add the layout page: `touch layouts/section/projects.html`
    - If desired, instead add this to your theme. For this, that's in `themes/hugo-blog-awesome/layouts`

## Alternative, and this worked much better

1. Create a content directory: `mkdir -p content/projects`
2. Add a default page: `touch -p content/projects/_default.md`
3. Write the content in the page
4. Make sure that the list template that's used at `/projects` uses `{{ .Content }}`.
    - For example, I needed to make sure that `{{ .Content }}` was in `themes/hugo-blog-awesome/layouts/_default/list.html`
        ```html
        {{- define "main" -}}
        <div class="wrapper list-page">
            <header class="header">
                <h1 class="header-title center">{{ .Title }}</h1>
            </header>
            <main class="page-content" aria-label="Content">
                {{ .Content }}
                {{ range .Pages.GroupByDate "2006" }}
                {{ $year := .Key }}
                <h2 class="post-year">{{ $year }}</h2>

                {{/* create a list of posts for each month, with month as heading */}}

                {{ range .Pages }}

                {{ partial "postCard" . }}

                {{ end }} {{/* end range .Pages */}}

                {{ end }} {{/* end range .Pages.GroupByDate "2006" */}}

            </main>
        </div>
        {{- end -}}
        ```



## More Resources

- https://discourse.gohugo.io/t/creating-static-content-that-uses-partials/265/19?u=royston