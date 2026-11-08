---
layout: page
title: Home
custom:
  home: true
  wide: true
---
{% include JB/setup %}

<section class="post-feed" aria-labelledby="top-posts-title">
  <h2 class="section-title" id="top-posts-title">Top Posts</h2>

  {% comment %} Hand-picked list, see _data/top_posts.yml. The lookup is only to
     show a date; a pick whose url has drifted still renders, just undated.
     The data file keeps the urls extensionless (Pages serves both forms, and the
     bare url reads better), but post.url carries the .html from the permalink in
     _config.yml - so strip whatever the data has and reattach .html for the
     lookup only. {% endcomment %}
  <ol class="top-list" role="list">
    {% for pick in site.data.top_posts %}
      {% assign pick_path = pick.url | remove: ".html" %}
      {% assign lookup_url = pick_path | append: ".html" %}
      {% assign match = site.posts | where: "url", lookup_url | first %}
      <li>
        <a href="{{ BASE_PATH }}{{ pick_path }}">{{ pick.title }}</a>
        {% if match %}
          <time class="date" datetime="{{ match.date | date: '%Y-%m-%d' }}">{{ match.date | date: '%b %Y' }}</time>
        {% else %}
          <span class="date">check _data/top_posts.yml</span>
        {% endif %}
      </li>
    {% endfor %}
  </ol>
</section>

<section class="post-feed" aria-label="Latest posts">
  <h2 class="section-title">Recent posts</h2>

  <ul class="card-grid">
    {% for post in site.posts limit:9 %}
      <li class="card">
        <a href="{{ BASE_PATH }}{{ post.url }}" class="card-link">
          <h3>{{ post.title }}</h3>
          <p class="card-meta">
            <time datetime="{{ post.date | date: '%Y-%m-%d' }}">{{ post.date | date: '%b %-d, %Y' }}</time>
            {%- if post.tags.size > 0 %}
              <span class="dot">·</span> {{ post.tags | size }} tags
            {%- endif %}
          </p>
          <p class="card-excerpt">{{ post.content | strip_html | truncatewords: 22 }}</p>
        </a>
      </li>
    {% endfor %}
  </ul>

  <p class="browse">
    <a class="btn primary" href="{{ BASE_PATH }}{{ site.JB.archive_path }}">The whole archive</a>
    <a class="btn ghost" href="{{ BASE_PATH }}{{ site.JB.tags_path }}">Browse by tag</a>
    <a class="btn ghost" href="{{ BASE_PATH }}{{ site.JB.categories_path }}">Browse by category</a>
  </p>
</section>
