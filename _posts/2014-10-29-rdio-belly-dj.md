---
layout: post
title: "Rdio & Belly DJ"
description: ""
category: 
tags: []
comments: false
---
{% include JB/setup %}

### TLDR: [belly-dj.herokuapp.com](http://belly-dj.herokuapp.com/)

I started looking for full-time work recently and a co-worker of mine mentioned [Belly](https://tech.bellycard.com/join/).
When I took a peek at their engineering page I was particularly excited by the [front-end JS challenge](https://tech.bellycard.com/join/#javascript-audio-player) they had posted.

The basic gist is [Belly](https://tech.bellycard.com/join/) provides a wrapper around the [Rdio API](http://www.rdio.com/developers/docs/web-service/index/).
The candidate's challenge is to build something on top of that.
The challenge is purposefully vague in order to encourage creativity.

In my case I thought it would be neat to create some semblance of a mixing table for [Rdio](http://www.rdio.com/home/en-us/) streams.
I'm not a DJ or even really familiar with how mixing tables work.
But how hard could it be (Famous last words.)

## Challenges

Initially my plan was to just initialize two [Rdio API](http://www.rdio.com/developers/docs/web-playback/index/) streams.
However [Rdio](http://www.rdio.com/home/en-us/) actively prevents users from playing two simultaneous streams.
If you try it the oldest stream will be cut off.
This appears to affect a currently logged in user across multiple computers as well as a browser window sharing the same session.

To get around this I first tried using two iframes and the [sandbox attribute](http://www.w3schools.com/tags/att_iframe_sandbox.asp).
This unfortunately was also a non-starter.
While the [Rdio API](http://www.rdio.com/developers/docs/web-playback/index/) will stream within an iframe it will not stream within an iframe with any [sandbox options](http://www.w3schools.com/tags/att_iframe_sandbox.asp).

At this point I had to resort to separate browser windows.
It also meant this supposedly simple project of mine needed a communication mechanism between two browser windows.
Thankfully [socket.io](http://socket.io/) is available and with some headaches I had basic communication between the two windows.

## The Best Part

Probably the most straightforward feature was the spinning album art but it also happens to be my favorite.
Modern browsers contain all sorts of CSS transitions that web developers don't get to use because the support is lacking or implemented inconsistently.
Thankfully when you're making something for yourself or only a handful of others which you know are all using Chrome you get to experiment a little.

```CSS
.rotate {
  -webkit-animation:spin 4s linear infinite;
  -moz-animation:spin 4s linear infinite;
  animation:spin 4s linear infinite;
}

.paused {
  -webkit-animation-play-state:paused;
  -moz-animation-play-state:paused;
  animation-play-state:paused;
}
```

## Code & Link

You can see the code on my [github page](https://github.com/pcorliss) at [github.com/pcorliss/belly-rdio-dj](https://github.com/pcorliss/belly-rdio-dj).
The app itself is available on [Heroku](https://www.heroku.com/) at [belly-dj.herokuapp.com](http://belly-dj.herokuapp.com/)
