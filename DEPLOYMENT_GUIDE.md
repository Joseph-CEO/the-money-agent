# 🚀 Deployment Guide - Autonomous Commerce Agent

## Overview
This guide will help you deploy your autonomous commerce agent to production for 24/7 operation.

## Quick Deployment Options

### Option 1: AWS EC2 (Recommended)
**Cost:** ~$5-10/month | **Difficulty:** Medium | **Uptime:** 99.9%+

### Option 2: DigitalOcean Droplet
**Cost:** $6/month | **Difficulty:** Easy | **Uptime:** 99.9%+

### Option 3: Google Cloud Compute Engine
**Cost:** Free tier available | **Difficulty:** Medium | **Uptime:** 99.9%+

### Option 4: Heroku
**Cost:** $7/month | **Difficulty:** Very Easy | **Uptime:** 99.9%+

---

## Pre-Deployment Checklist

- [ ] All tests pass (`python test_agent.py`)
- [ ] `.env` file configured with all API keys
- [ ] Affiliate network accounts approved
- [ ] Social media API credentials verified
- [ ] Domain name registered (optional but recommended)
- [ ] Google Analytics set up (optional)

---

## Deployment Method 1: AWS EC2 (Detailed)

### Step 1: Launch EC2 Instance

1. Go to AWS Console > EC2
2. Click "Launch Instance"
3. Choose settings:
   - **AMI:** Ubuntu Server 24.04 LTS
   - **Instance Type:** t2.micro (free tier eligible)
   - **Key Pair:** Create new or use existing
   - **Security Group:** Allow SSH (port 22)
4. Launch instance

### Step 2: Connect to Instance

```bash
# Download your .pem key file
chmod 400 your-key.pem

# Connect via SSH
ssh -i your-key.pem ubuntu@your-ec2-public-ip
```

### Step 3: Install Dependencies

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and tools
sudo apt install -y python3 python3-pip python3-venv git

