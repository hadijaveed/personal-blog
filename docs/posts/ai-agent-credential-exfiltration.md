---
authors:
  - hjaveed
hide:
  - toc
date: 2026-04-11
readtime: 5
slug: ai-agent-credential-exfiltration
comments: true
---

# Your AI Coding Agent Can Exfiltrate Your Credentials. You Would Never Know.

I spent last night configuring Claude Code's security and realized something uncomfortable: for months, I had been running an LLM with unrestricted access to my terminal. It could read my SSH keys, browse my AWS credentials, curl data to any endpoint, and push code to production. I just never thought about it because the tool was helpful and nothing bad had happened yet.

That is exactly the kind of reasoning that gets production databases dropped.

<!-- more -->

[@noisyb0y1 put it well on X](https://x.com/noisyb0y1/status/2041947492065943810){:target="\_blank"}: by default, Claude Code can read your SSH keys, AWS credentials, all .env files, and push code wherever it wants. One prompt injection in a cloned repo and your data is already gone. Most of us just never configured the security settings that already exist in the tool.

The reality is that most AI coding agents today operate with far more access than they need. We would never give a new contractor SSH access to every server on day one, but we hand an LLM the equivalent without blinking. Claude Code at least gives you the tools to fix this. The problem is almost nobody uses them.

## How I Run Claude Code

I have two shell aliases in my `.zshrc` that I use daily:

```bash
alias cc="claude --permission-mode auto"
alias ccd="claude --dangerously-skip-permissions"
```

`cc` is my default. It runs Claude Code in auto mode, which means the agent executes commands without asking unless they hit a deny or ask rule. That is the balance I want for most work: fast iteration with guardrails.

Note: `--permission-mode auto` is currently only available on Team and Enterprise plans. If you are on an individual Max plan, you do not have access to this flag yet. You will need to rely on the default permission prompts or use `/permissions` inside a session to configure your rules.

`ccd` is the dangerous one. It skips all permission checks entirely. I use it when I am debugging something frustrating and I just want the agent to move fast. But every time I type `ccd`, I am trusting the model completely. No deny list, no ask prompts, no sandbox enforcement. Everything is allowed.

I want to be transparent about this because most people do not think about the distinction. The flag you pass at startup determines your entire security posture for that session.

## The Default Problem

Claude Code's most common permission mode is `auto`. In auto mode, the agent executes commands without asking you. That is great for productivity. The catch is that "auto" means everything that is not explicitly denied or in the "ask" list runs silently.

Let that sink in. If your deny list is empty and your defaultMode is auto, the agent can run `curl`, `ssh`, `nc`, `wget`, and any other command on your machine without you ever seeing a prompt. It can read your `.env` files, your `~/.aws/credentials`, your `~/.ssh/id_rsa`. Not because it is malicious, but because nothing told it not to.

This is not a Claude Code problem specifically. It is an industry-wide pattern. Every AI coding tool that executes shell commands has this same surface area. Claude Code just happens to be one of the few that gives you granular controls to lock it down.

## Three Layers of Security

Claude Code's security model has three distinct layers, and they work independently. Understanding how they compose is the key to getting this right.

### Layer 1: Permission Rules

The permission system evaluates in a strict order: deny first, then ask, then allow, then defaultMode. Deny always wins. If a command matches a deny rule, it is blocked regardless of what the allow list says.

Here is what my actual `settings.json` looks like:

```json
{
  "permissions": {
    "deny": [
      "Read(~/.ssh/**)",
      "Read(~/.aws/**)",
      "Read(~/.gnupg/**)",
      "Read(~/.azure/**)",
      "Read(~/.kube/**)",
      "Read(~/.npmrc)",
      "Read(~/.git-credentials)",
      "Read(~/.config/gh/**)",
      "Read(*.env)",
      "Read(.env.*)",
      "Bash(curl *)",
      "Bash(wget *)",
      "Bash(nc *)",
      "Bash(ssh *)",
      "Bash(tailscale *)"
    ],
    "ask": [
      "Bash(git push *)",
      "Bash(git commit *)",
      "Bash(git merge *)",
      "Bash(git rebase *)",
      "Bash(git reset *)",
      "Bash(git checkout *)"
    ],
    "allow": [
      "Bash(npm run *)",
      "Bash(git status *)",
      "Bash(git diff *)",
      "Bash(git log *)"
    ],
    "defaultMode": "acceptEdits"
  }
}
```

The deny list is your hard boundary. The ask list is your review checkpoint. The allow list is your fast lane. And defaultMode determines what happens to everything else.

I use `acceptEdits` as my default mode rather than full `auto`. This means the agent can read freely and suggest edits, but it asks before executing bash commands that do not match any rule. It is a middle ground between the speed of auto and the caution of asking for everything.

The mental model is simple: deny the dangerous stuff, ask before irreversible stuff, allow the routine stuff. Everything else falls through to your defaultMode.

### Layer 2: OS-Level Sandbox

This is where it gets interesting. The `/sandbox` command does not just add permission rules. It enables actual kernel-level isolation using macOS Seatbelt (or bubblewrap on Linux). Every subprocess spawned by Claude Code inherits these restrictions. A clever `npm postinstall` script cannot escape it. A malicious dependency cannot reach outside the sandbox walls.

The sandbox restricts two things: filesystem access (writes limited to your working directory by default) and network access (proxied through a controlled layer).

The catch is that `/sandbox` is session-only. You have to run it every time you start Claude Code. Unless you add this to your settings:

```json
{
  "sandbox": {
    "enabled": true,
    "filesystem": {
      "denyRead": ["./.env", "./.env.*"]
    }
  }
}
```

Now it persists across every session. No need to remember.

### Layer 3: MCP Server Controls

If you use MCP servers (Gmail, Slack, Linear, calendar integrations), there is a separate gate. Setting `enableAllProjectMcpServers: false` blocks any MCP server defined in a project's `.mcp.json` from loading automatically. This prevents a cloned repo from injecting a malicious MCP server into your session.

You can then whitelist specific servers you trust, or set it to true and rely on the permission prompts, since MCP tool calls still go through the ask flow unless you explicitly allow them.

## The Escape Hatch That Undermines Everything

Here is the part that made me rewrite this entire post.

Claude Code has a parameter called `dangerouslyDisableSandbox`. When a bash command fails due to sandbox restrictions, Claude is [instructed to retry the command with this flag set to true](https://github.com/anthropics/claude-code/issues/14268){:target="\_blank"}. The intent is reasonable: sometimes a legitimate build tool needs access outside the sandbox walls. The implementation is where it gets scary.

When `dangerouslyDisableSandbox: true` is set on a bash command, the OS-level sandbox is completely bypassed. No Seatbelt. No bubblewrap. The subprocess runs with your full user permissions. And here is the critical part that most people miss:

**Permission deny rules only protect Claude's built-in tools, not bash subprocesses.**

A `Read(~/.ssh/**)` deny rule blocks Claude's Read tool from opening your SSH keys. But it does not prevent `cat ~/.ssh/id_rsa` in a bash command. The sandbox was the thing actually enforcing that boundary at the OS level. When the sandbox is disabled, that protection vanishes.

This means the security model has a gap:

```
With sandbox:
  deny rule blocks Read tool -> SSH keys protected
  sandbox blocks bash subprocess -> cat ~/.ssh/id_rsa also blocked

Without sandbox (dangerouslyDisableSandbox: true):
  deny rule blocks Read tool -> SSH keys protected via Read
  nothing blocks bash subprocess -> cat ~/.ssh/id_rsa succeeds
```

The deny list gives you a false sense of security if the sandbox is not enforcing the same boundaries at the OS level.

### It Gets Worse

There are [documented cases](https://github.com/anthropics/claude-code/issues/34315){:target="\_blank"} where the sandbox bypass happens without any user prompt. When a bash command is auto-approved (either through your allow list or your defaultMode), Claude can set `dangerouslyDisableSandbox: true` and the command executes silently. The user never sees a prompt asking whether the sandbox should be disabled.

Claude Code also classifies certain commands like `cat`, `ls`, and `grep` as "read-only" and auto-approves them regardless of other settings. A prompt injection that tricks the model into running `cat ~/.aws/credentials` with `dangerouslyDisableSandbox: true` would succeed without any user intervention.

The attack chain is straightforward:

1. You clone a repo with a malicious README or code comment
2. Claude reads the file and interprets the injected instruction
3. The model runs a bash command to read your credentials
4. If the sandbox blocks it, the model retries with `dangerouslyDisableSandbox: true`
5. The command succeeds because bash subprocesses are not bound by permission deny rules
6. A second command exfiltrates the data via network (also unsandboxed)

### How to Close the Escape Hatch

Add this to your `settings.json` under the sandbox configuration:

```json
{
  "sandbox": {
    "enabled": true,
    "allowUnsandboxedCommands": false
  }
}
```

Setting `allowUnsandboxedCommands` to false completely disables the escape hatch. The `dangerouslyDisableSandbox` parameter is ignored. Every bash subprocess stays inside the sandbox, no exceptions.

The tradeoff is real. Some build tools, Docker commands, and system utilities will fail inside the sandbox. You will need to handle those manually or add specific filesystem paths to your sandbox allowlist. But you will not have an unmonitored backdoor in your security model.

## What to Deny

After going through this exercise, I landed on four categories that should always be in the deny list:

**Credential stores.** SSH keys, GPG keys, AWS credentials, Azure config, Kubernetes config, npmrc, git-credentials, GitHub CLI tokens. These are the crown jewels. No LLM needs to read them, ever.

**Environment files.** `.env` and `.env.*` patterns. I block these at both the permission layer and the sandbox filesystem layer. Double coverage is intentional. If one layer fails, the other catches it.

**Network escape tools.** `curl`, `wget`, `nc`, `ssh`. These are the exfiltration vectors. If a prompt injection or confused agent tries to phone home, these are the commands it would use. Blocking them in Bash does not affect WebFetch or WebSearch, which are separate tools with their own controls.

**Application-specific data.** In my case, Tailscale. I run a Tailscale network that connects my machines. The agent has no business reading Tailscale state, keys, or configuration. Think about what is specific to your setup: VPN configs, password manager data, macOS Keychain, iMessage history. If it is sensitive and the agent does not need it, deny it.

## What About the Ask List?

The ask list is for actions that are not dangerous on their own but deserve a human checkpoint. For me, that is:

Destructive git operations: push, commit, merge, rebase, reset, checkout. I want to see every commit message and review before anything touches the remote.

Write-oriented integrations: sending Slack messages, creating Linear issues, modifying calendar events. Reading is fine. Writing to systems other people see requires my approval.

## What You Actually Lose

Let me be honest about the tradeoffs.

With the deny list, you lose the ability to have the agent fetch URLs via curl. If you need it to download something, you do it yourself or use the WebFetch tool. You lose the ability to have it push code. You push manually. You lose the ability to have it SSH into servers. You SSH yourself.

With the sandbox, you lose unrestricted filesystem writes. If a build tool needs to write to `/tmp` or `~/.npm`, you need to allowlist those paths. Docker does not work inside the sandbox because it needs access to `/var/run/docker.sock`, which Seatbelt blocks. You can exclude docker commands from the sandbox specifically.

With `allowUnsandboxedCommands: false`, you lose the automatic retry when legitimate tools hit sandbox walls. You will need to run those commands yourself or temporarily adjust your sandbox config. This is the biggest friction point, and the one most people will push back on.

None of these losses have meaningfully slowed me down. The things I lost are things I should have been doing manually anyway. Pushing code, SSH access, downloading arbitrary files: these are all actions that deserve human review.

## The Uncomfortable Truth

We are in an awkward moment in AI tooling. The agents are capable enough to be genuinely useful but not trustworthy enough to be unsupervised. The tooling gives us security controls, but the defaults are optimized for onboarding friction, not for production safety.

The security model has a real gap. Your deny list protects against Claude's built-in tools, but bash subprocesses operate under a different enforcement mechanism. The sandbox is the only thing standing between a prompt injection and your credentials. And that sandbox has a flag that disables it, which the model can invoke on its own.

If you are running Claude Code, Cursor, Windsurf, or any AI agent that executes shell commands, you are running an automated system with access to your development environment. Treat it like what it is. Not an enemy, but also not a trusted colleague. More like a talented intern with a terminal: incredibly productive, occasionally surprising, and absolutely in need of guardrails.

The configuration takes thirty minutes. The alternative is hoping that nothing goes wrong, which is not a security strategy. It is a prayer.
