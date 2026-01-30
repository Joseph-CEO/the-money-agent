#!/bin/bash

# Autonomous Commerce Agent - Automated Deployment Script
# This script automates the deployment process for Ubuntu/Debian systems

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper functions
print_header() {
    echo -e "\n${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}\n"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

# Check if running on supported OS
check_os() {
    if [[ -f /etc/os-release ]]; then
        . /etc/os-release
        if [[ "$ID" != "ubuntu" && "$ID" != "debian" ]]; then
            print_error "This script is designed for Ubuntu/Debian. Your OS: $ID"
            exit 1
        fi
        print_success "Running on $PRETTY_NAME"
    else
        print_error "Cannot detect OS"
        exit 1
    fi
}

# Install system dependencies
install_dependencies() {
    print_header "Installing System Dependencies"
    
    sudo apt update
    print_success "Updated package lists"
    
    sudo apt install -y python3 python3-pip python3-venv git curl build-essential
    print_success "Installed Python and build tools"
    
    # Optional: Install Nginx for serving landing pages
    read -p "Install Nginx for serving landing pages? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        sudo apt install -y nginx
        print_success "Installed Nginx"
    fi
}

# Set up application directory
setup_directory() {
    print_header "Setting Up Application Directory"
    
    INSTALL_DIR="$HOME/commerce-agent"
    
    if [[ -d "$INSTALL_DIR" ]]; then
        print_warning "Directory $INSTALL_DIR already exists"
        read -p "Delete and recreate? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            rm -rf "$INSTALL_DIR"
            print_success "Removed old directory"
        else
            print_info "Using existing directory"
        fi
    fi
    
    mkdir -p "$INSTALL_DIR"
    cd "$INSTALL_DIR"
    print_success "Created directory: $INSTALL_DIR"
}

# Copy application files
copy_files() {
    print_header "Copying Application Files"
    
    # Assuming files are in current directory
    if [[ -f "autonomous_agent.py" ]]; then
        print_info "Copying files from current directory..."
        cp *.py "$INSTALL_DIR/" 2>/dev/null || true
        cp *.txt "$INSTALL_DIR/" 2>/dev/null || true
        cp *.md "$INSTALL_DIR/" 2>/dev/null || true
        cp *.html "$INSTALL_DIR/" 2>/dev/null || true
        cp env.template "$INSTALL_DIR/.env" 2>/dev/null || true
        print_success "Files copied"
    else
        print_error "Application files not found in current directory"
        print_info "Please ensure you're running this script from the agent directory"
        exit 1
    fi
}

# Set up Python virtual environment
setup_virtualenv() {
    print_header "Setting Up Python Virtual Environment"
    
    cd "$INSTALL_DIR"
    python3 -m venv venv
    print_success "Created virtual environment"
    
    source venv/bin/activate
    pip install --upgrade pip
    print_success "Upgraded pip"
    
    if [[ -f "requirements.txt" ]]; then
        pip install -r requirements.txt
        print_success "Installed Python dependencies"
    else
        print_error "requirements.txt not found"
        exit 1
    fi
}

# Configure environment variables
configure_env() {
    print_header "Configuring Environment Variables"
    
    cd "$INSTALL_DIR"
    
    if [[ ! -f ".env" ]]; then
        if [[ -f "env.template" ]]; then
            cp env.template .env
        else
            print_error ".env template not found"
            return
        fi
    fi
    
    print_info "You need to configure your API keys in .env"
    print_info "Required keys:"
    echo "  - ANTHROPIC_API_KEY (Claude AI)"
    echo "  - AMAZON_ACCESS_KEY, AMAZON_SECRET_KEY, AMAZON_PARTNER_TAG"
    echo "  - TWITTER_API_KEY, TWITTER_API_SECRET, etc."
    echo ""
    
    read -p "Open .env file for editing now? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        ${EDITOR:-nano} .env
        print_success "Configuration saved"
    else
        print_warning "Remember to edit .env before starting the agent!"
    fi
}

# Create systemd service
create_service() {
    print_header "Creating Systemd Service"
    
    read -p "Set up agent as systemd service for auto-start? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_info "Skipping service creation"
        return
    fi
    
    SERVICE_FILE="/etc/systemd/system/commerce-agent.service"
    
    sudo tee "$SERVICE_FILE" > /dev/null <<EOF
[Unit]
Description=Autonomous Commerce Agent
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$INSTALL_DIR
Environment="PATH=$INSTALL_DIR/venv/bin"
ExecStart=$INSTALL_DIR/venv/bin/python autonomous_agent.py
Restart=always
RestartSec=10
StandardOutput=append:$INSTALL_DIR/logs/agent.log
StandardError=append:$INSTALL_DIR/logs/agent-error.log

[Install]
WantedBy=multi-user.target
EOF
    
    print_success "Created service file: $SERVICE_FILE"
    
    # Create logs directory
    mkdir -p "$INSTALL_DIR/logs"
    
    # Enable service
    sudo systemctl daemon-reload
    sudo systemctl enable commerce-agent
    print_success "Service enabled (will start on boot)"
}

# Run tests
run_tests() {
    print_header "Running Tests"
    
    cd "$INSTALL_DIR"
    source venv/bin/activate
    
    if [[ -f "test_agent.py" ]]; then
        print_info "Running test suite..."
        python test_agent.py
    else
        print_warning "test_agent.py not found, skipping tests"
    fi
}

# Configure firewall
configure_firewall() {
    print_header "Configuring Firewall"
    
    read -p "Configure UFW firewall? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        return
    fi
    
    sudo apt install -y ufw
    sudo ufw allow 22/tcp  # SSH
    
    if command -v nginx &> /dev/null; then
        sudo ufw allow 80/tcp   # HTTP
        sudo ufw allow 443/tcp  # HTTPS
    fi
    
    sudo ufw --force enable
    print_success "Firewall configured"
}

# Set up log rotation
setup_logrotate() {
    print_header "Setting Up Log Rotation"
    
    sudo tee /etc/logrotate.d/commerce-agent > /dev/null <<EOF
$INSTALL_DIR/logs/*.log {
    daily
    rotate 7
    compress
    delaycompress
    notifempty
    missingok
    create 0644 $USER $USER
}
EOF
    
    print_success "Log rotation configured"
}

# Print completion message
print_completion() {
    print_header "Deployment Complete! 🎉"
    
    echo -e "${GREEN}Your autonomous commerce agent has been deployed!${NC}\n"
    
    echo -e "${BLUE}Installation Directory:${NC} $INSTALL_DIR"
    echo -e "${BLUE}Configuration File:${NC} $INSTALL_DIR/.env"
    echo -e "${BLUE}Logs Directory:${NC} $INSTALL_DIR/logs\n"
    
    echo -e "${YELLOW}Next Steps:${NC}"
    echo -e "  1. Edit configuration: ${BLUE}nano $INSTALL_DIR/.env${NC}"
    echo -e "  2. Add your API keys to .env"
    echo -e "  3. Start the agent: ${BLUE}sudo systemctl start commerce-agent${NC}"
    echo -e "  4. View logs: ${BLUE}tail -f $INSTALL_DIR/logs/agent.log${NC}"
    echo -e "  5. Check status: ${BLUE}sudo systemctl status commerce-agent${NC}\n"
    
    echo -e "${YELLOW}Useful Commands:${NC}"
    echo -e "  Start agent:   ${BLUE}sudo systemctl start commerce-agent${NC}"
    echo -e "  Stop agent:    ${BLUE}sudo systemctl stop commerce-agent${NC}"
    echo -e "  Restart agent: ${BLUE}sudo systemctl restart commerce-agent${NC}"
    echo -e "  View logs:     ${BLUE}tail -f $INSTALL_DIR/logs/agent.log${NC}"
    echo -e "  Run tests:     ${BLUE}cd $INSTALL_DIR && source venv/bin/activate && python test_agent.py${NC}\n"
    
    echo -e "${GREEN}Dashboard:${NC} Open $INSTALL_DIR/dashboard.html in your browser\n"
    
    echo -e "${YELLOW}Important:${NC}"
    echo -e "  • Configure all API keys in .env before starting"
    echo -e "  • See SETUP_GUIDE.md for detailed instructions"
    echo -e "  • See DEPLOYMENT_GUIDE.md for production tips\n"
}

# Main deployment flow
main() {
    echo -e "${GREEN}"
    echo "╔════════════════════════════════════════════════════════════╗"
    echo "║   AUTONOMOUS COMMERCE AGENT - AUTOMATED DEPLOYMENT        ║"
    echo "║                                                            ║"
    echo "║   This script will set up your agent for production       ║"
    echo "╚════════════════════════════════════════════════════════════╝"
    echo -e "${NC}\n"
    
    read -p "Continue with deployment? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_info "Deployment cancelled"
        exit 0
    fi
    
    check_os
    install_dependencies
    setup_directory
    copy_files
    setup_virtualenv
    configure_env
    create_service
    configure_firewall
    setup_logrotate
    run_tests
    print_completion
}

# Run main function
main "$@"
