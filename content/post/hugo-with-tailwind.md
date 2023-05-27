---
title: "Hugo With Tailwind"
date: 2023-05-26
draft: false
tags: [hugo, tailwind, sites]
---

I just finished this [tutorial](https://www.hugotutorial.com/posts/2022-01-03-hugo-and-tailwindcss-3.0/) using tailwind with hugo.

Really enjoyed it and looking forward to using tailwind in future hugo themes. 

I like how there was no javascript or super involved build system. It was basically using the tailwindcss command line to build a css file.

I ran into a small issue where `$css.Permalink` was not being initialized, which is even mentioned in the tutorial but the recommended remediation didn't work for me. I'm not sure on the correct solution, so I hard-coded the css path in the baseof.html file. 
