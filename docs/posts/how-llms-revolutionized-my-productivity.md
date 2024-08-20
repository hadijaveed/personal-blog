---
authors:
    - hjaveed

hide:
    - toc

date: 2024-08-11
readtime: 7
slug: how-llms-revolutionized-my-productivity
comments: true
---

# How LLMs Revolutionized My Productivity

In the ever-evolving landscape of LLMs, I've observed two distinct camps: the doomsayers who predict a dystopian future and the overly optimistic who claim AI has completely transformed their lives overnight. As for me? I find myself somewhere in the middle – cautiously optimistic about the technology's potential while actively seeking ways to harness it for practical, everyday use.

<img src="/assets/llm-productivity.png" alt="My desk setup in 2024" id="llm-productivity" style="display: block; margin-left: auto; margin-right: auto; width: 100%; height: 400px; object-fit: cover;">
<style>
@media (max-width: 767px) {
  #llm-productivity {
    height: auto !important;
  }
}
</style>

<!-- more -->

## Personal Perspective

Let's face it: as engineers, tech managers, and technical entrepreneurs, we often find ourselves bogged down in mundane, repetitive tasks. But now, with LLMs, we have the opportunity to offload these tasks. This shift allows us to free up our mental bandwidth, zoom out, and focus on the bigger picture.

For me, being an engineer isn't about hiding behind a screen, churning out code in isolation. It's about stepping out, collaborating, and leveraging every tool at our disposal – AI included – to create solutions that actually make a dent. Understanding the business needs, questioning why we're building something in the first place, and focusing on user-centric experiences are all part of our job. We need to work hand-in-hand with product and business teams, not in our own little bubble. What gets me fired up is how AI-powered automation of those tedious tasks gives me more headspace to see the big picture and contribute more meaningfully to the product's success.

Since Large Language Models (LLMs) hit the scene, my productivity and problem-solving approach have taken a serious leap. Here's how AI has changed my workflow and allowed me to zoom out on the bigger picture:

### Automating and Streamlining Engineering Tasks

LLMs have become my go-to tool for handling both monotonous tasks that once consumed hours of my day:

- **JSON Data Wrangling**: Most of the engineering tasks involve parsing JSON data, reading API docs, or understanding interfaces to consume. I now use LLMs to write Python/TypeScript code for these tasks, significantly speeding up the process of integration.

- **Database Schema Design**: Once I understand the business problem, I use AI to design SQL tables or NoSQL collections. By providing the current model layout and structure, AI can reason through the current state and suggest changes. This allows me to spend more time understanding business objects required, and what I'm trying to solve, while AI automates the table/collection creation process.

- **REST API Development**: Let's be honest, creating basic APIs can sometimes feel like a task a well-trained monkey could do. Now, I use LLMs to write controllers, define REST endpoints, and create service classes. This shift allows me to focus more on defining the spec and questioning why I need an endpoint in the first place, rather than getting bogged down in repetitive code.

- **Documentation**: Documentation was always an area where I struggled, as it often felt like a task easy to procrastinate on. With AI, I can now provide my schema definitions, API designs, and code running instructions, and it can automate much of the documentation process. Creating clear, comprehensive documentation for projects is now a collaborative effort with AI. I also use it to document infrastructure and security policies when I'm involved in documenting security architecture.

- **Debugging**: A lot of time is often consumed by environment issues. While AI/LLMs aren't yet fully aware of specific environments (though this is changing with tools like [Cursor](https://www.cursor.com/){:target="_blank"}, [GitHub Copilot Workspace](https://githubnext.com/projects/copilot-workspace){:target="_blank"}, and [Gemini](https://cloud.google.com/products/gemini){:target="_blank"}), I can now provide error codes and stack traces to the model. It then suggests next steps and potential fixes, streamlining the debugging process. By describing an error or unexpected behavior, I often receive insightful suggestions for potential fixes or areas to investigate.

- **Project Bootstrapping**: Starting a project from scratch often involves dealing with boilerplate code and repetitive setup tasks. Whether it's setting up a REST API, initializing a React/Next.js project, or writing basic components, LLMs can generate the foundational code structure. This allows me to focus on the unique aspects of the project rather than getting bogged down in setup details.

> It's worth noting that by no means are LLMs perfect at these tasks. But with the right question or prompt, they do a pretty good job for me. Often, asking the right question is harder than finding the answer or solution. This is where spending more time is usually better, regardless of the approach.
> 
> Your workflow might differ in a larger enterprise, but I think bigger companies are already moving in this direction with local models and such.

> It's also important to note that the tasks I've mentioned primarily involve automating routine, repetitive work. AI hasn't replaced the need for thoughtful research, architecting complex systems, or writing intricate, business-critical code. These higher-level tasks still require human expertise and creativity.

