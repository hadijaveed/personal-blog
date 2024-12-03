---
authors:
    - hjaveed
hide:
    - toc
date: 2024-11-17
readtime: 5
slug: reversing-the-curse-of-conditional-workflows-with-llms
comments: true
---

# Can we revere the curse of rigid journeys/workflows with LLMs?

Does not matter if you are working with a marketing flow, e-commerce or in health-care. Being part of the health-care industry I've experienced it first hand how much hard it is to scale if/then/else journeys on different scenarios.. In health-care a lot of automated care is provided like before your appointment, after or discharge. often there are complex journeys for communication, pro-active out-reach or others

Consider e-commerce use-case, a visitor visited your store website.. and there is a complex journey to convert visitor intent to buyer, through pro-active outreach, offering up offers

usually these journeys/flows are anchored around if then else on new data observations such as page view, did X, or temporal relationship around time, meaning 5 days after user bought the first product

```diagram
e.g,      [patient watches video content]
                /              \
               /                \
              yes                no
               |                  \
             send_more         let's send another reminder
                                    \
                                   did they open?
                                      /      \
                                    yes       no
                                 send_more     try different intervention
```                                         


Now in the case above, imagine how many permutations you'll have to build once you start building more complex journeys. Personalization is hard at a user level or for patient in the above example. And either the marketing teams or the content building teams have to spend significant time in tweaking these journeys or change them. Contextual data based personalization adds value too.

Don't get me wrong, DAG based journey do serve a need. they are predictable state machines and are reliable. but to scale them in different scenarios and personalization is a difficult feat.

Enter LLM era.. can we create a journey with LLM, define outcome we want to achieve and LLM as a state machine can handle all of the rest? 
a). with strong reasoning capabilities the hope is workflows adjust fast, b). as the content scales or new permutations needs to be created, instead of created a hell of if/then/else logic, you define it as a policy and LLM as a state machine takes care of the rest. 
c). the llm as journey state machine observes the state and adopts as new bits and pieces of information gets appended to the context

How predictable it will be? For certain actions such as making a sensitive API call based on user action, or sending certain comms. can be catastrophic. 

Let's test this:

```
LLM as a state machine
[time based events]
                  \
                   \
                    >
                   [Machine] ---> action
                    /      \
[new-context] ->   /        \
                [Context] [Journey Policy]
```

## Code API

simple API... 

StorageAPI
    - store .. this stores the last execution
    - retrieve .. this stores the last retriever
    - run_scheduled_jobs .. runs the scheduled jobs

```py
w1 = Workflow(
    policy="""
    your job is to help customer buy a product. there are certain rules
    you need to observe and figure out.. how we can buy it or do it

    
    """,
    actions=[
        "action.send_sms",
        "action.suggest_new_products",
        "action.suggest_new_promotion",
    ],
    context={}, ## any kind of json context should work
    mode="adaptive/locked",
    storage=MemoryStore() or PostgresStore(),
)

w1.input("") ## send new input

w1.add_context("") ## append to already existing context

w1.on_action(subscribe_to_action)

def action_subscriber(action_type: dict, current_context: ContextStore:
    if action_type == x:
        do something...
    elif action_type == y:
        do something...
        current_context.add({ "new_info": "something happened" })

w1.get_mermaid() ## generates the mermaid diagram

w1.lock()
## context will be appended across all the execution of the journey
```

what about timing? temporal relationships? e.g, remind someone after every 5 minutes.. e.g, if someone say execute the flow after 5 minutes how would that happen? if someone says 30 minutes after reach out to the user how would that happen?

parses actions it will need to execute based on the document.. so time based relationships are scheduled. if something changes in middle.. it will cancel the time based relationship etc..

how do we parse dates and store them in the database?
- 5 days after they bought their product, I want you to send a promotional ad.
- check if user buys the product, if they do great, no need to do anything
- if they don't do it, let's try texting them the promotional message here
- if they buy the product cancel the previous step.
- once the product is bought, 2-weeks after tell them how much rewards they have accumulated.. they could buy more
- share more promotional deals etc..
- wait if they don't open the promotional email let's keep repeating these steps. but don't do it for more than 3 times
## Evals

------------------------------------------------------------------
We need to generate tons of evals and see how it performs over the time

I want to sell a product... send a promotional email message to them use appropiate action to do so

wait for at-least 3 days to see if they opened the message... if they did great.. if they did not schedule another message to be send after 2 days. maybe SMS this time? great..

ok so if they've opened the message, you will know, immediately send a an email saying hey it's 100% off now.. great.

wait for them to make a decision. if they buy product great. if they don't let's reach out to them

be smart, schedule things as needed..
---------------------------------