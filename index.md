---
layout: page
title: blog.50projects.com
tagline:
---
{% include JB/setup %}

<ul>
  {% for post in site.posts limit 5 %}
    <li>
      <a href="{{ post.url }}">{{ post.title }}</a>
    </li>
  {% endfor %}
</ul>

<span class="archive">
  <a class="archive" href="{{ BASE_PATH }}{{ site.JB.archive_path }}">Archive</a></li>
</span>