# Install system dependencies
sudo apt install -y build-essential libssl-dev libffi-dev
```

### Step 4: Upload Agent Files

**Option A: Using SCP**
```bash
# From your local machine
scp -i your-key.pem -r /path/to/agent-files/* ubuntu@your-ec2-ip:/home/ubuntu/agent/
```

**Option B: Using Git**
```bash
# On EC2 instance
git clone your-repository-url
cd your-repository-name
```

**Option C: Manual Upload**
```bash
# Create directory
mkdir -p /home/ubuntu/agent
cd /home/ubuntu/agent

# Upload files one by one using SCP or SFTP client like FileZilla
```

### Step 5: Configure Environment

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy and configure .env
cp env.template .env
nano .env  # Add your API keys
```

### Step 6: Test Installation

```bash
# Run test suite
python test_agent.py

# If all tests pass, run one cycle manually
python autonomous_agent.py
# Press Ctrl+C after one cycle completes
```

### Step 7: Set Up as System Service

```bash
# Create systemd service file
sudo nano /etc/systemd/system/commerce-agent.service
```

Add this content:
```ini
[Unit]
Description=Autonomous Commerce Agent
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/agent
Environment="PATH=/home/ubuntu/agent/venv/bin"
ExecStart=/home/ubuntu/agent/venv/bin/python autonomous_agent.py
Restart=always
RestartSec=10
StandardOutput=append:/home/ubuntu/agent/logs/agent.log
StandardError=append:/home/ubuntu/agent/logs/agent-error.log

[Install]
WantedBy=multi-user.target
```

```bash
# Create logs directory
mkdir -p /home/ubuntu/agent/logs

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable commerce-agent
sudo systemctl start commerce-agent

# Check status
sudo systemctl status commerce-agent
```

### Step 8: Monitor Logs

```bash
# View real-time logs
tail -f /home/ubuntu/agent/logs/agent.log

# View error logs
tail -f /home/ubuntu/agent/logs/agent-error.log

# Check service status
sudo systemctl status commerce-agent
```

### Step 9: Set Up Log Rotation

```bash
sudo nano /etc/logrotate.d/commerce-agent
```

Add:
```
/home/ubuntu/agent/logs/*.log {
    daily
    rotate 7
    compress
    delaycompress
    notifempty
    missingok
}
```

---

## Deployment Method 2: DigitalOcean Droplet

### Step 1: Create Droplet

1. Go to DigitalOcean dashboard
2. Click "Create" > "Droplets"
3. Choose:
   - **Image:** Ubuntu 24.04 LTS
   - **Plan:** Basic ($6/month)
   - **Region:** Closest to your target audience
4. Add SSH key
5. Create Droplet

### Step 2: Follow AWS Steps 2-9

The process is identical to AWS EC2 after you connect via SSH.

```bash
ssh root@your-droplet-ip
```

---

## Deployment Method 3: Heroku (Easiest)

### Step 1: Install Heroku CLI

```bash
# Download from https://devcenter.heroku.com/articles/heroku-cli
# Or on Mac:
brew tap heroku/brew && brew install heroku

# Login
heroku login
```

### Step 2: Prepare Application

```bash
# In your agent directory
# Create Procfile
echo "worker: python autonomous_agent.py" > Procfile

# Create runtime.txt
echo "python-3.11.0" > runtime.txt
```

### Step 3: Deploy

```bash
# Initialize git (if not already)
git init
git add .
git commit -m "Initial deployment"

# Create Heroku app
heroku create your-commerce-agent

# Set config vars (your API keys)
heroku config:set ANTHROPIC_API_KEY=your_key_here
heroku config:set AMAZON_ACCESS_KEY=your_key_here
# ... set all your .env variables

# Deploy
git push heroku main

# Scale worker
heroku ps:scale worker=1

# View logs
heroku logs --tail
```

---

## Post-Deployment Tasks

### 1. Verify Agent is Running

```bash
# Check logs for successful cycles
tail -f logs/agent.log

# Look for:
# "Starting cycle #1"
# "Fetched X offers from all networks"
# "Selected Y offers to promote"
# "Published Z posts to social media"
# "Cycle completed successfully"
```

### 2. Set Up Monitoring Alerts

**CloudWatch (AWS)**
```bash
# Create alarm for EC2 instance health
aws cloudwatch put-metric-alarm \
  --alarm-name commerce-agent-health \
  --alarm-description "Alert if agent stops" \
  --metric-name CPUUtilization \
  --namespace AWS/EC2 \
  --statistic Average \
  --period 300 \
  --threshold 1 \
  --comparison-operator LessThanThreshold
```

**Email Alerts**
Add to your .env:
```
ALERT_EMAIL=your-email@example.com
```

**Slack Alerts**
Add to your .env:
```
SLACK_WEBHOOK=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
```

### 3. Set Up Backup

```bash
# Create backup script
nano /home/ubuntu/backup.sh
```

Add:
```bash
#!/bin/bash
DATE=$(date +%Y%m%d)
tar -czf /home/ubuntu/backups/agent-backup-$DATE.tar.gz \
  /home/ubuntu/agent/agent_stats.json \
  /home/ubuntu/agent/analytics_data/ \
  /home/ubuntu/agent/landing_pages/

# Keep only last 7 days
find /home/ubuntu/backups/ -name "agent-backup-*.tar.gz" -mtime +7 -delete
```

```bash
chmod +x /home/ubuntu/backup.sh

# Add to crontab
crontab -e
# Add line:
0 2 * * * /home/ubuntu/backup.sh
```

### 4. Configure Domain (Optional)

If you have a domain for landing pages:

**AWS Route 53:**
1. Create hosted zone for your domain
2. Point A record to EC2 IP
3. Update SITE_URL in .env

**Cloudflare:**
1. Add domain to Cloudflare
2. Create A record pointing to server IP
3. Enable SSL/TLS

### 5. Set Up SSL (for landing pages)

```bash
# Install Certbot
sudo apt install -y certbot python3-certbot-nginx

# Install Nginx
sudo apt install -y nginx

# Get certificate
sudo certbot --nginx -d yourdomain.com

# Configure Nginx to serve landing pages
sudo nano /etc/nginx/sites-available/default
```

Add:
```nginx
server {
    listen 80;
    server_name yourdomain.com;
    
    location /deals/ {
        alias /home/ubuntu/agent/landing_pages/;
        index index.html;
    }
}
```

```bash
sudo systemctl restart nginx
```

---

## Performance Optimization

### 1. Increase Posting Frequency

After 1-2 weeks of successful operation:

```bash
# Edit .env
POSTS_PER_HOUR=3  # Increase from 2 to 3
```

```bash
# Restart service
sudo systemctl restart commerce-agent
```

### 2. Add More Affiliate Networks

Sign up for additional networks and add credentials to .env:
- ShareASale
- ClickBank
- Rakuten
- PartnerStack

### 3. Expand Social Platforms

Add credentials for:
- Instagram (via Facebook Graph API)
- Pinterest
- LinkedIn
- Reddit

### 4. Optimize Filters

Based on analytics, adjust in .env:
```bash
MIN_COMMISSION_RATE=7.0  # Increase if too many low-commission offers
MIN_DISCOUNT_PERCENT=20.0  # Increase for better deals
```

---

## Scaling to Multiple Instances

When you hit $10/hour and want to scale:

### Option 1: Multiple Accounts
- Create separate accounts for different niches
- Deploy separate instances
- Example: Tech deals, Home goods, Fashion

### Option 2: Increase Frequency
```bash
POSTS_PER_HOUR=6  # Increase posting rate
OFFERS_TO_FETCH=40  # Fetch more offers
```

### Option 3: Geographic Expansion
- Deploy instances in different regions
- Target different Amazon regions (.com, .co.uk, .de)
- Localize content for each market

---

## Troubleshooting Deployment

### Service Won't Start

```bash
# Check service status
sudo systemctl status commerce-agent

# View recent logs
sudo journalctl -u commerce-agent -n 50

# Check for Python errors
python -c "import autonomous_agent"
```

### High Memory Usage

```bash
# Check memory
free -h

# If needed, add swap space
sudo fallocate -l 1G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

### API Rate Limits Hit

```bash
# Reduce posting frequency temporarily
POSTS_PER_HOUR=1

# Spread across more hours
# Modify autonomous_agent.py schedule
```

### No Offers Being Found

```bash
# Check API credentials
python -c "from dotenv import load_dotenv; load_dotenv(); import os; print(os.getenv('AMAZON_ACCESS_KEY'))"

# Test individual network
python -c "from affiliate_connector import *; import asyncio; asyncio.run(test_network())"

# Lower filter thresholds
MIN_COMMISSION_RATE=3.0
MIN_DISCOUNT_PERCENT=10.0
```

---

## Security Best Practices

### 1. Secure API Keys

```bash
# Never commit .env to git
echo ".env" >> .gitignore

# Use environment variables on server
# Don't store keys in code
```

### 2. Update Regularly

```bash
# Set up auto-updates
sudo apt install unattended-upgrades
sudo dpkg-reconfigure --priority=low unattended-upgrades
```

### 3. Firewall Configuration

```bash
# Enable UFW
sudo ufw allow 22  # SSH
sudo ufw allow 80  # HTTP (if serving landing pages)
sudo ufw allow 443  # HTTPS
sudo ufw enable
```

### 4. SSH Hardening

```bash
# Disable password authentication
sudo nano /etc/ssh/sshd_config
# Set: PasswordAuthentication no

sudo systemctl restart sshd
```

---

## Maintenance Schedule

**Daily:**
- Check logs for errors
- Verify posts are publishing
- Monitor revenue in dashboard

**Weekly:**
- Review top performing offers
- Adjust filters based on analytics
- Check for API deprecations

**Monthly:**
- Review total revenue vs goals
- Optimize content templates
- Expand to new networks/platforms
- Backup data

**Quarterly:**
- Audit all API credentials
- Review legal compliance
- Update dependencies
- Scale resources if needed

---

## Success Metrics

Track these KPIs:

1. **Uptime:** Target 99.9%+
2. **Posts/Day:** Target 48 (2/hour)
3. **CTR:** Target 2-5%
4. **Conversion Rate:** Target 1-3%
5. **Revenue/Day:** Target $240+ ($10/hour)
6. **Cost/Revenue Ratio:** Target <5%

---

## Getting Help

If you run into issues:

1. **Check logs:** `tail -f logs/agent.log`
2. **Run tests:** `python test_agent.py`
3. **Review SETUP_GUIDE.md**
4. **Check API status pages:**
   - Amazon PA API Status
   - Twitter API Status
   - Anthropic Status

---

## Next Steps After Deployment

1. **Week 1:** Monitor closely, fix any issues
2. **Week 2:** Analyze performance, optimize filters
3. **Week 3:** Increase posting frequency
4. **Week 4:** Add more networks/platforms
5. **Month 2+:** Scale to multiple niches or regions

---

## Congratulations! 🎉

Your autonomous commerce agent is now deployed and running 24/7.

Monitor your dashboard and watch the revenue grow!

**Expected Timeline:**
- Days 1-7: $0-50 (testing & optimization)
- Days 8-30: $50-200 (learning algorithms)
- Days 31-60: $200-500 (gaining momentum)
- Days 61-90: $500-800 (approaching goal)
- Days 90+: $800+ (goal achieved!)

Good luck! 🚀💰
