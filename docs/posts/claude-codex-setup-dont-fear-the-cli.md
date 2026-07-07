---
authors:
  - hjaveed
hide:
  - toc
date: 2026-06-23
readtime: 6
slug: claude-codex-setup-dont-fear-the-cli
comments: true
---

# Your Claude + Codex Setup, and Why You Shouldn't Fear the CLI

This is the first episode of Build with Agents, where I record my coding agent setup, the ergonomics and developer tools I have wired up locally to stay productive. I will keep these short and ship them often, because my setup keeps changing and I would rather share what I have now than wait for it to be perfect.

<video autoplay muted loop playsinline controls style="width: 100%; max-width: 100%; border-radius: 8px; margin: 1.5rem 0;">
  <source src="REPLACE_WITH_GITHUB_ASSET_URL" type="video/mp4">
  Your browser does not support the video tag.
</video>

<!-- more -->

## Why the CLI, and why you shouldn't fear it

I am a CLI-first user. Not to look cool, but because I genuinely think the terminal is the best surface for this kind of work. Coding agents are fundamentally simple: a loop inside a harness, a long-running prompt with a bunch of tools. They do not need to be complicated.

The real reason is that I keep flip-flopping between Claude Code, Codex, and even [opencode](https://opencode.ai/){:target="\_blank"} with the GLM model, because not everything needs Claude-level intelligence. The question becomes: what is the one common surface where I can trigger all of these? VS Code is one option. But the terminal, split into a few panes, is better. These days you are not writing much code by hand. Your job is to generate it and review it as fast as you can, and the CLI is where that workflow lives.

## Recommended terminal: Ghostty

If you are on Mac or Linux, download [Ghostty](https://ghostty.org/){:target="\_blank"}. It is a GPU-accelerated terminal emulator that renders beautifully and has great defaults out of the box. On Windows it is not available yet. Please do not use the default macOS Terminal, it is not great.

If you want alternatives that also support GPU rendering, look at [Alacritty](https://alacritty.org/){:target="\_blank"} or [WezTerm](https://wezterm.org/){:target="\_blank"}.

A few Ghostty commands worth memorizing:

- `cmd+d` to split right
- `cmd+t` to create a new tab
- `cmd+shift+enter` to zoom the current split to fullscreen (hit it again to come back)
- `cmd+shift+p` to open the command palette, then type `split`, `tab`, or `rename` to find everything else

I usually run three splits so I can drive agents in parallel: one Claude Code instance, one Codex, and a pane for reviewing code.

## Shell aliases for your agents

Spin up agents faster with a few aliases. Depending on your shell, add these to `~/.zshrc`, `~/.bashrc`, or your profile:

```bash
alias cc="claude --permission-mode auto" # Claude Code in auto mode
alias co="codex"                         # Codex
alias cca="claude agents"                # the parallel Claude Agents UI
```

Notice that `cc` always spins up in auto mode. Clicking approve on every single command is what kills your flow, so I let the agent run on its own. The reason I am comfortable with it is the sandbox in my settings.json (next section): it blocks agents from reading secrets and limits what they can touch, so auto permissions become a productivity win instead of a footgun. Auto mode plus a sandbox, never auto mode alone.

## Running agents in parallel, and from your phone

The `cca` UI (Claude Agents) is where most of my knowledge work happens: reading email, scanning Slack, planning features, running my personal finance and task loops. It lets you run multiple threads in parallel over a directory, pin the ones you care about, and background the rest. Hit `?` inside it for the full list of keyboard shortcuts, and `ctrl+s` to cycle between the session view, the directory view, and the needs-input view.

A few habits that make this work:

- Name your sessions. Use the rename command and give each one a clear label like `build-with-agents` or `backend-implementation`. Names persist locally, so you can recognize them both here and on your phone.
- Branch instead of starting cold. Run a long-lived orchestration thread where you plan, then `/branch` from it into a focused session. The handoff is natural because all the planning context comes along. It is breadth-first when you start a feature, then depth-first once you go heads-down on one piece. Use `/resume` to find a session by name.
- Loop the recurring stuff. `/loop` runs a session on a schedule, so my daily task review and email reader just fire every day at 5 without me touching them.
- Background with `/bg` to move a thread out of the way while it keeps working.

Turn on remote control and every session shows up on your phone and the web. I never expected to be planning and steering work from my phone against my always-on Mac mini, but it is genuinely useful. You can set it once in your settings.json so you do not have to enable it per session.

## A secure Claude settings.json

This one matters. You do not want Claude going rogue, reading your `.env` files, and exfiltrating secrets. I wrote a separate post on why that is dangerous and how it can be exploited, so a setup that gives you peace of mind is worth it. The key piece is the sandbox setting.

You can grab mine here and adapt it:

[github.com/hadijaveed/build-with-agents/config/claude/settings.json](https://github.com/hadijaveed/build-with-agents/blob/main/config/claude/settings.json){:target="\_blank"}

A few of the defaults in there:

- A sandbox so agents cannot read sensitive files
- Default effort level and remote control enabled for every session
- Error reporting to Sentry turned off
- Auto-compact at a sane token size, because the one-million-context window never worked well for me
- Voice input enabled (I use Wispr Flow, but long-pressing space in Claude works well too)

## Code review tools: LazyGit, hunk, and lumen

Since you are not typing most of the code, reviewing fast is the whole game. I will do a proper deep dive on review workflow in a later episode, but set these up now.

[LazyGit](https://github.com/jesseduffield/lazygit){:target="\_blank"} is an excellent terminal UI for git and the hub I review from. Then two tools that plug into it:

- [hunk](https://github.com/modem-dev/hunk){:target="\_blank"}, a review-first terminal diff viewer built for agent-authored changes. Install with `npm i -g hunkdiff`.
- [lumen](https://github.com/jnsahaj/lumen){:target="\_blank"} for great diff summaries. Install with `brew install lumen`.

My LazyGit config, including the custom keybindings below, is here:

[github.com/hadijaveed/build-with-agents/config/lazygit.yml](https://github.com/hadijaveed/build-with-agents/blob/main/config/lazygit.yml){:target="\_blank"}

With that config, inside LazyGit:

- Press `shift+D` on any file to open it in the hunk diff view
- Press `shift+L` to see it in the lumen view

Both serve their own purpose, one for line-level review, one for a higher-level summary.

## Next up

Effective ways to review code when you can no longer read every line, plus more of the CLI primitives I lean on. See you in the next one.
