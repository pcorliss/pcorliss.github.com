source 'https://rubygems.org'

# GitHub Pages builds this site with its own `github-pages` gem (currently v232)
# and ignores this file entirely, so pinning the versions here does not change
# what Pages runs. The point is fidelity: `jekyll build` and `jekyll serve`
# should exercise the same engine that actually publishes the site, otherwise a
# local build can pass with filters or output that Pages cannot produce.
#
# Pinned to the versions Pages reports at https://pages.github.com/versions/
# (checked Nov 2025). Bump these when that table changes.
gem "jekyll", "3.10.0"

# Transitive gems pinned too, because they decide the HTML we ship: kramdown
# turns the Markdown posts into markup and Rouge writes the syntax
# highlighting that the stylesheet colours.
gem "kramdown", "2.4.0"
gem "rouge", "3.30.0"

# Jekyll 3's kramdown converter asks for the GFM parser (Jekyll 4 does not), and
# Pages ships this gem, so posts on Pages get GFM table/autolink behaviour.
gem "kramdown-parser-gfm", "1.1.0"

# Ruby 3 dropped webrick from stdlib; Jekyll 3's `serve` still needs it.
gem "webrick", "~> 1.8"

# Local tooling, not part of the site build.
gem "rake"
