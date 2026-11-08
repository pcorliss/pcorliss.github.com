---
layout: page
title: Home
custom:
  home: true
  wide: true
---
{% include JB/setup %}

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
