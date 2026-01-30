# 🚀 EXACT DEPLOYMENT COMMANDS - Copy & Paste

## Choose Your Deployment Method:

---

## ⚡ OPTION 1: LOCAL (Test on Your Computer) - 5 MINUTES

### ✅ **Best for:** Testing before cloud deployment, learning how it works

### **Commands to Run:**

```bash
# Step 1: Navigate to your agent directory
cd /path/to/autonomous-commerce-agent

# Step 2: Create virtual environment
python3 -m venv venv

# Step 3: Activate virtual environment
source venv/bin/activate  # Mac/Linux
# OR
venv\Scripts\activate     # Windows

# Step 4: Install dependencies
pip install -r requirements.txt

# Step 5: Configure your API keys
cp env.template .env
nano .env  # Edit this file and add your API keys

# Step 6: Test everything
python test_agent.py

# Step 7: Start the agent!
python autonomous_agent.py
```

### **Keep It Running 24/7:**

**Option A - Using screen:**
```bash
screen -S agent
python autonomous_agent.py
# Press Ctrl+A then D to detach
# Reattach with: screen -r agent
```

**Option B - Using nohup:**
```bash
nohup python autonomous_agent.py > agent.log 2>&1 &
# View logs: tail -f agent.log
```

### **Monitor:**
```bash
# View logs
tail -f agent.log

# Check stats
cat agent_stats.json | python -m json.tool

# Open dashboard
open dashboard.html  # Mac
xdg-open dashboard.html  # Linux
start dashboard.html  # Windows
```

---

## 🌩️ OPTION 2: AWS EC2 (Recommended for Production) - 15 MINUTES

### ✅ **Best for:** 24/7 reliable operation, professional setup

### **Cost:** ~$5-10/month (t2.micro is free tier eligible)

### **Step 1: Launch EC2 Instance**

```bash
# Go to AWS Console: https://console.aws.amazon.com/ec2/

# 1. Click "Launch Instance"
# 2. Name: commerce-agent
# 3. AMI: Ubuntu Server 24.04 LTS
# 4. Instance type: t2.micro
# 5. Key pair: Create new (download .pem file)
# 6. Network: Allow SSH (port 22)
# 7. Storage: 8 GB (default)
# 8. Click "Launch Instance"
# 9. Note your instance's PUBLIC IP ADDRESS
```

### **Step 2: Connect to Your Instance**

```bash
# Make key file secure
chmod 400 your-key.pem

# Connect via SSH (replace YOUR_EC2_IP)
ssh -i your-key.pem ubuntu@YOUR_EC2_IP
```

### **Step 3: Upload Files to EC2**

**FROM YOUR LOCAL MACHINE** (in a new terminal):
```bash
# Upload all files to EC2
scp -i your-key.pem -r /path/to/agent-files/* ubuntu@YOUR_EC2_IP:/home/ubuntu/agent/

# Or use individual files
scp -i your-key.pem *.py ubuntu@YOUR_EC2_IP:/home/ubuntu/agent/
scp -i your-key.pem *.txt ubuntu@YOUR_EC2_IP:/home/ubuntu/agent/
scp -i your-key.pem *.md ubuntu@YOUR_EC2_IP:/home/ubuntu/agent/
scp -i your-key.pem *.html ubuntu@YOUR_EC2_IP:/home/ubuntu/agent/
scp -i your-key.pem env.template ubuntu@YOUR_EC2_IP:/home/ubuntu/agent/.env
```

### **Step 4: Set Up on EC2**

**ON YOUR EC2 INSTANCE** (via SSH):
```bash
# Go to agent directory
cd /home/ubuntu/agent

# Run automated setup
chmod +x deploy.sh
./deploy.sh

# OR manual setup:
sudo apt update
sudo apt install -y python3 python3-pip python3-venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### **Step 5: Configure API Keys**

```bash
# Edit .env file
nano .env

