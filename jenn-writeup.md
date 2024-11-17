# Automated Call Line Use-Case Proposal for ModivCare

ModivCare is looking to improve operational efficiency in the hiring process of caregivers, reduce churn during the hiring process, improve the experience of new hires during HR form completion, and reduce the time it takes to get hired.

The goal of this proposal is to build a pilot solution quickly without getting bogged down in technical integrations. This pilot will help establish and measure the success of an automated call line that can meet KPIs and address key pain points.

## Success Criteria

- An automated call line that can answer questions about the hiring process, provide guidance on HR form completion, I-9 forms and other documentation. Complex questions will be escalated and transferred to human agents with appropriate context
- Serve as the tier 1 automated call line for hiring-related questions
- Measure the following metrics:
    - Percentage of questions answered by the automated call line
    - Number of calls resolved by the AI call line vs escalated to human agents
    - Time reduction in the hiring process and form completion after roll-out
    - Percentage of hires completing the onboarding process after roll-out
    - Multi-lingual support capabilities

## Proposed Solution

- Set up a dedicated call number for automated inquiries to minimize telephony system integration time
- Train the call line on documents, training manuals, FAQs and other relevant materials provided by ModivCare. We'll start with a focused set of documents and iteratively expand training as we validate the model's performance
- Implement escalation capabilities to human agents with appropriate context when questions cannot be answered
- Provide clear metrics and reporting to measure success and impact:
    - Question intent and answer distribution
    - Common themes addressed by the call line
    - Help team track success metrics

**Technical Stack**:
- **Call Number**: Twilio with an AI agent
- **AI Model**: OpenAI on Azure or other open-source model
- **Document Understanding**: RAG and Hybrid Search
- **Reporting**: Any BI tool of team's preference

**Tech Stack Costs**:
- **Call Number**: Twilio with Bland or RetellAI: $3,000/month upfront
- **Call Per Minute**: $0.21/minute
- **Cloud Costs**: To be determined based on MVP requirements - deeper technical integration may be needed post-pilot. For now we will provide hosted solution and can work on BAA.

## What is Required from ModivCare Team

- High-quality training manuals, FAQs and relevant documentation
- Clear use-case descriptions
- Access to human agents who can help build and test the call line, provide feedback and support technical team iterations

## Timeline

Timeline largely depends on content access and subject matter expert availability from the ModivCare team. Rough timeline estimate:

- 1 week: Call number setup and automated call line configuration
- 3 weeks: Model training and collaboration with ModivCare team
- 1 week: Model iteration based on feedback
- 1 week: Production roll-out