## Tools I Use Daily

Here's a rundown of the AI-powered tools that have become indispensable in my workflow:

#### Cursor
[Cursor](https://www.cursor.com/){:target="_blank"}, paired with [Claude Sonnet 3.5](https://www.anthropic.com/news/claude-3-5-sonnet){:target="_blank"} or [GPT-4o](https://openai.com/index/hello-gpt-4o/){:target="_blank"}, is my go-to for coding tasks. As a former [VSCode](https://code.visualstudio.com/){:target="_blank"} user, I appreciate Cursor's familiar yet enhanced IDE experience:

- The Command + K shortcut is far more useful than auto-complete or GitHub Copilot's sometimes intrusive suggestions.
- Contextual prompts using **@file**, **@folder**, and **@codebase** shortcuts are incredibly intuitive.
- While the web-search feature needs improvement, I'm optimistic about its potential.
- For new projects, I've transitioned from gpt-engineer to Composer, though the file modification UX still has room for growth.

I spend a significant portion of my time crafting detailed specs in Markdown. This not only creates solid documentation but also helps me formulate better prompts for AI assistance. The **@shortcuts** for referencing are particularly helpful here.

A lot of my focus goes into creating robust data models (e.g., SQLAlchemy models, TypeScript interfaces, Pydantic or Prisma schemas). Well-defined data objects are crucial for maintaining code health and hygiene.

#### Warp Terminal
After years of using [iTerm2](https://iterm2.com/){:target="_blank"}, I've switched to [Warp Terminal](https://www.warp.dev/){:target="_blank"}. Its speed (thanks to being written in Rust) and features like Command + I for quick AI question and environment queries have won me over.

#### Web-based AI Tools
Needles to say, I regularly use GPT, Claude's console, and Perplexity for web searches and more complex QnA.

## Areas Where I'd Like to See AI Improve

While AI has significantly boosted my productivity, there are still areas where I believe AI-powered tools have room for improvement. Here are some domains where I'm eagerly anticipating advancements:

- **UX Design:** As engineers, we often lack good instincts about user experience. I'm constantly looking for better ways to translate requirements into rough mockups, but haven't found the perfect AI tool for this yet. [Figjam](https://www.figma.com/figjam/ai/){:target="_blank"} is trying to get there, but I did not have too much success with it

- **Legacy Code Translation:** Dealing with large, legacy codebases remains a challenge. While this could be a standalone product, I'm hoping future models like Gemini will have enough context to reason through complex systems. The main hurdle seems to be creating a user-friendly interface for interacting with extensive file systems.

- **Complex SQL Queries:** AI still struggles with intricate SQL models and data warehouses involving numerous objects and relationships. This likely stems from the contextual knowledge required, and it's unclear when AI will be able to fully tackle this complexity.

- **Cloud Infrastructure:** While tools like AWS, GCP, and Azure are making strides with AI integration (e.g., StarAgent and Gemini), we're not yet at a point where AI can independently create infrastructure, set up alerts, and debug cloud environments. The main limitations are lack of context and incomplete tooling.

- **Improving Soft Skills in an Async World**: This might be very aspirational, I'm curious about how AI could enhance soft skills by analyzing communication patterns, suggesting improvements in correspondence, and providing real-time feedback during virtual meetings. While AI could potentially assist with understanding meeting context, streamlining documentation, and generating talking points, it's crucial to remember that genuine human connection and empathy remain irreplaceable in developing strong professional relationships.


## Zooming Out: The Bigger Picture

With LLMs and a curious mindset, I've been able to accomplish more. I believe you can too. In my humble opinion, our day-to-day workflows as engineers need to evolve. We need to work more effectively, though what that means may differ between large tech companies and startups/scale-ups. While I may not be best suited to advise someone working in a larger company, if you're a builder creating products, you might relate to my experience.

Here's how I see the role of engineers expanding:

- **Become a Product Engineer**: Interface with both business and technical teams, write code faster, and produce documentation quickly. Lead or be an influential individual contributor

- **Dive Deeper into Business Processes**: Learn the crux of how businesses operate. Leverage your technical vision and AI to iterate on products rapidly and complement business needs

- **Connect Directly with Customers**: Spend more time understanding customer needs. Don't solely rely on product managers to translate requirements; be the front-facing person yourself, you will build better

- **Embrace Growth Engineering**: This might be aspirational, but it's something I'm working towards. Understand the growth funnel and see how you can leverage AI tooling and your technical expertise to drive growth towards the product

Much of what I've mentioned above, points towards companies doing more with smaller teams. But isn't that the current trend? Instead of complaining or lagging behind, get ahead of the game. Use these tools to your advantage, rather than worrying about how they might replace you.

Remember, these are just my personal opinions based on how I've used AI to my advantage. The key is to find what works best for you and your team.