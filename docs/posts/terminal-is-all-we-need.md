---
authors:
  - hjaveed
hide:
  - toc
date: 2025-08-04
readtime: 5
slug: terminal-is-all-we-need
comments: true
---

# How Claude Code Made Me Fall in Love with the Terminal 

Like many of you, I recently made the full switch from Cursor to [Claude Code](https://docs.anthropic.com/en/docs/claude-code). This transition marked more than just a tool change – it fundamentally transformed how I think about development environments.

For years, I lived in VSCode, relying heavily on mouse navigation and minimal keyboard shortcuts. I resisted the pull of Neovim and keyboard-centric workflows. But after embracing Claude Code, I discovered something profound: **the terminal is the new IDE**. You can run it everywhere with a consistent workflow – be it a Linux box, your Mac, or a VPS. That's all you need.

<!-- more -->

## The Terminal Renaissance

Post-Claude Code adoption, I discovered something profound. The terminal isn't just a command line anymore – it's become a powerful orchestration layer for AI-driven development. The ability to customize, control, and context-switch using nothing but keyboard commands feels like rediscovering the original Unix philosophy, but supercharged for the AI era.

As a recent article on [Coding for the Future Agentic World](https://addyo.substack.com/p/coding-for-the-future-agentic-world) put it:

> "The terminal is the new IDE - CLI agents turn your shell into an action‑oriented interface where prompts translate into multi‑file commits and tests"

This perfectly captures what I've been experiencing. The power of being in the terminal, switching contexts, and conducting multiple AI agents while navigating entirely via keyboard has transformed my productivity in ways I didn't expect.

## Why Terminal Workflows Matter Now

The shift to terminal-based development isn't just about nostalgia or hacker aesthetics. It's about finding the right interface for AI-augmented coding. Here's what I've discovered:

### Speed vs. Control

I was using Cursor's AI agents, and while the review UX was impressive, it was *too fast*. Yes, you read that right – too fast. When working on established codebases, I want to be in the loop, reviewing work as it happens. Being able to control the pace of AI assistance is crucial.

With Cursor agents, you can spawn multiple agents, but the context switching felt disconnected. It never matched the fluid experience of working in a [tmux](https://github.com/tmux/tmux) or [Zellij](https://zellij.dev/) window where you can see your AI "cooking" the code in real-time.

### The Context Problem

`.cursorrules` never quite worked for me. In contrast, Claude Code's slash commands – essentially fancy prompts – have made me incredibly productive. The direct, explicit nature of terminal commands aligns perfectly with how I think about giving instructions to AI.

### Productive Impatience

AI processing creates natural pauses in your workflow. Rather than sitting idle while Claude Code crunches through a complex task, I've learned to use these moments productively. I'll switch to another pane and start:
- Writing test cases I want to validate
- Drafting the next specification
- Setting up another AI agent for a parallel task

The terminal makes this context switching seamless. Before AI completes one task, I'm already thinking three steps ahead, preparing context for the next interaction.

## My Terminal-First Toolkit

Here's the stack that has revolutionized my development experience:

### [Neovim](https://neovim.io/) with [LazyVim](https://www.lazyvim.org/)

The transition from VSCode to Neovim was brutal for 3-4 days. But after pushing through the initial pain, I'm now far more effective. Navigating entirely via keyboard, reviewing code, and writing has become genuinely enjoyable.

I use LazyVim and keep my configuration on [GitHub](https://github.com) for consistent experiences across servers and machines. The investment in learning vim motions has paid off exponentially.

### [Zellij](https://zellij.dev/) for Session Management

Zellij is modern tmux – and it's delightful to work with. I've aliased it to `zz` for quick access:

```bash
alias zz="zellij"
```

Starting a new session is as simple as `zz a backend-work`. The keybindings are intuitive:
- `Ctrl + p` to create new panes
- `Ctrl + t` for tabs
- Arrow keys for navigation
- Built-in resizing and moving

When AI is processing in one pane, I can seamlessly switch to another. Each pane becomes like having a dedicated AI co-programmer working on a specific task. My role shifts to reviewing code, anticipating edge cases, and improving specifications.

### [GitHub Copilot](https://github.com/features/copilot) for Autocompletion

While Cursor's completion model is excellent, GitHub Copilot in Neovim holds its own. It's not quite as sophisticated, but it's more than adequate for day-to-day coding.

### [Avante.nvim](https://github.com/yetone/avante.nvim) for Inline Editing

I missed Cursor's `Cmd + K` experience for quick edits. Avante.nvim fills this gap. It's not perfect, but with proper keybindings, I rarely need it – Claude Code handles the heavy lifting.

### [Ghostty](https://ghostty.org/) Terminal

This beautiful terminal won me over with its simplicity and speed. It's the perfect foundation for this entire workflow.

### [Claude Code Router](https://github.com/musistudio/claude-code-router)

Recently started using this to experiment with different models like Kimi for faster responses. If you haven't tried model routing, I highly recommend it – being able to switch between models based on task complexity is game-changing.

### Additional Power Tools

- [lazygit](https://github.com/jesseduffield/lazygit) - Git management without leaving the terminal
- [lazydocker](https://github.com/jesseduffield/lazydocker) - Docker container management made simple
- [Rainfrog](https://github.com/achristmascarl/rainfrog) - SQL database management in the terminal
- Docker Compose - Let Claude Code work with compose files to spin up dependencies and integrate multiple codebases

## The Slash Command Revolution

One of Claude Code's killer features is its slash commands. I've built up a library of custom commands that act as sophisticated prompts. These aren't just shortcuts – they're carefully crafted instructions that ensure consistent, high-quality AI assistance.

With hooks, I can trigger linting and type checking automatically. The terminal becomes a highly customized environment where AI and traditional tools work in perfect harmony.

## Final Thoughts: Was It Worth It?

Absolutely. 

The initial learning curve for Neovim was steep, but living entirely in the terminal has reignited my joy in programming. Zellij's session management enables laser-focused work – each session becomes a dedicated workspace for deep concentration.

The ability to conduct multiple AI agents simultaneously, review their work in real-time, and maintain complete keyboard control has made me significantly more productive. More importantly, it's made programming fun again.

As AI continues to evolve, I believe terminal-based workflows will become increasingly important. The terminal provides the perfect balance of power, flexibility, and control for orchestrating AI agents. It's not about going backwards – it's about finding the right interface for the future of development.

Whether you're writing code, searching files, or editing documentation, tools like Claude Code are transforming the humble terminal into a powerful AI-augmented development environment. 

The terminal isn't just alive – it's thriving. And for developers willing to invest in mastering it, the rewards are substantial.
