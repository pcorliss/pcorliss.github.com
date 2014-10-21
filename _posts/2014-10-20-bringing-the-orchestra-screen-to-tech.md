---
layout: post
title: "Bringing the Orchestra Screen to Tech"
description: ""
category: 
tags: []
comments: false
---
{% include JB/setup %}

### TLDR: [BadBias.herokuapp.com](http://badbias.herokuapp.com/)

The last chapter of Malcolm Gladwell's book
[Blink](http://www.amazon.com/gp/product/0316010669/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=0316010669&linkCode=as2&tag=blog50proje-20&linkId=23GUU7O2R3YT6Q4W)
introduced me to the concept of screens used for orchestra auditions.
For those that are unfamiliar: a screen is set up to hide the identity of the performer from those evaluating the candidate.

> Using data from actual auditions in an individual fixed-effects framework, we find that the screen increases by 51% the probability a woman will be advanced out of certain preliminary rounds. The screen also enhances, by severalfold, the likelihood a female contestant will be the winner in the final round.
>
> Claudia Goldin, Cecilia Rouse -
> <cite title='Orchestrating Impartiality: The Impact of "Blind" Auditions on Female Musicians'>
> [Orchestrating Impartiality: The Impact of "Blind" Auditions on Female Musicians](http://www.nber.org/papers/w5903)
> </cite>

These findings got me thinking about possible ways to apply this to the interview process for technology.
For many tech companies, the decision to hire candidates is based on their ability to write code to solve a series of problems, often evaluated via a combination of homework, a technical phone-screen, and in-person interviews.
During this process, the candidate's resume and code is reviewed by multiple people, and bias can arise from surprising sources.

> The results show significant discrimination against African-American names: White names receive 50 percent more callbacks for interviews.

> Marianne Bertrand, Sendhil Mullainathan -
> <cite title='Are Emily and Greg More Employable than Lakisha and Jamal? A Field Experiment on Labor Market Discrimination'>
> [Are Emily and Greg More Employable than Lakisha and Jamal? A Field Experiment on Labor Market Discrimination](http://www.nber.org/papers/w9873)
> </cite>

## A Simple Tool to Remove Bias

As a first step, I decided to build a [simple tool](http://badbias.herokuapp.com/) for blinding public [LinkedIn](https://www.linkedin.com) profiles by hiding data that could be used to infer the race, gender, or age of the candidate.
I included the option to hide company and educational institution names to avoid advancing candidates based on pedigree alone.

You can see an example of my [public profile](https://www.linkedin.com/in/philipcorliss) and the [blind version](http://badbias.herokuapp.com/linkedin/phil)

## Challenges

[LinkedIn](https://www.linkedin.com) has an [API](https://developer.linkedin.com/), but they [don't offer a user's public profile without that specific user logging in via oAuth](https://developer.linkedin.com/documents/profile-fields).
As a result, I had to go the screen-scraping route and process the contents using [Nokogiri](http://www.nokogiri.org/).
This leaves the project in an especially brittle state, where a small change on [LinkedIn](https://www.linkedin.com)'s side could mean that the content is rendered incorrectly or that it throws errors.

Public-profiles on [LinkedIn](https://www.linkedin.com) use two totally different templates.
Here's an example of [my profile](https://www.linkedin.com/in/philipcorliss) and a [former colleague's profile](https://www.linkedin.com/in/redsquirrel).
I'm unable to explain the reasoning for it, but parsing and replacing text within both profiles without completely breaking either required a lot of effort.

Certain portions of a resume &mdash; summaries, volunteer work, and awards &mdash; can provide identifying information about the candidate.
Some of it made sense to hide, i.e.
the user's co-workers and people in their network, but other information, like awards, seemed too important to omit.

The link you view when browsing [LinkedIn](https://www.linkedin.com) isn't the public profile of the user, and there isn't an API to convert it to a public profile either.
I'm guessing this will lead to a lot of head-scratching and a poor user-experience.

#### Valid Public Profile Links
* [/in/philipcorliss](https://www.linkedin.com/in/philipcorliss)
* /pub/philip-corliss/0/349/28

#### Non-Public Profile Links
* /profile/view?id=123456789&authType=name&authToken=xvZQ&trk=prof-sb-browse_map-name

[LinkedIn](https://www.linkedin.com) has a number of anti-screen-scraping protections in place.
As an example, this is what happens when you make a request with certain user-agents or from certain IPs.

```
$ curl -I 'https://www.linkedin.com/in/philipcorliss'
HTTP/1.1 999 Request denied
Date: Mon, 20 Oct 2014 22:00:20 GMT
Server: ATS
X-Li-Pop: PROD-ELA4
X-LI-UUID: 24URwzD6nhPwF54ilysAAA==
Content-Length: 511
Content-Type: text/html
```

## Next Steps

Next, I intend to integrate with GitHub to create a completely blind code review tool that companies can use to assign coding challenges to candidates.

## Code & Link

There's no code provided for this project as it's a mess of untested spaghetti mostly built as a proof of concept.
But you can visit and use the project freely at [BadBias.herokuapp.com](http://badbias.herokuapp.com/).
