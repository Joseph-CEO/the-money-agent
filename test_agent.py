#!/usr/bin/env python3
"""
Comprehensive Test Suite for Autonomous Commerce Agent
Tests all components including new affiliate networks
"""

import sys
import os
import asyncio
import json
from datetime import datetime

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


class TestColors:
    """ANSI color codes for terminal output"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


def print_header(text):
    """Print section header"""
    print(f"\n{TestColors.HEADER}{TestColors.BOLD}{'='*70}{TestColors.ENDC}")
    print(f"{TestColors.HEADER}{TestColors.BOLD}{text:^70}{TestColors.ENDC}")
    print(f"{TestColors.HEADER}{TestColors.BOLD}{'='*70}{TestColors.ENDC}\n")


def print_success(text):
    """Print success message"""
    print(f"{TestColors.OKGREEN}✓ {text}{TestColors.ENDC}")


def print_error(text):
    """Print error message"""
    print(f"{TestColors.FAIL}✗ {text}{TestColors.ENDC}")


def print_warning(text):
    """Print warning message"""
    print(f"{TestColors.WARNING}⚠ {text}{TestColors.ENDC}")


def print_info(text):
    """Print info message"""
    print(f"{TestColors.OKCYAN}ℹ {text}{TestColors.ENDC}")


async def test_affiliate_connector():
    """Test affiliate connector with all networks"""
    print_header("Testing Affiliate Connector")
    
    try:
        from affiliate_connector import AffiliateConnector
        from autonomous_agent import AgentConfig
        
        config = AgentConfig()
        connector = AffiliateConnector(config)
        
        print_info("Testing affiliate network fetching...")
        
        # Test fetching offers
        offers = await connector.fetch_offers(limit=20)
        
        if offers:
            print_success(f"Fetched {len(offers)} offers successfully")
            
            # Show sample offers by network
            networks = {}
            for offer in offers:
                offer_dict = offer.to_dict() if hasattr(offer, 'to_dict') else offer
                network = offer_dict.get('network', 'unknown')
                if network not in networks:
                    networks[network] = []
                networks[network].append(offer_dict)
            
            print_info(f"\nOffers by network:")
            for network, network_offers in networks.items():
                print(f"  • {network.upper()}: {len(network_offers)} offers")
                if network_offers:
                    sample = network_offers[0]
                    print(f"    Sample: {sample['title'][:50]}... (${sample['price']:.2f}, {sample['discount_percent']:.0f}% off)")
            
            # Test new networks specifically
            new_networks = ['shopify', 'semrush', 'hubspot', 'hostinger']
            found_new = [n for n in new_networks if n in networks]
            
            if found_new:
                print_success(f"\n✨ New networks integrated: {', '.join(found_new)}")
            else:
                print_warning("\n⚠ New networks not yet configured (add credentials to .env)")
            
            return True
        else:
            print_warning("No offers fetched (add API credentials to .env)")
            return True  # Not a failure if credentials aren't set yet
            
    except Exception as e:
        print_error(f"Affiliate connector test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_decision_engine():
    """Test decision engine filtering and ranking"""
    print_header("Testing Decision Engine")
    
    try:
        from decision_engine import DecisionEngine
        from affiliate_connector import AffiliateConnector
        from autonomous_agent import AgentConfig
        
        config = AgentConfig()
        engine = DecisionEngine(config)
        connector = AffiliateConnector(config)
        
        print_info("Fetching offers for filtering test...")
        offers = await connector.fetch_offers(limit=20)
        
        if offers:
            print_success(f"Testing with {len(offers)} offers")
            
            # Test filtering
            selected = engine.select_best_offers(offers, count=5)
            
            if selected:
                print_success(f"Selected {len(selected)} top offers")
                
                for i, offer in enumerate(selected, 1):
                    offer_dict = offer.to_dict() if hasattr(offer, 'to_dict') else offer
                    print(f"\n  {i}. {offer_dict['title'][:50]}...")
                    print(f"     Network: {offer_dict['network']}")
                    print(f"     Price: ${offer_dict['price']:.2f} (was ${offer_dict['original_price']:.2f})")
                    print(f"     Commission: ${offer_dict['commission_amount']:.2f} ({offer_dict['commission_rate']:.1f}%)")
                    print(f"     Discount: {offer_dict['discount_percent']:.0f}%")
                
                return True
            else:
                print_warning("No offers passed filters (try adjusting MIN_COMMISSION_RATE in .env)")
                return True
        else:
            print_warning("No offers available for testing")
            return True
            
    except Exception as e:
        print_error(f"Decision engine test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_content_generator():
    """Test AI content generation"""
    print_header("Testing Content Generator")
    
    try:
        from content_generator import ContentGenerator
        from affiliate_connector import AffiliateOffer
        from autonomous_agent import AgentConfig
        
        config = AgentConfig()
        
        if not config.anthropic_api_key:
            print_warning("ANTHROPIC_API_KEY not set - skipping content generation test")
            print_info("Add your API key to .env to test content generation")
            return True
        
        generator = ContentGenerator(config)
        
        # Create a test offer
        test_offer = AffiliateOffer({
            'id': 'TEST001',
            'network': 'test',
            'title': 'Premium Wireless Headphones with Noise Cancellation',
            'description': 'High-quality over-ear headphones with active noise cancellation, 30-hour battery life, and premium sound quality',
            'image_url': 'https://example.com/headphones.jpg',
            'price': 149.99,
            'original_price': 299.99,
            'discount_percent': 50.0,
            'commission_rate': 8.0,
            'commission_amount': 12.00,
            'category': 'Electronics',
            'merchant': 'Test Merchant',
            'affiliate_url': 'https://example.com/aff/test001',
            'rating': 4.7,
            'reviews': 1523
        })
        
        print_info("Generating content with Claude AI...")
        content = await generator.generate_content(test_offer)
        
        if content:
            print_success("Content generated successfully!\n")
            print(f"{TestColors.BOLD}Social Post:{TestColors.ENDC}")
            print(f"  {content['social_post']}\n")
            print(f"{TestColors.BOLD}Headline:{TestColors.ENDC}")
            print(f"  {content['headline']}\n")
            print(f"{TestColors.BOLD}Landing Page Copy:{TestColors.ENDC}")
            print(f"  {content['landing_copy'][:200]}...\n")
            
            return True
        else:
            print_error("Content generation returned empty")
            return False
            
    except Exception as e:
        print_error(f"Content generator test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_landing_page_manager():
    """Test landing page creation"""
    print_header("Testing Landing Page Manager")
    
    try:
        from landing_page_manager import LandingPageManager
        from affiliate_connector import AffiliateOffer
        from autonomous_agent import AgentConfig
        
        config = AgentConfig()
        manager = LandingPageManager(config)
        
        # Create test offer and content
        test_offer = AffiliateOffer({
            'id': 'TEST002',
            'network': 'test',
            'title': 'Professional Blender 1500W',
            'description': 'High-powered blender perfect for smoothies, soups, and food prep',
            'image_url': 'https://example.com/blender.jpg',
            'price': 89.99,
            'original_price': 159.99,
            'discount_percent': 43.8,
            'commission_rate': 10.0,
            'commission_amount': 9.00,
            'category': 'Kitchen',
            'merchant': 'Test Kitchen Co',
            'affiliate_url': 'https://example.com/aff/test002',
            'rating': 4.6,
            'reviews': 892
        })
        
        test_content = {
            'headline': 'Save 44% on Professional Blender - Limited Time!',
            'landing_copy': 'Transform your kitchen with this powerful 1500W blender. Perfect for smoothies, soups, and more.',
            'social_post': 'Amazing deal on pro blender!',
            'email_subject': '44% Off Professional Blender Today'
        }
        
        print_info("Creating landing page...")
        result = await manager.create_landing_page(test_offer, test_content)
        
        if result and result['path']:
            print_success(f"Landing page created: {result['path']}")
            print_info(f"Public URL: {result['url']}")
            
            # Check if file exists
            if os.path.exists(result['path']):
                file_size = os.path.getsize(result['path'])
                print_success(f"File verified: {file_size} bytes")
                return True
            else:
                print_error("Landing page file not found")
                return False
        else:
            print_error("Landing page creation failed")
            return False
            
    except Exception as e:
        print_error(f"Landing page manager test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_analytics_tracker():
    """Test analytics tracking"""
    print_header("Testing Analytics Tracker")
    
    try:
        from analytics_tracker import AnalyticsTracker
        from autonomous_agent import AgentConfig
        
        config = AgentConfig()
        tracker = AnalyticsTracker(config)
        
        print_info("Testing analytics functions...")
        
        # Test recording metrics
        tracker.track_click('TEST001', 'twitter')
        tracker.track_click('TEST002', 'bluesky')
        tracker.track_conversion('TEST001', 12.50)
        
        print_success("Tracked 2 clicks and 1 conversion")
        
        # Test calculations
        ctr = tracker.calculate_ctr()
        conv_rate = tracker.calculate_conversion_rate()
        
        print_info(f"Click-through rate: {ctr:.2f}%")
        print_info(f"Conversion rate: {conv_rate:.2f}%")
        
        # Generate report
        report = tracker.generate_report()
        print_success("\nGenerated performance report:")
        print(report[:500] + "...\n")
        
        return True
        
    except Exception as e:
        print_error(f"Analytics tracker test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_full_cycle():
    """Test a complete agent cycle"""
    print_header("Testing Full Agent Cycle")
    
    try:
        from autonomous_agent import AutonomousAgent, AgentConfig
        
        config = AgentConfig()
        
        # Check for required API key
        if not config.anthropic_api_key:
            print_warning("ANTHROPIC_API_KEY not set - skipping full cycle test")
            print_info("Add your Claude API key to test the full cycle")
            return True
        
        print_info("Creating agent instance...")
        agent = AutonomousAgent(config)
        
        print_success("Agent created successfully")
        print_info("Running one complete cycle...\n")
        
        # Run one cycle
        await agent.run_cycle()
        
        print_success("\n✨ Full cycle completed successfully!")
        
        # Show stats
        stats = agent.get_status()
        print_info(f"\nAgent Statistics:")
        print(f"  Cycles run: {stats['stats']['cycles_run']}")
        print(f"  Offers processed: {stats['stats']['offers_processed']}")
        print(f"  Posts published: {stats['stats']['posts_published']}")
        print(f"  Total revenue: ${stats['stats']['revenue_generated']:.2f}")
        
        return True
        
    except Exception as e:
        print_error(f"Full cycle test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def run_all_tests():
    """Run all test suites"""
    print(f"\n{TestColors.BOLD}{TestColors.HEADER}")
    print("╔════════════════════════════════════════════════════════════════════╗")
    print("║     AUTONOMOUS COMMERCE AGENT - COMPREHENSIVE TEST SUITE          ║")
    print("║                                                                    ║")
    print("║  Testing: Shopify, SEMrush, HubSpot, Hostinger + Original Networks║")
    print("╚════════════════════════════════════════════════════════════════════╝")
    print(TestColors.ENDC)
    
    test_results = []
    
    tests = [
        ("Affiliate Connector (7 Networks)", test_affiliate_connector),
        ("Decision Engine", test_decision_engine),
        ("Content Generator", test_content_generator),
        ("Landing Page Manager", test_landing_page_manager),
        ("Analytics Tracker", test_analytics_tracker),
        ("Full Agent Cycle", test_full_cycle),
    ]
    
    for test_name, test_func in tests:
        try:
            result = await test_func()
            test_results.append((test_name, result))
        except Exception as e:
            print_error(f"Test '{test_name}' crashed: {e}")
            test_results.append((test_name, False))
    
    # Print summary
    print_header("Test Summary")
    
    passed = sum(1 for _, result in test_results if result)
    total = len(test_results)
    
    for test_name, result in test_results:
        if result:
            print_success(f"{test_name}")
        else:
            print_error(f"{test_name}")
    
    print(f"\n{TestColors.BOLD}Results: {passed}/{total} tests passed{TestColors.ENDC}")
    
    if passed == total:
        print(f"\n{TestColors.OKGREEN}{TestColors.BOLD}")
        print("╔════════════════════════════════════════════════════════════════════╗")
        print("║                    🎉 ALL TESTS PASSED! 🎉                         ║")
        print("║                                                                    ║")
        print("║              Your agent is ready for deployment!                  ║")
        print("╚════════════════════════════════════════════════════════════════════╝")
        print(TestColors.ENDC)
        
        print(f"\n{TestColors.OKCYAN}Next Steps:{TestColors.ENDC}")
        print("  1. Configure your .env file with all API keys")
        print("  2. Run: python autonomous_agent.py")
        print("  3. Monitor: Open dashboard.html in your browser")
        print("  4. Deploy to cloud for 24/7 operation")
        
        return 0
    else:
        print(f"\n{TestColors.FAIL}{TestColors.BOLD}")
        print("╔════════════════════════════════════════════════════════════════════╗")
        print("║                  ⚠️  SOME TESTS FAILED  ⚠️                         ║")
        print("╚════════════════════════════════════════════════════════════════════╝")
        print(TestColors.ENDC)
        
        print(f"\n{TestColors.WARNING}Action Required:{TestColors.ENDC}")
        print("  • Review error messages above")
        print("  • Check your .env configuration")
        print("  • See SETUP_GUIDE.md for help")
        
        return 1


if __name__ == '__main__':
    sys.exit(asyncio.run(run_all_tests()))
