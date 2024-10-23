---
authors:
    - hjaveed
hide:
    - toc
date: 2024-10-23
readtime: 5
slug: is-your-security-posture-holding-your-healthcare-startup-back
comments: true
---

# Is Your Security Posture Holding Your Healthcare Startup Back?

When deploying a healthcare product, HIPAA compliance is crucial. No matter how innovative your solution is, without convincing the CIO or security team, you won't get deployed. I view security and HIPAA posture as essential features of any healthcare product.

<!-- more -->

I've successfully deployed healthcare products at large payors and health systems with stringent security requirements. Through my mistakes and successes, I've gained valuable insights that I want to share.

From my observations, early-stage startups often fall into two camps:
1. Those who postpone security considerations, thinking "we'll handle it closer to the pilot or contracting phase."
2. Those who overcompensate based on online advice, creating unnecessarily complex security architectures that become difficult to manage long-term.

As a startup CTO or tech lead, you should focus on two main goals regarding HIPAA and security:

1. Protecting patient data as a fundamental responsibility. Your product must address this seriously from the start.
2. Developing a security posture that convinces healthcare organizations you can deploy quickly without getting bogged down in lengthy security risk assessments.

!!! note
    This post focuses on technical advice for system architecture and navigating dated security risk assessment questionnaires. It doesn't cover legal aspects of compliance policies, BAAs, or insurance needs. Those topics deserve a separate discussion.

!!! note
    While this advice primarily applies to AWS cloud tools, the concepts can be adapted to other cloud providers.

<hr style="border:1px solid #474545">

## Architechting the Cloud

Here's an unpopular opinion: using too many SaaS tools can complicate your HIPAA compliance process. Stick to the essentials. Why? Each SaaS provider requires a BAA, often forcing you into pricier business tiers and expanding your attack surface.

But what about the benefits of SaaS tools? They're undeniably useful. Nowadays, we have fantastic open-source alternatives that you can self-host. Take [Metabase](https://www.metabase.com/){:target="_blank"} for reporting or [Posthog](https://posthog.com/){:target="_blank"} for analytics, for instance. There's also a wealth of open-source observability and monitoring tools at your disposal. Cloud providers also offer managed services within your VPC, giving you the best of both worlds - convenience and control.

!!! note
    Some might ask, "Why bother with self-hosting?" It's simpler than you think. Spinning up an EC2 or GCP VM isn't rocket science. You can easily run dockerized apps, set up automatic EBS volume backups, encrypt data, and manage patches with AWS SSM. This approach often takes less time and money than juggling multiple SaaS subscriptions. While scaling might become a challenge later, by that point, you'll likely have the resources for pricier SaaS options and a dedicated DevOps team.

An air-gapped solution can be a game-changer. It gives you fewer servers or containers to manage and more control over security.

Keep your infrastructure simple from the start. You don't need a plethora of SaaS tools to build something great. Leverage self-hosted and open-source options where possible.

