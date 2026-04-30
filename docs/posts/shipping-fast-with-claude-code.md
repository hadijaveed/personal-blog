---
authors:
  - hjaveed
hide:
  - toc
date: 2026-04-23
readtime: 5
slug: shipping-fast-with-claude-code
comments: true
---

# Claude Writes the Code. You Run the Loop.

I have been building a lot with Claude recently. Obviously you can ship all of the code very easily. But how do you plan new large scale features, how do you understand UX, brainstorm different kinds of UX patterns with Claude, and then ship across 3 repos in an established codebase, without breaking things.

Put in front of your customers the large feature you build, not in months but in weeks. Test your assumptions and iterate on top of it.

There is a lot of hype with multi agent workflows where there is an orchestrator agent that spawns off multiple child agents. Orchestrator checks with the child agents on the progress and figure out whats going on.

Works fine for code exploration, or when agent needs to build context, during implementations it usually does not work. Also you might have seen in Opus 4.7 Claude team does not spin up multiple agents. In fact things run in one thread in general and Claude Opus 4.7 has gotten really good in autonomously executing tasks

The SWE pattern in my mind holds here, decomposing larger problems into smaller sub-problems, and then combining sub-problems into a larger problems like dynamic programming...

![Breadth first: orchestrator forks across 3 repos](../assets/diagrams/01-breadth.png)

## Start the work with breadth-first approach

When starting a new feature, I always start with breadth first approach. e.g,

- ask agent to gather all the context through code exploration and PRD.
- create tasks and spend time planning as much as you could
- keep working on the planning phase... explore UX alternatives do competitve research

Once you have the solid plan and everything is working accordingly, time to go depth first approach.. Where think of orchestrator as a staff level software engineer who you will talk to, to checkin the work of the agents. how they are performing. whats working and whats not working. or where we need to go next

I have been working on a patient chat feature that spans across 3 repos. Involves creating a backend model to fetch data from multiple resources, requires an agent loop and orchestration, and overall a front-end experience. Looks easy but when you are dealing with so many data sources, thinking about auth patterns, protecting patient data security and other things it adds up. This is just one example.

Obviously the breadth first approach here is go build a system like this. Working with large code base that spans across 3 repos and 2 different languages... agent can get it done. But for you to be in the loop is so difficult even with all the planning the mistakes slowly compound and next thing you know you are running in an endless loop.

## Depth first approach when going deep on things

Now there is a specific UI or backend or a feature I need to build I will spawn off another agent a new claude code terminal instance here

```
claude --fork orchestrator-agent-id -n chat-agent
```

so this agent will inherit all the context from the orchestrator agent and either I will compact or start here depending on if summary is required. Yes Claude can do it too, but remember I need to go depth first here. I want to be in the loop. there are certain decisions Claude can get wrong that I need to fix. this is what I will do...

while Claude is cooking here, I may go to orchestrator to chat about something, get ahead of how I am thinking about the integration so I zoom out a bit

And then I will zoom in when I need to be in the loop. I will test the feature in detail like write test make sure the API, UX layer the data layer makes sense

![Depth first: zoom into one fork, you in the loop](../assets/diagrams/02-depth.png)

## Keep checking with the orchestrator

there are other UX research I will do

lot of people talk about spinning multiple sub-agents, but this does not work well. I like to keep the context clean and nice and easy to manage

usually in claude code I compact around 400,000 tokens thats my default setting, here is my env here

![Vet: zoom back to orchestrator, does the integration still hold](../assets/diagrams/03-vet.png)

## Keep the loop going

![Ship, listen with MCPs, re-prompt the orchestrator](../assets/diagrams/04-loop.png)

- you shipped the first version commit your .md plan and intent to your code repo.. yes ship it with the code
- write things like a PRD, what was the Problem, Solution and how you are gonna test your assumptions
- gather client feedback, logs or results you got e.g, Gmail MCP, Slack MCP, Linear MCP, Cloudwatch MCP, Sentry MCP,.. I use all of it to gather the full list. I use all of them
- ask the orchestrator to read the plan or /resume the session. Ask it where we left off.. whats going on where we are lacking etc...
- ask it to act like a staff engineer product manager, work on UX, work on a bug... make it easy for the users
- go talk to users. I use Granola MCP and record meetings with Granola. I spend time shadowing them while my granola is on. Ask them what like you'd change. why it is tough
- I make certain quick decisions using Claude Code here
- fine if I ship the wrong things, but having this quick iteration loop is so much important. My job is to craft a solution that solves end user problem. Code and everything is just means to an end which AI is automating. I am in the loop

Orchestrator is my Staff level engineer who is always with me. I am his manager. Sub-agents are my junior engineer but they are knowledgeable

also once a new feature is shipped I do /loop /schedule to keep checking logs. I have skills to look for client issues that comes up so orchestrator is up to date and knows

I use /remote-control with orchestrator to trigger it on mobile. I will obsess about the end UX and keep improving iteration

We are still very early in the process. Things change everyday, a lot of patterns here will hold some might not

Have fun building.

In case helpful here is my Claude Code config...

few important parameters to talk about

the adaptive thinking or 1M token have not been helpful. neither agent team features is not helpful for me.

```json
{
  "env": {
    "CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING": "1",
    "CLAUDE_CODE_AUTO_COMPACT_WINDOW": "400000",
    "DISABLE_ERROR_REPORTING": "1",
    "CLAUDE_CODE_DISABLE_FEEDBACK_SURVEY": "1"
  },
  "alwaysThinkingEnabled": true,
  "effortLevel": "xhigh",
  "autoMemoryEnabled": true,
  "showThinkingSummaries": true
}
```
