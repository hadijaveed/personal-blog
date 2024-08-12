---
authors:
    - hjaveed
hide:
    - toc
date: 2022-03-04
readtime: 3
slug: helping-people-quit-smoking-through-financial-rewards
---

# Helping People Quit Smoking Through Financial Rewards

Guest post on [AWS Startups Blog](https://aws.amazon.com/blogs/startups/helping-people-quit-smoking-through-financial-rewards/){:target="_blank"}

Smoking is still the leading cause of preventable death, and the pandemic made matters worse: cigarette sales increased in 2020 for the first time in over 20 years. There are over 34 million adult smokers in the US, many of whom are lower income. Reaching them and providing effective support at this scale while keeping costs down can only be achieved with the aid of technology and carefully designed patient experience.

<!-- more -->

[Vincere Health](https://www.vincere.health/){:target="_blank"} is one of few health technology platforms built for people in diverse socio-economic categories. Unlike traditional cessation programs, Vincere offers low-cost access to addiction healthcare using reward-based habit training. Our belief is clinicians in the loop are integral to lasting behavior change, and the technology serves to facilitate and personalize this relationship at scale.

<img src="https://d2908q01vomqb2.cloudfront.net/cb4e5208b4cd87268b208e49452ed6e89a68e0b8/2022/03/01/Vincere.png" alt="Vincere Health" style="display: block; margin-left: auto; margin-right: auto;">


## Need for a personalized “quit journey”
Smoking cessation is best represented as a journey, not a single event. The personalized care experience that is individualized to each participant’s needs has shown increased rates of success conquering addiction with care compliance rates up to 80% and quit rates up to 35%. Participants are encouraged to set compelling yet reachable weekly goals using our program and stay connected to their health coaches for support.

Our platform allows health coaches to create a personalized participant quit journey.

- Health coaches can create a care journey for multiple days/months that can track multiple events just like on a calendar, e.g, breath test at a specific time/day, complete a self-reported outcome survey, or participant/coach video call appointment.
- Coaches can define financial reward criteria for achieving a certain goal. e.g, participants can earn rewards for completing a self-reported survey, breath test habit compliance, or making it to the appointments.
- Define personalized reminders and notifications. These reminders could be configured to go out at different intervals looking at the user information for behavioral reinforcement and motivational nudges.

During the program, we collect and aggregate lots of data from participants, to measure engagement based on habit compliance, take proactive actions, and inform health coaches about participant triggers or relapses.

## Using AWS Cloud to scale
We chose AWS as our cloud provider because AWS provided the necessary tools to help us build a HIPAA-compliant platform. The plug-and-play nature of AWS architecture helped us iterate faster as a startup with a small team.


<img src="https://d2908q01vomqb2.cloudfront.net/cb4e5208b4cd87268b208e49452ed6e89a68e0b8/2022/03/01/Helping-People-Quit-Smoking-Through-Financial-Rewards.png" alt="Helping People Quit Smoking Through Financial Rewards" style="display: block; margin-left: auto; margin-right: auto;">

Let’s explore the main components behind our architecture.

- We embrace microservice architecture that runs on top of [AWS Fargate](https://aws.amazon.com/fargate/){:target="_blank"}. Fargate helps us a lot to avoid the operational burdens of managing servers and allows us to scale, meeting the growing needs of our workloads.
- [Amazon Relational Database Service (Amazon RDS)](https://aws.amazon.com/rds/){:target="_blank"} is our main transactional database. [Amazon ElastiCache](https://aws.amazon.com/elasticache/) complements our core database in performance by caching read-heavy data.
- We use [Amazon Redshift](https://aws.amazon.com/pm/redshift/?trk=ps_a134p000007C7V4AAK&trkCampaign=acq_paid_search_brand&sc_channel=PS&sc_campaign=acquisition_US&sc_publisher=Google&sc_category=Analytics&sc_country=US&sc_geo=NAMER&sc_outcome=acq&sc_detail=amazon%20redshift&sc_content=Redshift_e&sc_matchtype=e&sc_segment=556597604330&sc_medium=PAC-PaaS-P%7CPS-GO%7CBrand%7CDesktop%7CSU%7CAnalytics%7CRedshift%7CUS%7CEN%7CText%7Cxx%7CEXT&s_kwcid=AL!4422!3!556597604330!e!!g!!amazon%20redshift&ef_id=Cj0KCQjwrJOMBhCZARIsAGEd4VFC9elMgztWVthtW30ydhxWYHozW1_K0xPs3kl1UPvCrazjILettKgaAso9EALw_wcB:G:s&s_kwcid=AL!4422!3!556597604330!e!!g!!amazon%20redshift){:target="_blank"} as the central data warehouse and Amazon S3 as a scalable data lake, merging all application data with events, engagement data, device data, and rewards for analytics and understanding our participants better.
- [Amazon Chime SDK](https://aws.amazon.com/chime/chime-sdk/){:target="_blank"} helped us build audio/video communication tools faster, which are leveraged by our health coaches to communicate and keep a personal connection with participants.


## Going Forward
Due to our personalized smoking cessation platform built on AWS and our amazing health coaches, we have been able to launch successful clinical validations with leading institutions such as Boston Medical Center and their research has been [accepted by a prestigious American Thoracic Society journal](https://www.atsjournals.org/doi/10.1164/ajrccm-conference.2021.203.1_MeetingAbstracts.A1676){:target="_blank"}.

Our strategic partners and individual participants are seeing higher program satisfaction rates of 82% Net Promoter Score, 68% reduction in tobacco usage across the population when CO (Carbon Monoxide) was measured objectively using the devices, and higher program engagement rates where on average 7.4 weekly touchpoints were measured during the clinical trial.

AWS proved to be the best architecture for Vincere Health because it provides capabilities to allow us to comply with HIPAA with ease and confidence. Achieving our goal started with data gathering and learning more from participants. Our next steps are to continue to build our platform and add more intelligent layers on the platform using Machine Learning and advanced data gathering techniques to scale our program and reach out to participants proactively who are in the need of the most.
