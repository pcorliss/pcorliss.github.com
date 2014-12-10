---
layout: post
title: "Recovering Git Commits"
description: ""
category: 
tags: []
comments: false
---
{% include JB/setup %}

### TLDR: Don't force push. But if you do you can get around the damage.

If you've ever accidentally force pushed something you understand the sinking feeling in your stomach as you desperately try and figure out how to recover from the error.
Often times it's possible to utilize the [reflog](http://git-scm.com/docs/git-reflog), find the local commit, and tag or reference it in someway to avoid garbage collection and losing the work forever.

In my case while doing some research for a project I noted that there was no way with a stock git client to recover from a force push if it no longer exists locally and isn't referenced on a remote.
In cases like the unfortunate [Jenkins incident](https://news.ycombinator.com/item?id=6713742) this sort of thing would require intervention by [GitHub](https://github.com/) Staff.

Curious I started looking for a way to do this manually via the git client, direct manipulation of git references, and finally hand-crafted calls over the wire.

## Setup

I started with an empty repository on [BitBucket](https://bitbucket.org/pcorliss/force-push-testing).
A few test commits were added, followed by a `git reset --hard HEAD~1`, another commit, and then a force push.
On both [GitHub](https://github.com/) and [Bitbucket](https://bitbucket.org) [the commit](https://bitbucket.org/pcorliss/force-push-testing/src/74b66b74321dd6e88a1fca05b728b39d0ec33ebc) will still be visible via the web GUI but because it's no longer referenced via the history of any tags or branches it's now completely inaccessible to other clients besides my own.
Even `git clone --mirror` ignores dangling commits.
Normally either you or someone in your organization would have the previous commit locally and could add a tag.
But if no one else is available and you don't have the commit locally you'll be out of luck.

## Git Wire Protocol

Git provides some nice debugging tools which allow you to take a peek at the various commands being sent over the wire. I use the following alias to turn them all on at once.

```
alias git_debug='export GIT_TRACE_PACKET=1 GIT_CURL_VERBOSE=1 GIT_TRANSPORT_HELPER_DEBUG=1 GIT_DEBUG_SEND_PACK=1 GIT_TRACE=1'
```

The output looks something like this:

```
pcorliss.github.com $ git fetch
trace: built-in: git 'fetch'
trace: run_command: 'ssh' 'git@github.com' 'git-upload-pack '\''pcorliss/pcorliss.github.com.git'\'''
packet:        fetch< 428b2a372495666ecde7f8c1557365a8e7c2ccd3 HEAD\0multi_ack thin-pack side-band side-band-64k ofs-delta shallow no-progress include-tag multi_ack_detailed symref=HEAD:refs/heads/master agent=git/2:2.1.3+github-642-g667ea60
packet:        fetch< 428b2a372495666ecde7f8c1557365a8e7c2ccd3 refs/heads/master
packet:        fetch< 0000
```

While this provided some nice clues on how git connects and sends commands it obfuscated important parts of the protocol including signatures and pack file generation and formatting.

## SSH Proxy

The only way to get around this was to build a proxy with which GIT would connect through and allow me to see and record the raw IO.
Git provides an environment variable `GIT_SSH` you can set which makes building a program to intercept the traffic a little bit easier.

After quite a bit of trial and error I built [git_ssh_proxy](https://github.com/pcorliss/git_ssh_proxy) to intercept and record the traffic coming from git.

A sample of the output recorded from `git push --tags`

```
CMD ssh -x git@bitbucket.org git-receive-pack 'pcorliss/force-push-testing.git'
STDOUT 008841abcee85021a3b08de5d73492ead4612afa4690 refs/heads/master^@ report-status delete-refs side-band-64k quiet ofs-delta agent=git/2.1.1
STDOUT 003d7953b561d6ebab069442e51440d3dc05a18ab20c refs/tags/fubar
STDOUT 003b501dd68b248d636c2a040949fe83c27119ce228c refs/tags/iii
STDOUT 0000 NOBREAK
STDIN 009e0000000000000000000000000000000000000000^@ 4b55fc9b074e6e34c1458e32ababba8d4565cafb refs/tags/dangling_commit_X report-status side-band-64k agent=git/2.0.00000 NOBREAK
STDIN PACK....RAW BYTES EXCLUDED FOR READABILITY..... NOBREAK
ERROR STDIN EOF:  String 0
STDOUT 003a^A000eunpack ok
STDOUT 0023ok refs/tags/dangling_commit_X
ERROR stdout EOF
ERROR stderr EOF
SYS pid 42668 exit 0
```

Initially I had tried to hand-craft the input but that proved difficult for two reasons.

1. Each line is preceded by the hex encoded length of the command
1. Push commands send up compressed binary data in [packfile format](https://www.kernel.org/pub/software/scm/git/docs/technical/pack-format.txt). Even empty pack data lines contain a signature with binary data.

Eventually using the SSH Proxy I recorded the sent data and was able to create new tags by just modifying the SHA line. As long as the SHA exists on the remote this command should work.

```
cat stdin.out | ssh -x git@github.com "git-receive-pack 'pcorliss/force_push_testing.git'"
```

## Tool For Tag Creation

Using the recorded data I created a second tool for the express purpose of generating the appropriate command and sending to the remote server.
It allows a user to automatically [create tags for dangling commits](https://github.com/pcorliss/dangling_commit).
I had a number of difficulties dealing with IO appropriately but after some tweaking it now works with both [Github](https://github.com/) and [Bitbucket](https://bitbucket.org) endpoints and should work with any git endpoint that uses SSH.

## GitHub API method
After I started writing this blog post I found this [alternate method](http://www.objectpartners.com/2014/02/11/recovering-a-commit-from-githubs-reflog/) which uses the [GitHub API](https://developer.github.com/v3/).
As far as I can tell there isn't a corollary on the [Bitbucket API](https://confluence.atlassian.com/display/BITBUCKET/Use+the+Bitbucket+REST+APIs).
