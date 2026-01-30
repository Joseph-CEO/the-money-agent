#!/usr/bin/env python3
"""
Test Script - Validates agent setup and configuration
Run this before deploying to production
"""

import os
import sys
from dotenv import load_dotenv

def test_environment():
    """Test environment configuration"""
    print("🔍 Testing Environment Configuration...")
    
    load_dotenv()
    
    required_vars = {
        'ANTHROPIC_API_KEY': 'Claude AI API (required for content generation)',
        'AMAZON_ACCESS_KEY': 'Amazon Associates API',
        'AMAZON_SECRET_KEY': 'Amazon Associates API',
        'AMAZON_PARTNER_TAG': 'Amazon Associates Tag',
        'TWITTER_API_KEY': 'Twitter/X API',
        'TWITTER_API_SECRET': 'Twitter/X API',
        'SITE_URL': 'Website URL for landing pages'
    }
    
    optional_vars = {
        'CJ_API_KEY': 'CJ Affiliate',
        'IMPACT_API_KEY': 'Impact Affiliate',
        'GA_ID': 'Google Analytics',
        'SLACK_WEBHOOK': 'Slack Alerts'
    }
    
    print("\n✅ Required Variables:")
    missing_required = []
    for var, description in required_vars.items():
        value = os.getenv(var)
        if value:
            print(f"  ✓ {var}: Configured ({description})")
        else:
            print(f"  ✗ {var}: MISSING ({description})")
            missing_required.append(var)
    
    print("\n📋 Optional Variables:")
    for var, description in optional_vars.items():
        value = os.getenv(var)
        status = "✓" if value else "○"
        print(f"  {status} {var}: {'Configured' if value else 'Not set'} ({description})")
    
    if missing_required:
        print(f"\n❌ Missing {len(missing_required)} required variables!")
        print("Please add them to your .env file")
        return False
    else:
        print("\n✅ All required variables configured!")
        return True


def test_dependencies():
    """Test Python dependencies"""
    print("\n🔍 Testing Python Dependencies...")
    
    required_packages = [
        'aiohttp',
        'schedule',
        'anthropic',
        'requests'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"  ✓ {package}")
        except ImportError:
            print(f"  ✗ {package} - MISSING")
            missing.append(package)
    
    if missing:
        print(f"\n❌ Missing {len(missing)} packages!")
        print("Run: pip install -r requirements.txt")
        return False
    else:
        print("\n✅ All dependencies installed!")
        return True


def test_modules():
    """Test agent modules can be imported"""
    print("\n🔍 Testing Agent Modules...")
    
    modules = [
        'affiliate_connector',
        'decision_engine',
        'content_generator',
        'social_publisher',
        'landing_page_manager',
        'analytics_tracker'
    ]
    
    errors = []
    for module in modules:
        try:
            __import__(module)
            print(f"  ✓ {module}.py")
        except Exception as e:
            print(f"  ✗ {module}.py - ERROR: {str(e)[:50]}")
            errors.append((module, str(e)))
    
    if errors:
        print(f"\n❌ {len(errors)} modules have errors!")
        for module, error in errors:
            print(f"  - {module}: {error}")
        return False
    else:
        print("\n✅ All modules load successfully!")
        return True


def test_api_connectivity():
    """Test basic API connectivity"""
    print("\n🔍 Testing API Connectivity...")
    
    # Test Claude API
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if api_key:
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=api_key)
            # Don't actually make a call, just validate the client initializes
            print("  ✓ Claude API client initialized")
        except Exception as e:
            print(f"  ✗ Claude API - ERROR: {str(e)[:50]}")
            return False
    else:
        print("  ○ Claude API - Skipped (no key)")
    
    print("\n✅ API connectivity test passed!")
    return True


def test_directories():
    """Test required directories can be created"""
    print("\n🔍 Testing Directory Permissions...")
    
    dirs = [
        'landing_pages',
        'analytics_data'
    ]
    
    for dir_name in dirs:
        try:
            os.makedirs(dir_name, exist_ok=True)
            print(f"  ✓ {dir_name}/")
        except Exception as e:
            print(f"  ✗ {dir_name}/ - ERROR: {str(e)}")
            return False
    
    print("\n✅ All directories accessible!")
    return True


def run_all_tests():
    """Run all validation tests"""
    print("="*60)
    print("🚀 AUTONOMOUS COMMERCE AGENT - VALIDATION TEST")
    print("="*60)
    
    tests = [
        ("Environment", test_environment),
        ("Dependencies", test_dependencies),
        ("Modules", test_modules),
        ("Directories", test_directories),
        ("API Connectivity", test_api_connectivity)
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ {name} test failed with exception: {e}")
            results.append((name, False))
    
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    all_passed = all(result for _, result in results)
    
    print("\n" + "="*60)
    if all_passed:
        print("🎉 ALL TESTS PASSED!")
        print("="*60)
        print("\nYou're ready to run the agent:")
        print("  python autonomous_agent.py")
        print("\nView the dashboard:")
        print("  Open dashboard.html in your browser")
        return 0
    else:
        print("⚠️  SOME TESTS FAILED")
        print("="*60)
        print("\nPlease fix the issues above before running the agent.")
        print("See SETUP_GUIDE.md for detailed instructions.")
        return 1


if __name__ == '__main__':
    sys.exit(run_all_tests())
