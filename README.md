# notes.alexledger.net

## Search

Search is supported with [pagefind](https://pagefind.app/).

## Usage

```bash
# Serve the site locally
hugo serve

# Serve the site locally with drafts
hugo serve -D

# Build the site with search
hugo
npx -y pagefind --site public

# Serve the site with search from the public dir
npx -y serve public
```

## Initial Setup


```
# Install and create
brew install hugo
hugo new site notes.alexledger.net

# Download theme instead of git clone
cd themes
curl -O https://github.com/jbub/ghostwriter/archive/master.zip
unzip ghostwriter-master.zip
mv ghostwriter-master ghostwriter
cd ..

# Copy in starting material
cp -r themes/ghostwriter/exampleSite/content/page content/
cp -r themes/ghostwriter/exampleSite/content/post content/

# Paste the following into config.toml (from the site below)
baseurl = "/"
title = "My blog"
theme = "ghostwriter"

[Params]
    mainSections = ["post"]
    intro = true
    headline = "My headline"
    description = "My description"
    github = "https://github.com/XXX"
    twitter = "https://twitter.com/XXX"
    email = "XXX@example.com"
    opengraph = true
    shareTwitter = true
    dateFormat = "Mon, Jan 2, 2006"

[Permalinks]
    post = "/:filename/"


# Now run hugo serve
hugo server

# Navigate to http://127.0.0.1:1313/
```

Followed https://flaviocopes.com/start-blog-with-hugo/.
