---
date: 2023-03-01
tags:
    - design
title: Interesting Plumbing Behind Personal Websites
---
# Interesting Plumbing Behind Personal Websites

People do some cool and fascinating things with their personal websites. This note documents some sites I've come across that have inspired me with their experiments, interesting technical plumbing, and philosophies of websites.

## [gwern.net](https://gwern.net)

[gwern.net](https://gwern.net) is a blog that can feel like a wiki. It's intentionally designed to resemble many aspects of Wikipedia but with many additions and experiments.

The [about](https://gwern.net/about) page describes the sites and their constructions. Under the hood, it's a statically generated site compiled with pandoc and Hakyll.

The [design](https://gwern.net/design) of the site is extensively documented and engaging with its use of a Wikipedia layout, side notes, footnotes, page previews, popins, and popups.

### Things I like about Gwern's Site

- The Page Previews and popins are so fun. I think about them all the time and the richness they add to a web-reading experience. Reading Gwern's site was one of the few times since I found Wikipedia and Reddit nearly two decades ago that I felt the web was a much richer and more immersive reading and sharing experience than books.

## Simon Willison's sites

Two of Simon Willison's sites - [TILs](https://simonwillison.net/2020/Apr/20/self-rewriting-readme/) and [Niche Museums](https://simonwillison.net/2019/Nov/25/niche-museums/) -  use an interesting baked data pattern that Simon described [here](https://simonwillison.net/2021/Jul/28/baked-data/) where a SQLite database is deployed with the site, and the site effectively a set of jinja templates on top of a deployed SQLite database.

The sites are described in more detail [here](https://github.com/simonw/til) and [here](https://simonwillison.net/2020/Apr/20/self-rewriting-readme/).

### What I like about Simon's sites

- Sqlite gives you so much power. You can run arbitrary queries in the HTML to get data in whatever shape is needed.
- SQLite has a nice full-text search capability
- The concepts are conceptually simple. Of all the build processes I saw, this was the simplest conceptually, despite its significant innovation and departure from standard blogs.
- Clever uses of GitHub actions to construct and build content

## Amos's [fasterthanli.me](https://fasterthanli.me)

The construction of Amos's website is extensively described in his [a new website for 2020](https://fasterthanli.me/articles/a-new-website-for-2020) post. The post is an extended and fun read, documenting his move from Hugo to his own static-site generator.

Amos landed on a site with:

- Zola (a rust static site generator)
- Use SQLite, especially for full-text search
- [Liquid](https://shopify.github.io/liquid/) for templating

### What I like About Amos's Site

- I liked Amos's thoughtful write-up and migration to the new site structure
- I like the use of SQLite for full-text search. Simon Willison also leverages this.

I did feel like the site was over-engineered for what it's doing. But each decision was justified and thought-through, which can always be appreciated, especially when it's out there for the public to consume and learn from.

## Linus Lee's [Thesephist](https://thesephist.com/)

Written in a custom programming language with tons of tools. All of the code is available on github. Really fun to peruse.

## Patterns Across the Sites

- All three sites above used Cloudflare for their CDN, even if the site was already behind some other scaling tool like Cloudfront.
- Many write in markdown
- Many use a templating language; Liquid and Jinja are used.
- A lot of them break the rules, doing their own thing for fun and experimentation - the web affords a lot of flexibility.

## Static Site Generators

I love the concept of static site generators, but I have found their maintenance and customizability limiting.

I want to play with custom features, especially interesting design experiments like Gwern did to make the web a richer reading experience.

Here's a list of some of the static site generators that I came across and played with in making my most recent sites:

- [Hugo](https://gohugo.io/) (Go)
- [Jekyll](https://jekyllrb.com/) (Ruby)
- [Zola](https://www.getzola.org/) (Rust)
- [Pelican](https://getpelican.com/) (Python)
- [Gatsby](https://www.gatsbyjs.com/docs/glossary/static-site-generator/) (Javascript)
- [Astro](https://astro.build/) (Javascript, but also more than an SSG)
- [Hakyll](https://jaspervdj.be/hakyll/) (Haskell)

And here are some more optimized for Documentation:

- [Mkdocs](https://www.mkdocs.org/) (Python)
- [mdBook](https://rust-lang.github.io/mdBook/) (Rust)

The jamstack site has hundreds listed [here](https://jamstack.org/generators/).

