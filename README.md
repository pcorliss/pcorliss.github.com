# Local development

```
bundle install
bundle exec rake preview                    # build, serve on :4000, watch for changes
bundle exec rake post title="A New Post"    # scaffold a post in ./_posts
```

The toolchain is pinned to exactly the versions GitHub Pages runs, because Pages
ignores this repo's Gemfile and builds with its own `github-pages` gem. Pinning
means `jekyll build` exercises the engine that actually publishes the site.

Check that the pins have not drifted:

```
python3 tools/check_pages_versions.py
```

# Checks

```
bundle exec jekyll build
bundle exec jekyll serve                    # in another shell
python3 tools/verify_site.py                # every internal link + #anchor over HTTP
```

`tools/verify_site.py` walks `_site`, fetches every site-relative link from the
running server and checks status codes, `#fragment` targets both within a page
and across pages, and reports `http://` references that a modern browser would
flag as mixed content.

Other tools:

- `tools/recover_images.py` - finds external images referenced by posts, checks
  them, pulls dead ones out of the Wayback Machine into `images/recovered/` and
  rewrites the post to use the local copy. Writes a manifest to
  `/tmp/image-map.json`.
- `tools/check_pages_versions.py` - diffs the pinned gems against
  https://pages.github.com/versions/.

# Deployment

Pages builds from `master`, so pushing is the deploy.

```
git push origin master
```

# Jekyll-Bootstrap

This site started as a [Jekyll-Bootstrap](http://jekyllbootstrap.com) skeleton.
The parts still in use are the `JB/*` includes and the `rake post` / `rake page`
tasks; the theme helpers it documents are mostly dead. 0.3.0, versioned using
[semantic versioning](http://semver.org/).
