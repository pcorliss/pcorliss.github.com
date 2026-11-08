---
layout: post
title: "A Local LLM Beats Facebook but not the Kobayashi Maru"
description: ""
category: Technical
tags: [TODO]
---
{% include JB/setup %}

The story starts last year. I wanted to explore building a personal assistant. I had been experimenting with the LLama models and thought that with the right hardware I might be able to get a basic persoanl assistant running. At the time this turned out to be wildly ambitious. The models I could run on the Nvidia 5060 Ti card I purchased weren't able to follow instructions or respond fast enough to be usable, even as a basic coding assistant. I ended up using the machine to stream Satisfactory to my Steam Deck more than anything else.

Fast-forward to October of 2026 and I start hearing interesting things about [Strata](https://github.com/niko1221/strata). Within about an hour I had `qwen3.8-flash-next-iq3_s` running at about 50 tokens/s. I connected up [pi](TODO link to Pi) and had it build [a snake game](TODO link to snake game in GitHub). Without any extra prompting it had a working first pass, a second passed fixed the music and sound effects. A very impressive first start.

![Strata](/images/Strata.png)

![Snake game title](/images/SnakeGame2.png)
![Snake game demo](/images/SnakeGame1.png)

## Kobayashi Maru

I took a look through my `~/git` directory for half-finished projects and found the archive of the [Kobayashi Maru Game]() I pulled from the [Wayback Machine](). Back in 2021 I had played this online web based game, figured out the path to beat it, and won a lifetime subscription to [Paramount+](). The Facebook integration broke after about a year, and the DNS stopped resolving around 2025. I made a half-hearted attempt to get the archive and remove the Facebook integration, but the obfuscated JS was too much for me to overcome.

Reading about others successfully using LLMs to port/emultate games made me think this would be a good opportunity to see how far I could get. With a single prompt we were off, after a short period of time it had deobfuscated the JS, analyzed it, and written some scripts to rewrite the links and build an offline version. With some more time it had built a shim for Facebook login. It also decided that there were bugs in various places and it would helpfully "fix" them by adding additional shims. At this point it needed to be paused as it started winding down unasked for features.

With a little direction and I had it on Github, [github.com/pcorliss/kobayashi_maru](https://github.com/pcorliss/kobayashi_maru), and hosted on GitHub Pages, [blog.50projects.com/kobayashi_maru/](https://blog.50projects.com/kobayashi_maru/).

Total time was about 2-3 hours, of which most was spent unmonitored.

## Where it failed

The LLM/harness got hyper-fixated on building a full headless Chrome based testing framework. It tried to fix the failure counter that it classified as a bug in the original game. Which turned out to be a bad interpretatin of the code.

I hadn't played it in 5 years so only had vague memories of some of the tricks to beating it. The game had initially been marketed as "impossible" and the designers had injected lots of blind paths and requirements to get to the good ending. So I asked it to analyze the code and determine the path necessary to reach the end. After several hours it had written a script and was trying to brute force the game by following every story path. I found my old notes from when I played it before and gave it the path I had followed but it still couldn't figure it out.

It would be an interesting experiment to see if a state of the art model from Anthropic or OpenAI would have better success. But for the moment I'm enjoying my John Henry moment where I'm still better at some things than the machine. Even if it is just playing a video game.

![Kobayashi Maru Success](/images/KobayashiMaruWin.png)

## Takeaways

- This is the most impressed I've been so far with Local LLMs. With just 16GB of VRAM, 64 GB of RAM, and fast disk I was able to run a full fledged harness with thinking support.
- In my day-job I work as a Platform Engineer at a trading company TODO insert linkedin link. I make use Claude Opus 5.5 heavily. It was interesting to step back to a weaker model. It makes me appreciate what the paid models offer and what I can get with local hardware.
- This local model doesn't compare to Opus 5.5, but it's better than what I was using a year ago and I'm hopeful that the Local LLM models continue to track less than a year behind the best in class available paid models.

## My LLM Machine Specs

- CPU: AMD Ryzen 5 9600X
- RAM: 64GB DDR 5
- GPU: Nvidia RTX 5060 Ti 16GB
- Drive: 1TB NVMe
- Model: `qwen3.8-flash-next-iq3_s`