Some providers offer HIPAA-focused wrappers for cloud services, like [Aptible](https://www.aptible.com/){:target="_blank"}. However, these often come with a hefty premium.

What about platforms like [Next.js (Vercel)](https://vercel.com/){:target="_blank"} or [Supabase (Managed)](https://supabase.com/){:target="_blank"}? While they now offer HIPAA-compliant BAAs, convincing security auditors during risk assessments can still be tricky. Personally, I prefer self-hosting. Explaining how Next.js runs your code to an auditor can be a challenge I'd rather avoid. You can always self-host them on your own infra.


## How to answer dated security risk assessment questionnaire

Let's go through some sample questions often asked in the risk assessment process and evaluated by IT teams:

**How do you patch your servers?**
Lol. We don't do it; AWS does it for us. Wait, what do you mean? Or hey, we're on serverless. Auditors be like, "There's gotta be some server somewhere running your code." Remember, these questions are dated and still follow an on-prem mindset. If using AWS EC2, you can demonstrate patches with AWS SSM, or demonstrate ECS Fargate patching, or share documentation around how Lambda layers are patched.

Some example questions below...

- What's your disaster recovery plan?
- Do you have a firewall? Deny all traffic by default?
- What's the intrusion detection and prevention?
- What are the password requirements? Do you lock out on failed attempts, have inactivity timeouts, etc.?

Above are all the good ones, then there are the questions about physical server locations, employee training/access which is not covered in this post.

Following are the components you need to consider for your architecture


### Network Isolation

Network isolation is a critical first step for protecting patient data. You need to properly isolate your resources using VPCs and Subnets - this isn't optional.

Here's what you need to know: Never expose sensitive resources like databases and caches directly to the internet. Put them in private subnets where they're shielded from external access. AWS has made this really straightforward with their VPC and subnet creation tools.

For your architecture:
- Place your API containers and servers in private subnets
- Only expose them through public subnets using an API Gateway, Load Balancer, or Reverse proxy
- Use security groups to strictly control communication between subnets, opening only required ports and protocols

I've seen many teams skip proper network isolation or accidentally expose databases to the internet. This is a major security risk that will immediately raise red flags in any security assessment. Don't make this mistake - be rigorous about your network architecture from day one.

<img src="/assets/vpc-network-architechture.png" alt="VPC netwrok" id="vpc-network" style="display: block; margin-left: auto; margin-right: auto; width: 100%; height: 400px; object-fit: cover;">
<style>
@media (max-width: 767px) {
  #desk-setup-2024 {
    height: auto !important;
  }
}
</style>


### Encrypting in Rest and Transit

Needless to say, use HTTPS for all web communication. Use TLS certs for communicating to DBs, caches, etc. It's very easy to set up.

For data at rest, make sure you're encrypting DB backups, S3 ideally or GCP cloud management services. At the very least, use SSE (S3) or AES256 encryption.

For development, migration DBs could be accessed from local using either VPN ([OpenVPN](https://openvpn.net/){:target="_blank"} on EC2 is cheap and easy) or use a bastion host. Spin up a tiny EC2 with appropriate security group. Instead of using SSH keys, use AWS Session Manager. It's easy to give short-lived credentials to your developers. Or if you want to use managed VPN [Tailscale](https://tailscale.com/){:target="_blank"} is a good option.


### Least Privilege Model and Secrets Management

When it comes to security, less is more. Implement the principle of least privilege to minimize potential attack surfaces:

- Use IAM roles for your servers and containers to access AWS services. This eliminates the need to expose access keys directly.
- Leverage AWS Organizations to manage accounts and services across different environments (DEV, TEST, PROD). This gives you granular control over access and resources.
- Never, ever write secrets directly into your codebase or container images. It's a recipe for disaster. Instead, use AWS Parameter Store or AWS/GCP Secrets Manager. These services make it easy to store and manage sensitive information securely.

### Egress traffic filtering

This is something often overlooked. If you've a web application server, you can use Fully Qualified Domain Name (FQDN) filtering to allow traffic to certain domains and block all others. This is a good approach to limit the data leakage from your API.

With NPM packages or Python packages, they bring a lot of dependencies. There is risk where these dependencies expose your API data to the internet, and you might be exposing your server to the internet without knowing. NAT gateway alone won't help here. AWS Route 53 Resolver [DNS Firewall](https://aws.amazon.com/route53/resolver-dns-firewall/){:target="_blank"} can help here. It's super easy to set up and manage, and you can create reports/monitoring with AWS CloudWatch. Or, if you're ambitious, you can deploy FQDN yourself with NAT, though this isn't recommended for most cases. During security reviews, there have been multiple sites that have asked these questions.

### Penetration Testing
Involve a decent penetration testing company to test your application for vulnerabilities. This is a good exercise to find out if you have any undiscovered vulnerabilities. Plus you get a certificate to demonstrate that you have done a penetration testing.

### Data Retention and Deletion
Retaining CloudWatch logs, retaining DB backups, retaining observability tracing data, retaining API access logs, etc. This is something you can set up. Depending on your policy and data sensitivity, you can set up different retention policies. This will come up in risk assessment questionnaires.

### Intrusion Detection and Prevention
This is a tricky one to start with. Because every risk assessment questionnaire will assess you about intrusion detection and prevention.

There are managed services at least in AWS, particularly for web applications, using [AWS WAF](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/distribution-web-awswaf.html){:target="_blank"} / [AWS Shield](https://docs.aws.amazon.com/waf/latest/developerguide/what-is-aws-waf.html){:target="_blank"} can do a lot of things for prevention. You can integrate AWS WAF very easily either in API Gateway or in ALB. You can use rules to block/allow with pretty easy setup such as preventing SQL injections, cross-site scripting, bad bots, etc.

For intrusion detection, you can use [AWS GuardDuty](https://docs.aws.amazon.com/guardduty/latest/ug/what-is-guardduty.html){:target="_blank"}, to monitor all the resources, set up alerts and demonstrate that you have it enabled.

### Disaster Recovery

Disaster recovery is a crucial aspect that often comes up in security questionnaires. They'll ask about your disaster recovery plan or request details of a DR exercise. Don't let this intimidate you - with AWS, it's more manageable than you might think.

AWS availability zones are a good start. You can set up multi-region resources, create DB replicas with RDS, and implement multi-region S3 replication. However, the database often becomes the bottleneck when documenting your failover exercise.

Most auditors still have an on-premises datacenter mindset. You'll need to educate them on how availability zones work. Be prepared to explain and demonstrate your recovery time objectives (RTO) and recovery point objectives (RPO).

### Frontend Considerations

Make sure you use secure https cookies, implement in-activity timeout, lockout on failed attempts. Implement MFA etc. Lot of these could be implemented with any decent web auth libraries without too much overhead. For out of box solution, [Auth0](https://auth0.com/){:target="_blank"} can provide these or open-source self-hosted solutions like [Keycloak](https://www.keycloak.org/){:target="_blank"} or [Zitadel](https://zitadel.com/){:target="_blank"}. If you have a web application, auditors will ask about frontend security.


## Ending Notes

The above might seem overwhelming, especially for a young company, but in reality, it's manageable. Cloud providers like AWS simplify the process. CTOs often get intimidated by these implementations, but it's not too hard, honestly. You have CDK scripts open-sourced by the [Medplum team](https://github.com/medplum/medplum/tree/main/packages/cdk){:target="_blank"} and many other templates to build your stack from scratch. Implementing VPCs/Subnets, encrypting data, and adopting a least privilege model isn't difficult.

Remember, no matter how robust your application is, you won't get deployed until you convince the IT risk assessment team. No approval means no revenue.

I've also seen CTOs and tech leads make the mistake of hiring a fractional CISO or a dedicated DevOps person too early. The reality is that tech leads with basic knowledge can learn and implement these measures using tools provided by AWS/GCP, particularly AWS in my experience. It doesn't take much time to do this. 

By learning security from the ground up, as a CTO or tech lead, you'll be comfortable answering these questions. Remember, you have a duty to protect patient data rather than completely delegating it to a fractional person or third party. Additionally, many of the measures mentioned above will help you achieve SOC2 Type 2 compliance faster with tools like Vanta or Drata. You can use security compliance policies from these tools and let them monitor your cloud infrastructure. The next frontier will be HITRUST, but it's often not required upfront and can be addressed in later stages of the company.
