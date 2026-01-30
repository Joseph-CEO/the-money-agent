# Autonomous Commerce AI Agent - Complete Setup Guide

## Overview
This autonomous AI agent automates affiliate marketing to generate approximately $10/hour through:
- Automated deal discovery from affiliate networks
- AI-powered content generation
- Multi-platform social media posting
- Landing page creation and hosting
- Analytics and performance tracking

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Affiliate Network Setup](#affiliate-network-setup)
3. [Social Media Setup](#social-media-setup)
4. [Installation](#installation)
5. [Configuration](#configuration)
6. [Deployment Options](#deployment-options)
7. [Running the Agent](#running-the-agent)
8. [Monitoring & Optimization](#monitoring--optimization)
9. [Legal Compliance](#legal-compliance)
10. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Accounts
- [ ] Amazon Associates account (+ API access)
- [ ] CJ Affiliate account
- [ ] Impact account (optional)
- [ ] Twitter/X Developer account
- [ ] Anthropic Claude API account
- [ ] Domain name
- [ ] Hosting service (Vercel/Netlify/AWS)

### Technical Requirements
- Python 3.9+
- Git
- Basic command line knowledge
- Credit card for API services (most have free tiers)

---

## Affiliate Network Setup

### 1. Amazon Associates
**Timeline:** 1-3 days for approval

1. Sign up at https://affiliate-program.amazon.com/
2. Complete profile and website information
3. Wait for approval (usually 1-3 days)
4. After approval, apply for Product Advertising API access:
   - Go to https://webservices.amazon.com/paapi5/documentation/
   - Register for PA API
   - Wait for API approval (1-2 days)
5. Get your credentials:
   - Access Key ID
   - Secret Access Key  
   - Partner Tag (Associate ID)

**Important:** Amazon requires you to generate at least 3 qualifying sales within 180 days or your account will be closed.

### 2. CJ Affiliate (Commission Junction)
**Timeline:** 1-7 days for approval

1. Sign up at https://www.cj.com/
2. Complete publisher application
3. Describe your website/traffic sources
4. Wait for approval
5. Once approved, request API access:
   - Go to Account > API Integration
   - Generate API key
   - Note your Website ID

### 3. Impact (Optional)
**Timeline:** 3-7 days for approval

1. Sign up at https://impact.com/
2. Complete publisher profile
3. Wait for approval
4. Access API credentials in dashboard

---

## Social Media Setup

### Twitter/X API
**Timeline:** Instant to a few hours

1. Go to https://developer.twitter.com/
2. Sign up for Developer Account (Free tier available)
3. Create a new App
4. Generate API keys:
   - API Key
   - API Secret
   - Access Token
   - Access Token Secret
   - Bearer Token
5. Set App permissions to "Read and Write"

**Costs:** Free tier: 1,500 tweets/month, $100/month for 3,000 tweets

### Bluesky (Optional)
1. Create account at https://bsky.app/
2. Generate App Password in Settings > App Passwords
3. Save handle and app password

### Telegram (Optional)
1. Create bot via @BotFather on Telegram
2. Create a channel for posting
3. Add bot as channel admin
4. Save bot token and channel ID

---

## Installation

### 1. Clone or Download Files
```bash
# If using git
git clone <repository-url>
cd autonomous-commerce-agent

# Or download and extract the ZIP file
```

### 2. Set Up Python Environment
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment Variables
```bash
# Copy template
cp .env.template .env

# Edit with your favorite editor
nano .env
# OR
vim .env
```

Fill in all required API keys and credentials.

---

## Configuration

### Minimum Required Configuration
```
# .env file - MUST HAVE:
ANTHROPIC_API_KEY=sk-ant-xxx
AMAZON_ACCESS_KEY=xxx
AMAZON_SECRET_KEY=xxx
AMAZON_PARTNER_TAG=xxx
TWITTER_API_KEY=xxx
TWITTER_API_SECRET=xxx
TWITTER_ACCESS_TOKEN=xxx
TWITTER_ACCESS_SECRET=xxx
SITE_URL=https://yoursite.com
```

### Agent Tuning Parameters
Edit these in `.env` to optimize performance:

```bash
# Posting frequency
POSTS_PER_HOUR=2  # Start conservative

# Offer filtering
MIN_COMMISSION_RATE=5.0  # Minimum 5% commission
MIN_DISCOUNT_PERCENT=15.0  # Minimum 15% off
MIN_PRICE=10.0  # Products $10+
MAX_PRICE=500.0  # Products under $500

# Fetching
OFFERS_TO_FETCH=20  # Fetch 20 offers per cycle
```

---

## Deployment Options

### Option 1: Local Development (Start Here)
**Best for:** Testing, learning, low-cost start

```bash
# Run the agent locally
python autonomous_agent.py
```

Pros:
- Free
- Easy to test and modify
- Full control

Cons:
- Needs to stay running on your computer
- Not accessible 24/7

### Option 2: Cloud VM (Recommended for Production)
**Best for:** 24/7 operation, scalability

#### AWS EC2:
```bash
# 1. Launch t2.micro instance (free tier eligible)
# 2. SSH into instance
# 3. Install dependencies
sudo apt update
sudo apt install python3-pip python3-venv
git clone <your-repo>
cd autonomous-commerce-agent
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 4. Set up as service
sudo nano /etc/systemd/system/affiliate-agent.service
```

Service file content:
```ini
[Unit]
Description=Autonomous Commerce Agent
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/autonomous-commerce-agent
ExecStart=/home/ubuntu/autonomous-commerce-agent/venv/bin/python autonomous_agent.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start
sudo systemctl enable affiliate-agent
sudo systemctl start affiliate-agent
sudo systemctl status affiliate-agent
```

**Costs:** ~$5-10/month for t2.micro

#### DigitalOcean Droplet:
Similar to AWS but simpler interface.
**Costs:** $6/month for basic droplet

### Option 3: Serverless (Advanced)
**Best for:** Minimal costs, automatic scaling

Deploy to AWS Lambda or Google Cloud Functions with scheduled triggers.
**Costs:** <$5/month typically

---

## Running the Agent

### Start the Agent
```bash
# Activate virtual environment
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Run agent
python autonomous_agent.py
```

### What Happens:
1. Agent starts and validates configuration
2. Runs first cycle immediately
3. Schedules hourly cycles
4. Logs activity to `agent.log`
5. Saves metrics to `agent_stats.json`

### Monitor Logs
```bash
# Watch logs in real-time
tail -f agent.log

# View statistics
cat agent_stats.json | python -m json.tool
```

---

## Monitoring & Optimization

### Key Metrics to Track

1. **Click-Through Rate (CTR)**
   - Target: 2-5% is good
   - If <1%: Improve headlines, offers
   - If >5%: Great! Scale up

2. **Conversion Rate**
   - Target: 1-3% is good
   - If <1%: Better offer selection, improve landing pages
   - If >3%: Excellent! Increase volume

3. **Revenue Per Post**
   - Calculate: Total revenue ÷ Posts published
   - Target: $5+ per post for $10/hr goal

4. **Top Performing Categories**
   - Identify which product categories convert best
   - Adjust filters to favor these categories

### Generate Performance Report
```bash
# In Python console or add to agent
from analytics_tracker import AnalyticsTracker
from autonomous_agent import AgentConfig

config = AgentConfig()
tracker = AnalyticsTracker(config)
print(tracker.generate_report())
```

### Optimization Tips

**Week 1-2: Learning Phase**
- Start with 2 posts/hour
- Monitor which offers get clicks
- Track conversion rates
- Adjust filters based on performance

**Week 3-4: Optimization Phase**
- Increase to 3-4 posts/hour if CTR >2%
- Focus on top-performing categories
- A/B test different content styles
- Optimize posting times

**Month 2+: Scaling Phase**
- Add more affiliate networks
- Expand to more social platforms
- Test different price points
- Consider paid promotion for top posts

---

## Legal Compliance

### FTC Compliance (US)
**Required:** Disclose affiliate relationships

✅ On social posts: Add #ad or #affiliate
✅ On landing pages: Include disclosure at top
✅ In emails: Mention affiliate relationship

### GDPR Compliance (EU)
If you have EU visitors:
- Add privacy policy
- Include cookie consent
- Allow opt-out of tracking

### Terms of Service Compliance
- **Amazon:** Must use official links, include disclaimer
- **Twitter:** Follow automation rules, no spam
- **Each network:** Read and follow TOS

### Tax Reporting
- Keep records of all earnings
- Report as business income
- Consider forming LLC (consult accountant)

### Sample Disclosure Text
```
"Disclosure: This post/page contains affiliate links. 
We may earn a commission from purchases made through 
these links at no extra cost to you. We only recommend 
products we believe will provide value."
```

---

## Troubleshooting

### Agent Won't Start
```bash
# Check for missing dependencies
pip install -r requirements.txt --upgrade

# Validate .env file
python -c "from dotenv import load_dotenv; load_dotenv(); import os; print('ANTHROPIC_API_KEY' in os.environ)"
```

### No Offers Returned
- Check affiliate API keys are valid
- Verify account approval status
- Check network for API rate limits
- Review filter thresholds (may be too strict)

### Posts Not Publishing
- Verify social media API credentials
- Check account posting permissions
- Review API rate limits
- Check for account suspensions

### Low Revenue
**Common causes:**
- Poor offer selection (adjust filters)
- Low traffic (increase posting frequency)
- Poor CTR (improve content quality)
- High competition (find better niches)

**Solutions:**
1. Analyze top performers in analytics
2. Focus on those categories/price points
3. Improve content templates
4. Test different posting times

### API Errors
```bash
# Amazon PA API
Error: "Throttled"
Solution: Reduce request frequency, wait and retry

# Twitter API  
Error: "Rate limit exceeded"
Solution: Reduce posts/hour or upgrade API tier

# Claude API
Error: "Invalid API key"
Solution: Check key in .env, regenerate if needed
```

---

## Next Steps

### Week 1 Checklist
- [ ] Set up all required accounts
- [ ] Configure .env file
- [ ] Run first test cycle manually
- [ ] Verify posts appear on social media
- [ ] Check landing pages are accessible
- [ ] Set up Google Analytics

### Week 2 Goals
- [ ] Let agent run for 7 days
- [ ] Track first conversions
- [ ] Analyze top performing offers
- [ ] Optimize filters based on data
- [ ] Increase posting frequency if CTR >2%

### Month 1 Goals
- [ ] Generate first $100 in commissions
- [ ] Achieve 2%+ CTR
- [ ] Achieve 1%+ conversion rate
- [ ] Scale to 3-4 posts/hour
- [ ] Add second affiliate network

### Growth Path to $10/Hour
```
Month 1: $100-200 ($3-6/day, learning phase)
Month 2: $300-500 ($10-16/day, optimization)
Month 3: $600-800 ($20-26/day, scaling)
Month 4+: $1000+ ($30+/day, $10+/hour achieved)
```

---

## Advanced Features (Future Enhancements)

### Email Marketing Integration
- Collect email subscribers
- Send daily/weekly deal emails
- Use Mailchimp or SendGrid API

### AI Image Generation
- Generate custom product images
- Use DALL-E or Midjourney API
- A/B test custom vs product images

### SEO Optimization
- Auto-generate blog posts
- Optimize for product review keywords
- Build backlinks

### Multi-Language Support
- Translate content for international markets
- Target multiple Amazon regions
- Expand to global affiliates

---

## Support & Resources

### Official Documentation
- Amazon PA API: https://webservices.amazon.com/paapi5/documentation/
- CJ API: https://developers.cj.com/
- Twitter API: https://developer.twitter.com/en/docs
- Claude API: https://docs.anthropic.com/

### Community & Help
- Create issues on GitHub
- Join affiliate marketing communities
- Follow affiliate marketing blogs

### Recommended Learning
- Amazon Associates Help: https://affiliate-program.amazon.com/help
- FTC Endorsement Guidelines: https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking
- Twitter Automation Best Practices: https://help.twitter.com/en/rules-and-policies/twitter-automation

---

## License & Disclaimer

This software is provided as-is for educational purposes. 

**Disclaimers:**
- No guarantee of earnings
- Affiliate success depends on many factors
- You are responsible for legal compliance
- Test thoroughly before deploying
- Monitor for policy violations

**Your Responsibilities:**
- Comply with all applicable laws
- Follow platform Terms of Service
- Properly disclose affiliate relationships
- Pay applicable taxes
- Use ethical marketing practices

---

## Quick Start Summary

```bash
# 1. Install
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. Configure
cp .env.template .env
nano .env  # Fill in API keys

# 3. Run
python autonomous_agent.py

# 4. Monitor
tail -f agent.log

# 5. Optimize based on analytics
```

**Minimum time to first revenue:** 7-14 days
**Realistic timeline to $10/hour:** 2-4 months with optimization

Good luck! 🚀