# Add your keys:
# ANTHROPIC_API_KEY=sk-ant-xxx
# AMAZON_ACCESS_KEY=xxx
# TWITTER_API_KEY=xxx
# etc.

# Save: Ctrl+X, then Y, then Enter
```

### **Step 6: Set Up as System Service**

```bash
# Create service file
sudo nano /etc/systemd/system/commerce-agent.service
```

**Paste this content:**
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

**Save and enable:**
```bash
# Create logs directory
mkdir -p /home/ubuntu/agent/logs

# Enable service
sudo systemctl daemon-reload
sudo systemctl enable commerce-agent
sudo systemctl start commerce-agent

# Check status
sudo systemctl status commerce-agent
```

### **Step 7: Monitor**

```bash
# View live logs
tail -f /home/ubuntu/agent/logs/agent.log

# Check service status
sudo systemctl status commerce-agent

# Restart if needed
sudo systemctl restart commerce-agent

# Stop service
sudo systemctl stop commerce-agent
```

---

## 🐳 OPTION 3: DigitalOcean Droplet (Easiest Cloud) - 10 MINUTES

### ✅ **Best for:** Simple setup, great documentation

### **Cost:** $6/month

### **Step 1: Create Droplet**

```bash
# Go to: https://cloud.digitalocean.com/droplets

