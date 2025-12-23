---
authors:
  - hjaveed
hide:
  - toc
date: 2025-12-24
readtime: 4
slug: product-and-engineering-principles
comments: true
---

# Blueprint and Engineering Principles

These are the principles we follow at [RevelAI Health](https://www.revelaihealth.com/){:target="\_blank"}. They've shaped how we build and ship. Might be useful for other early to late stage startups too.

<!-- more -->

## Ownership and agency

When you build something, own it end to end. Relying on QA or other team members? Those days are gone.

AI has helped save us time writing code. But shipping to production still takes longer than you'd expect. The bottleneck isn't coding anymore. It's everything else.

- When you code something, test it yourself
- If you have a dependency on others (a vendor, internal team member, anyone), own the communication
- Do a follow-through in production. See how it's behaving
- You can't throw features over the wall

## Developing product taste

Product taste is a term used by many leaders. [Sarah Guo wrote a great piece on it](https://www.linkedin.com/pulse/taste-sarah-guo-u9qcf/){:target="\_blank"}. Taste is a coherent philosophy encoded in thousands of aligned decisions.

The engineering role has evolved beyond hiding behind your screen and getting work done. Understanding product from first principles, sitting in user shoes, and raising the bar on product UX. This matters now.

Get in front of customers. Learn from their pain points. The best engineers I've worked with have strong product opinions.

## Shipping fast

We always encourage shipping fast. Not the old "move fast and break things." That doesn't work with AI in the loop.

The only way to know if something works at a startup is by shipping. Put features in front of customers. Get feedback. Iterate. Repeat.

Velocity matters. Perfection doesn't.

## Good async comms

Writing gives you clarity. When you write down your thoughts, you think about edge cases. You give clarity of thought to yourself and others.

Communicating clear PRDs beats hopping on really long calls. You can reference it later. Others can digest it on their own time.

We encourage everyone to default to async.

## Know when to break from async

Too much back and forth on Slack can drag. If something is taking more than 5 to 10 messages to resolve, just jump on a huddle.

Get it resolved quickly. It's much better to do 10 minutes synchronously than write long essays of messages over 2 days.

Async is the default. But know when to break from it.

## Use your product as a user

Many engineers don't use their own product. If you're building in healthcare, you're not a nurse or doc. If you're building in fintech, you might not be doing investments.

But you can pretend to be a user. Use it daily. You learn a ton using your own product.

As engineers, we're busy shipping. But using what we build is how you develop intuition for what's broken.

## The real reward is adoption

I've seen teams celebrate GitHub pull requests. Teams celebrating "we shipped feature X."

The real reward is feature adoption. Anything you've built that's not getting adopted by customers? Something is wrong. Not just you, the whole product is doing something wrong.

PRs merged and features shipped feel good. But they're not the goal. Customer adoption is.

## No one is coming to clear your tech debt

You're never going to get dedicated time to clear tech debt. It's hard to convince everyone, make a plan, and get it done.

Don't wait for someone to tell you. Find ways to clean it up incrementally. Get buy-in from the team as you go.

If you wait for permission, you'll wait forever.
