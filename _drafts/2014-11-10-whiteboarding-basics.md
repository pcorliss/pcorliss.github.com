---
layout: post
title: "Acing the Technical Interview"
description: ""
category: 
tags: []
comments: false
---
{% include JB/setup %}

... Intro ...

## Disclaimer

My POV is centered interviewing in the Chicago job market focused primarily around Ruby and Python shops.
Anecdotally this section of the Chicago market appears to focus more on practical skills and less on academic skills.
For example you're less likely to be asked to implement a sorting function. Your mileage may vary while interviewing but I've found the following to reflect reality pretty well.


## Scheduling Mechanics

Ideally you're reaching out to multiple companies as part of your job search. Scheduling is an absolute nightmare at this point as you go back and forth with a recruiting coordinator. A good rule of thumb is to offer up days/times where you're usually available, and 1-3 specific times. A good way to automate this is to use a tool like [YouCanBook.me](https://ga.youcanbook.me/) which allows others to see your availability directly.

## General Strategies

Communication
Whiteboard
Assumptions
I don't know vs. I'm not sure but if I had to guess
Don't wear a suit - ask the recruiter what appropriate dress is

## Soft Questions

These are my own personal nightmare. With experience I've gotten good at giving answers that people want to hear. Practice with a friend for optimal results. While answering these questions it's important to make these answers sound natural so try to put your own personal spin on it.

* Why did you leave your last job?
  This is likely not the real reason you left your last job. Instead it's something vague about a lack of challenges, opportunities for growth.
* Describe your hobbies.
  Recruiters are looking for two items here. A demonstration that you're not a robot and that you like to code outside of work. Ideally I'd omit things that reveal some protected statuses like children. State a few hobbies you enjoy, cooking, basketball, etc.. Then follow up with a coding side-project you're working on. It doesn't necessarily have to be a public project, or even have been started. Simply demonstrate passion for it.
* What drives you?
  The answer the interviewer is looking for is "Increasing shareholder value." But they don't actually want you to say that. Instead you should talk about how interested you are in improving the customer/coworker experience through performance/UI/feature improvements. Solving problems is also a good answer but be prepared to expand on how these things drive you.
* Why do you want to work here?
  This [onion article](http://www.theonion.com/articles/job-applicant-blows-away-interviewer-with-intimate,37296/) sums up nicely my feelings on this question. The purpose of this question appears to discern which candidates have done their homework on the company. My understanding is that this helps determine which candidate really wants the job. The mere presence of a candidate on a phone call or an interview is apparently enough. If asked this question regurgitate some company info and mention how you feel you could fit in.

## Note on Fairness

Before we dive in I want to speak a bit on the issue of fairness. Ideally all interviewers are professionals and interested in your success in the process as much as you are. This is not always the case. The interview process is weighted entirely on the side of the interviewer. Leaving the candidate with very little power in the equation. Even as a senior candidate in my last job search I had little power to dictate anything about the process. My best advice is to roll with it as best you can, keep your cool, and do the best you can.

### Examples
* A complete jerk
* Checking their email, texts, stepping out to take a call
* Hasn't read your resume
* Filling in last-minute for a sick interviewer
* Make you skip lunch
* Demand you code in a language unfamiliar to you
* Ask you questions they don't know the answer to

## Hard Questions

The bread and butter of the technical interview. I find these break up into a handful of separate types.

### Trivia

I don't ask these questions myself, as they often are a demonstration of specific knowledge as opposed to capacity to learn, problem solving, and aptitude. They also seem to disqualify candidates that know a concept but know it with a different vocabulary. Example: Big-O Notation versus Computational Complexity. But you will encounter them. I'm unaware of a way to prepare for these questions except by years of exposure to your language of choice as well as diverse language practitioners.

* What is [Hoisting](http://www.w3schools.com/js/js_hoisting.asp)?
* List the different ways ruby [looks up methods](https://practicingruby.com/articles/method-lookup-2)
* What's the Computational Complexity of [Merge Sort](http://bigocheatsheet.com/)

### Defending your choices

Essentially your comparing two things against each other. You might be asked to compare and contrast ruby and python. Or MySQL and PostgreSQL. Or just describe why some language or tool is your favorite. A bad answer would be "because that's the only thing I know". A good answer would be demonstrate a basic understanding of the pros/cons and features. The best preparation is years of use but failing that a good strategy for preparing is to go through your preferred toolkit (ruby, rails, postgres, ember, bootstrap) and look for criticism of each. The interviewer wants to see demonstrated passion and oppinions, but stop short of dogmatism preventing you from being flexible. There's nothing worse than spending 5 minutes telling the interviewer why XYZ sucks only to find out that their entire stack is written in it.

### Algorithms & Data Structures


  Modeling - OO/DB - BizRules
    SQL/ActiveRecord - Basics, Aggregators, Joins
    Scaling/Architecture - Bit.ly
  Pairing
  Katas
  Riddles
    Lateral Thinking
    Moving Mt Fuji
    Weighing Machines

  Your Own Questions
    Questions can make you stand out from other candidates
    Recruiter
      Benefits, Culture
    Technical
    Mgmt
  Other Resources
    http://www.restlessprogrammer.com/2013/09/hacking-coding-interview.html
    Cracking the Coding Interview
    Steve Yegge
    http://bigocheatsheet.com/