# 1. Click "Create" > "Droplets"
# 2. Choose Ubuntu 24.04 LTS
# 3. Choose Basic plan ($6/month)
# 4. Select region (closest to you)
# 5. Add SSH key (or use password)
# 6. Name: commerce-agent
# 7. Click "Create Droplet"
# 8. Note your droplet's IP ADDRESS
```

### **Step 2: Connect**

```bash
ssh root@YOUR_DROPLET_IP
```

### **Step 3: Upload Files**

**FROM YOUR LOCAL MACHINE:**
```bash
scp -r /path/to/agent-files/* root@YOUR_DROPLET_IP:/root/agent/
```

### **Step 4-7: Same as AWS EC2 Steps Above**

Just replace `ubuntu` with `root` and `/home/ubuntu` with `/root`

---

## 🎯 OPTION 4: Heroku (Absolutely Easiest) - 10 MINUTES

### ✅ **Best for:** Zero server management, instant deployment

### **Cost:** $7/month

### **Step 1: Install Heroku CLI**

```bash
# Mac
brew tap heroku/brew && brew install heroku

# Ubuntu/Debian
curl https://cli-assets.heroku.com/install.sh | sh

# Windows
# Download from: https://devcenter.heroku.com/articles/heroku-cli
```

### **Step 2: Login**

```bash
heroku login
# Press any key to open browser and login
```

### **Step 3: Prepare Application**

```bash
cd /path/to/agent

# Create Procfile
echo "worker: python autonomous_agent.py" > Procfile

# Create runtime.txt
echo "python-3.11.0" > runtime.txt

# Initialize git
git init
git add .
git commit -m "Initial deployment"
```

### **Step 4: Create Heroku App**

```bash
heroku create your-commerce-agent
# Note the app name shown
```

### **Step 5: Configure Environment Variables**

```bash
# Set ALL your environment variables
heroku config:set ANTHROPIC_API_KEY=sk-ant-xxx
heroku config:set AMAZON_ACCESS_KEY=xxx
heroku config:set AMAZON_SECRET_KEY=xxx
heroku config:set AMAZON_PARTNER_TAG=xxx
heroku config:set TWITTER_API_KEY=xxx
heroku config:set TWITTER_API_SECRET=xxx
heroku config:set TWITTER_ACCESS_TOKEN=xxx
heroku config:set TWITTER_ACCESS_SECRET=xxx
heroku config:set SITE_URL=https://yourdeals.com

# Add more as needed
heroku config:set SHOPIFY_PARTNER_ID=xxx
heroku config:set POSTS_PER_HOUR=2
heroku config:set MIN_COMMISSION_RATE=5.0
```

### **Step 6: Deploy**

```bash
git push heroku main
# Or: git push heroku master
```

### **Step 7: Scale Worker**

```bash
heroku ps:scale worker=1
```

### **Step 8: Monitor**

```bash
# View logs
heroku logs --tail

# Check status
heroku ps

# Restart
heroku restart

# Stop
heroku ps:scale worker=0
```

---

## 🔥 OPTION 5: Google Cloud (Free Tier) - 15 MINUTES

### ✅ **Best for:** Long-term free option (12 months free + always free tier)

### **Step 1: Create VM Instance**

```bash
# Go to: https://console.cloud.google.com/compute/instances

# 1. Click "CREATE INSTANCE"
# 2. Name: commerce-agent
# 3. Region: us-central1 (always free eligible)
# 4. Machine type: e2-micro (always free)
# 5. Boot disk: Ubuntu 24.04 LTS
# 6. Firewall: Allow HTTP/HTTPS (optional)
# 7. Click "Create"
# 8. Note the External IP
```

### **Step 2: Connect**

```bash
# Using gcloud CLI
gcloud compute ssh commerce-agent --zone=us-central1-a

# Or use browser SSH (click "SSH" in console)
```

### **Step 3-7: Same as AWS EC2 Steps**

---

## 📋 POST-DEPLOYMENT CHECKLIST

**After deploying to ANY platform:**

```bash
# 1. Verify agent is running
tail -f agent.log
# Look for: "Starting cycle #1", "Cycle completed successfully"

# 2. Check social media
# Visit Twitter/Telegram - do you see posts?

# 3. Check landing pages
ls landing_pages/
# Should see HTML files being created

# 4. Monitor analytics
cat agent_stats.json

# 5. Open dashboard
# Download dashboard.html and open in browser
```

---

## 🆘 QUICK TROUBLESHOOTING

### **Agent won't start:**
```bash
# Check logs for errors
tail -50 agent.log

# Verify Python dependencies
pip install -r requirements.txt

# Check .env file
cat .env | grep API_KEY
```

### **No posts appearing:**
```bash
# Test social media credentials
python -c "from social_publisher import SocialPublisher; from autonomous_agent import AgentConfig; p = SocialPublisher(AgentConfig()); print('OK')"

# Check API rate limits
# Twitter: 1500 tweets/month on free tier
```

### **No offers found:**
```bash
# Lower thresholds in .env
MIN_COMMISSION_RATE=3.0
MIN_DISCOUNT_PERCENT=10.0

# Then restart:
sudo systemctl restart commerce-agent
```

---

## 🎯 QUICK START RECOMMENDATION

**Fastest path to earning:**

1. **Start LOCAL** (5 minutes)
   - Test everything works
   - See your first cycle
   - Verify posts appear

2. **Move to DIGITALOCEAN** (10 minutes)
   - Simple, cheap, reliable
   - Good documentation
   - Easy to manage

3. **Scale to AWS** (later)
   - When revenue justifies it
   - Better performance
   - More professional

---

## 📞 NEED HELP?

**Check these first:**
1. `tail -f agent.log` - See what's happening
2. `python test_agent.py` - Run diagnostic tests
3. SETUP_GUIDE.md - Detailed instructions
4. DEPLOYMENT_GUIDE.md - Advanced deployment

**Common Issues:**
- Missing API keys → Edit .env
- Tests failing → Check API credentials
- Service won't start → Check logs
- No revenue → Give it 7-14 days

---

## ✅ SUCCESS INDICATORS

**You'll know it's working when:**
- ✅ Logs show "Cycle completed successfully"
- ✅ Posts appear on social media (with #ad)
- ✅ Landing pages are being created
- ✅ agent_stats.json shows increasing numbers
- ✅ First clicks tracked in analytics
- ✅ First sale notification!

---

**Choose your deployment method above and copy the commands!** 🚀
