---
authors:
    - hjaveed
hide:
    - toc
date: 2022-10-04
readtime: 4
slug: using-nudges-to-reinforce-health-behaviors
---

# Using Nudges to Reinforce Healthy Behaviors

[Guest Post on Twilio Blog](https://customers.twilio.com/en-us/vincere-health){:target="_blank"} on how we Vincere used Twilio to Reinforce Healthy Habits That Improve the Lives of Underserved Populations

<!-- more -->
Vincere Health believes clinicians play an integral role in promoting sustainable behavior change and that technology facilitates and personalizes this relationship at scale. Vincere Health is one of few health technology platforms built for people in diverse socio-economic categories.

## The Journey

Smoking is the leading cause of preventable disease, disability, and death in the United States. The recent pandemic made matters worse where cigarette sales increased in 2020 for the first time in over 20 years. There are over 34 million adult smokers in the U.S., many of whom are in the lower income population. Reaching this population and providing effective support at scale while keeping costs down can best be achieved with the aid of technology and a carefully designed patient experience.

Vincere Health built a platform to offer low-cost access to addiction healthcare with an option for using reward-based habit training to increase care compliance. While providing addiction healthcare, this platform also solves problems related to patient engagement, patient outreach at scale, and clinician productivity by automating administrative tasks and decreasing their cognitive burden.

## Building a Platform for a Personalized Care Journey
Smoking cessation is best represented as a journey, not a single event. Personalized care experiences tailored to each participant's needs have shown increased rates of success in conquering addiction while increasing care compliance and quit rates.

Vincere Health realized early on in their journey that creating a platform that allows care team members to build care pathways themselves, instead of hard-coding a program and spending subsequent product and engineering time to tweak it, is the key to creating truly differentiated and personalized experiences. Most of the existing workflow automation no-code tools are not particularly user-friendly or built to solve similar use cases. By building a platform that enables drag and drop care pathways, Vincere Health can empower clinical teams to truly have autonomy, agility to experiment, and flexibility to personalize programs for diverse demographics.

Vincere Health built a nudge engine that allows care teams to create personalized journeys in the following ways:

– Create a care journey for multiple days or months that can track a variety of events on a calendar using their Campaign Studio UI. A campaign includes customized messaging, remote patient monitoring (RPM), and assessments / surveys.

– Define personalized nudges and tasks. Vincere Health uses Twilio's Programmable Messaging API to power automated SMS messages at specific intervals serving relevant educational content, motivational nudges, behavior enforcement, and medication or appointment reminders for care coordination. When patients respond, Vincere Health integrates the Conversations API with their chatbot so the patient, clinician, and chabot can all take part in a two-way conversation on a single thread while remaining HIPAA-compliant.

– Have the option to define financial reward criteria for achieving certain goals. For example, participants can earn rewards for completing a self-reported survey, a set of tasks, breath tests, or any RPM device test compliance.

– Load preset care plan templates as new participants onboard to provide intervention or design and templetize their own automated care plan.

– Deploy programs with app-less (SMS) experience or using a mobile app via API within minutes.

During the program, Vincere Health collected and aggregated data from participants to measure engagement based on habit compliance. This data allowed care teams to segment participants and take proactive actions.


> We want clinicians to be in charge of care pathways and let them create the programs themselves. We want to allow coaches to be autonomous and independent. They can experiment on their own with the help of our platform using Twilio's APIs.

### Using Twilio as the Communication Cloud Provider

Vincere Health's goal was to create a frictionless experience and reduce access barriers to the programs their care teams have built on their platform. Using omni-channel communication where participants can communicate with their care team and access the program either through SMS (app-less experience) or in-app messages has been an integral part of Vincere Health's success in increasing patient engagement.

Twilio was chosen to power this communication because it provided the necessary tools to build HIPAA-compliant, omni-channel communications channels. Twilio's APIs and SDKs enabled Vincere Health to quickly build a scalable and reliable platform.

Twilio Programmable Messaging API was used to send all the SMS nudges and reminders at scale. The long-term maintainability and plug-and-play nature of the Conversations API helped Vincere Health involve their care team members in real-time to build personalized relationships through two-way conversations.


> "A few of the things that stand out the most are developer experience, HIPAA compliance documentation, and long term maintainability. You can own the experience completely while Twilio is the underlying infrastructure for communication."


### Going Forward
With a custom communication platform powered by Twilio and amazing health coaches, Vincere Health has been able to launch successful clinical validations with leading institutions such as Boston Medical Center and their research has been published by the American Thoracic Society Journal.

Vincere Health's goal started with creating tools to support holistic care journeys that enhance care team effectiveness. Automation of day-to-day tasks for patient outreach and timely care team involvement has resulted in meaningful and long-term change for people who need it the most. Vincere Health's next steps are to continue to refine and scale their platform by adding intelligent layers using machine learning and advanced data gathering techniques. Their goal is to engage participants proactively with compassion and relevant care that meets their changing needs.

### The Results
Vincere Health's strategic partners and individual participants are seeing higher program satisfaction rates of 82% Net Promoter Score, higher program engagement rates of 7.4 average weekly touchpoints, and 68% reduction in tobacco usage across populations when carbon monoxide (CO) was measured objectively using devices during clinical trials. Over 150,000 SMS-based nudges were sent resulting in 20% of health coaches' time saved through automated reach and reminders.
