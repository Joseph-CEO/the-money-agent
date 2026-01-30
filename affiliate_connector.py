"""
Affiliate Connector - Integrates with multiple affiliate networks
Supports: Amazon Product Advertising API, CJ Affiliate, Impact
"""

import aiohttp
import hashlib
import hmac
import base64
from datetime import datetime
from typing import List, Dict, Optional
import logging
from urllib.parse import quote

logger = logging.getLogger(__name__)


class AffiliateOffer:
    """Standardized offer format across all networks"""
    def __init__(self, data: Dict):
        self.id = data.get('id')
        self.network = data.get('network')  # 'amazon', 'cj', 'impact'
        self.title = data.get('title')
        self.description = data.get('description')
        self.image_url = data.get('image_url')
        self.price = data.get('price', 0.0)
        self.original_price = data.get('original_price', 0.0)
        self.discount_percent = data.get('discount_percent', 0.0)
        self.commission_rate = data.get('commission_rate', 0.0)
        self.commission_amount = data.get('commission_amount', 0.0)
        self.category = data.get('category', 'General')
        self.merchant = data.get('merchant', '')
        self.affiliate_url = data.get('affiliate_url')
        self.deep_link = data.get('deep_link')
        self.rating = data.get('rating', 0.0)
        self.reviews = data.get('reviews', 0)
        
    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'network': self.network,
            'title': self.title,
            'description': self.description,
            'image_url': self.image_url,
            'price': self.price,
            'original_price': self.original_price,
            'discount_percent': self.discount_percent,
            'commission_rate': self.commission_rate,
            'commission_amount': self.commission_amount,
            'category': self.category,
            'merchant': self.merchant,
            'affiliate_url': self.affiliate_url,
            'rating': self.rating,
            'reviews': self.reviews
        }


class AffiliateConnector:
    """Connects to multiple affiliate networks and fetches offers"""
    
    def __init__(self, config):
        self.config = config
        self.session = None
    
    async def fetch_offers(self, limit: int = 20) -> List[AffiliateOffer]:
        """Fetch offers from all configured networks"""
        all_offers = []
        
        async with aiohttp.ClientSession() as session:
            self.session = session
            
            # Fetch from each network in parallel
            tasks = []
            per_network_limit = max(3, limit // 7)  # Divide among 7 networks
            
            if self.config.amazon_access_key:
                tasks.append(self._fetch_amazon_offers(per_network_limit))
            
            if self.config.cj_api_key:
                tasks.append(self._fetch_cj_offers(per_network_limit))
            
            if self.config.impact_api_key:
                tasks.append(self._fetch_impact_offers(per_network_limit))
            
            # New networks
            if hasattr(self.config, 'shopify_partner_id') and self.config.shopify_partner_id:
                tasks.append(self._fetch_shopify_offers(per_network_limit))
            
            if hasattr(self.config, 'semrush_affiliate_id') and self.config.semrush_affiliate_id:
                tasks.append(self._fetch_semrush_offers(per_network_limit))
            
            if hasattr(self.config, 'hubspot_affiliate_code') and self.config.hubspot_affiliate_code:
                tasks.append(self._fetch_hubspot_offers(per_network_limit))
            
            if hasattr(self.config, 'hostinger_affiliate_id') and self.config.hostinger_affiliate_id:
                tasks.append(self._fetch_hostinger_offers(per_network_limit))
            
            # Execute all fetches concurrently
            import asyncio
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for result in results:
                if isinstance(result, Exception):
                    logger.error(f"Error fetching offers: {result}")
                else:
                    all_offers.extend(result)
        
        logger.info(f"Fetched {len(all_offers)} total offers from all networks")
        return all_offers[:limit]
    
    async def _fetch_amazon_offers(self, limit: int) -> List[AffiliateOffer]:
        """Fetch offers from Amazon Product Advertising API"""
        try:
            # Amazon PA API 5.0 requires complex signing
            # This is a simplified example - use boto3 or paapi5-python-sdk in production
            
            # For MVP, we'll simulate with popular deal categories
            offers = []
            
            # Example: Search for deals in popular categories
            keywords = [
                'electronics deals',
                'home kitchen deals',
                'books bestsellers',
                'fashion deals',
                'toys deals'
            ]
            
            # In production, use actual Amazon PA API:
            # from paapi5_python_sdk.api.default_api import DefaultApi
            # from paapi5_python_sdk.search_items_request import SearchItemsRequest
            
            logger.info(f"Amazon API integration ready (using mock data for demo)")
            
            # Mock data for demonstration
            mock_offers = [
                {
                    'id': 'AMZN001',
                    'network': 'amazon',
                    'title': 'Wireless Noise Cancelling Headphones',
                    'description': 'Premium over-ear headphones with active noise cancellation',
                    'image_url': 'https://example.com/headphones.jpg',
                    'price': 149.99,
                    'original_price': 249.99,
                    'discount_percent': 40.0,
                    'commission_rate': 4.0,
                    'commission_amount': 6.00,
                    'category': 'Electronics',
                    'merchant': 'Amazon',
                    'affiliate_url': f'https://amazon.com/dp/MOCKSKU?tag={self.config.amazon_partner_tag}',
                    'rating': 4.5,
                    'reviews': 1250
                },
                {
                    'id': 'AMZN002',
                    'network': 'amazon',
                    'title': 'Smart Home Security Camera System',
                    'description': '4-camera wireless security system with night vision',
                    'image_url': 'https://example.com/camera.jpg',
                    'price': 199.99,
                    'original_price': 349.99,
                    'discount_percent': 42.9,
                    'commission_rate': 8.0,
                    'commission_amount': 16.00,
                    'category': 'Smart Home',
                    'merchant': 'Amazon',
                    'affiliate_url': f'https://amazon.com/dp/MOCKSKU2?tag={self.config.amazon_partner_tag}',
                    'rating': 4.7,
                    'reviews': 892
                }
            ]
            
            for offer_data in mock_offers[:limit]:
                offers.append(AffiliateOffer(offer_data))
            
            return offers
            
        except Exception as e:
            logger.error(f"Error fetching Amazon offers: {e}")
            return []
    
    async def _fetch_cj_offers(self, limit: int) -> List[AffiliateOffer]:
        """Fetch offers from CJ Affiliate (Commission Junction)"""
        try:
            # CJ API endpoint
            url = "https://product-search.api.cj.com/v2/product-search"
            
            headers = {
                'Authorization': f'Bearer {self.config.cj_api_key}',
                'Accept': 'application/json'
            }
            
            params = {
                'website-id': 'YOUR_WEBSITE_ID',  # Set via config
                'advertiser-ids': 'joined',
                'serviceable-area': 'US',
                'currency': 'USD',
                'records-per-page': limit,
                'page-number': 1
            }
            
            # For demo purposes, using mock data
            # In production, uncomment the actual API call:
            # async with self.session.get(url, headers=headers, params=params) as response:
            #     data = await response.json()
            #     return self._parse_cj_response(data)
            
            logger.info(f"CJ API integration ready (using mock data for demo)")
            
            mock_offers = [
                {
                    'id': 'CJ001',
                    'network': 'cj',
                    'title': 'Professional Blender 1500W',
                    'description': 'High-powered blender for smoothies and food prep',
                    'image_url': 'https://example.com/blender.jpg',
                    'price': 89.99,
                    'original_price': 159.99,
                    'discount_percent': 43.8,
                    'commission_rate': 10.0,
                    'commission_amount': 9.00,
                    'category': 'Kitchen',
                    'merchant': 'Kitchen Pro',
                    'affiliate_url': 'https://www.anrdoezrs.net/click-XXXXX-YYYYY',
                    'rating': 4.6,
                    'reviews': 543
                }
            ]
            
            return [AffiliateOffer(d) for d in mock_offers[:limit]]
            
        except Exception as e:
            logger.error(f"Error fetching CJ offers: {e}")
            return []
    
    async def _fetch_impact_offers(self, limit: int) -> List[AffiliateOffer]:
        """Fetch offers from Impact Affiliate Network"""
        try:
            # Impact API endpoint
            url = "https://api.impact.com/Mediapartners/YOUR_ACCOUNT_SID/Catalogs/Items"
            
            headers = {
                'Authorization': f'Bearer {self.config.impact_api_key}',
                'Accept': 'application/json'
            }
            
            params = {
                'PageSize': limit
            }
            
            logger.info(f"Impact API integration ready (using mock data for demo)")
            
            # Mock data for demonstration
            mock_offers = [
                {
                    'id': 'IMP001',
                    'network': 'impact',
                    'title': 'Fitness Tracker Watch',
                    'description': 'Track steps, heart rate, sleep and calories',
                    'image_url': 'https://example.com/fitness.jpg',
                    'price': 79.99,
                    'original_price': 129.99,
                    'discount_percent': 38.5,
                    'commission_rate': 12.0,
                    'commission_amount': 9.60,
                    'category': 'Fitness',
                    'merchant': 'FitGear',
                    'affiliate_url': 'https://impact.com/campaign/XXXXX/click',
                    'rating': 4.4,
                    'reviews': 721
                }
            ]
            
            return [AffiliateOffer(d) for d in mock_offers[:limit]]
            
        except Exception as e:
            logger.error(f"Error fetching Impact offers: {e}")
            return []
    
    def _parse_cj_response(self, data: Dict) -> List[AffiliateOffer]:
        """Parse CJ API response into standardized offers"""
        offers = []
        # Parse CJ-specific response format
        return offers
    
    def _parse_impact_response(self, data: Dict) -> List[AffiliateOffer]:
        """Parse Impact API response into standardized offers"""
        offers = []
        # Parse Impact-specific response format
        return offers
    
    async def _fetch_shopify_offers(self, limit: int) -> List[AffiliateOffer]:
        """Fetch offers from Shopify Partner Program"""
        try:
            # Shopify Partner Program offers recurring commissions
            # API: https://shopify.dev/api/partner
            
            logger.info(f"Shopify Partner integration ready (using mock data for demo)")
            
            # Mock offers - Shopify pays 200% of first two months or $2000 per Plus referral
            mock_offers = [
                {
                    'id': 'SHOPIFY001',
                    'network': 'shopify',
                    'title': 'Shopify - Start Your Online Store',
                    'description': 'Build your ecommerce business with Shopify. 14-day free trial, no credit card required.',
                    'image_url': 'https://cdn.shopify.com/shopifycloud/brochure/assets/brand-assets/shopify-logo.png',
                    'price': 29.00,  # Basic plan monthly
                    'original_price': 0.00,  # Free trial
                    'discount_percent': 100.0,  # Free trial
                    'commission_rate': 200.0,  # 200% of first 2 months
                    'commission_amount': 58.00,  # 2 months at $29
                    'category': 'Ecommerce',
                    'merchant': 'Shopify',
                    'affiliate_url': f'https://shopify.pxf.io/c/{self.config.shopify_partner_id if hasattr(self.config, "shopify_partner_id") else "XXXXX"}/affiliate-link',
                    'rating': 4.8,
                    'reviews': 89543
                },
                {
                    'id': 'SHOPIFY002',
                    'network': 'shopify',
                    'title': 'Shopify Plus - Enterprise Ecommerce',
                    'description': 'Scale your business with Shopify Plus. Enterprise-grade features and support.',
                    'image_url': 'https://cdn.shopify.com/shopifycloud/brochure/assets/brand-assets/shopify-plus-logo.png',
                    'price': 2000.00,  # Plus starting price
                    'original_price': 2000.00,
                    'discount_percent': 0.0,
                    'commission_rate': 100.0,  # $2000 flat per Plus referral
                    'commission_amount': 2000.00,
                    'category': 'Ecommerce',
                    'merchant': 'Shopify',
                    'affiliate_url': f'https://shopify.pxf.io/c/{self.config.shopify_partner_id if hasattr(self.config, "shopify_partner_id") else "XXXXX"}/plus',
                    'rating': 4.9,
                    'reviews': 12890
                }
            ]
            
            return [AffiliateOffer(d) for d in mock_offers[:limit]]
            
        except Exception as e:
            logger.error(f"Error fetching Shopify offers: {e}")
            return []
    
    async def _fetch_semrush_offers(self, limit: int) -> List[AffiliateOffer]:
        """Fetch offers from SEMrush Affiliate Program"""
        try:
            # SEMrush BeRush affiliate program
            # Pays $200 per new subscription + 10% recurring
            # https://www.semrush.com/partners/affiliates/
            
            logger.info(f"SEMrush affiliate integration ready (using mock data for demo)")
            
            mock_offers = [
                {
                    'id': 'SEMRUSH001',
                    'network': 'semrush',
                    'title': 'SEMrush Pro - SEO & Marketing Tool',
                    'description': 'All-in-one SEO toolkit. Keyword research, competitor analysis, site audit, and more.',
                    'image_url': 'https://static.semrush.com/common/semrush-logo.svg',
                    'price': 119.95,
                    'original_price': 129.95,
                    'discount_percent': 7.7,
                    'commission_rate': 40.0,  # $200 flat + 10% recurring (represented as 40% for first month)
                    'commission_amount': 200.00,  # Flat $200 for new subscription
                    'category': 'Marketing',
                    'merchant': 'SEMrush',
                    'affiliate_url': f'https://www.semrush.com/?ref={self.config.semrush_affiliate_id if hasattr(self.config, "semrush_affiliate_id") else "XXXXX"}',
                    'rating': 4.6,
                    'reviews': 5432
                },
                {
                    'id': 'SEMRUSH002',
                    'network': 'semrush',
                    'title': 'SEMrush Guru - Advanced Marketing Suite',
                    'description': 'Advanced SEO tools with historical data, extended limits, and content marketing toolkit.',
                    'image_url': 'https://static.semrush.com/common/semrush-logo.svg',
                    'price': 229.95,
                    'original_price': 249.95,
                    'discount_percent': 8.0,
                    'commission_rate': 40.0,
                    'commission_amount': 200.00,
                    'category': 'Marketing',
                    'merchant': 'SEMrush',
                    'affiliate_url': f'https://www.semrush.com/prices/?ref={self.config.semrush_affiliate_id if hasattr(self.config, "semrush_affiliate_id") else "XXXXX"}',
                    'rating': 4.7,
                    'reviews': 3821
                }
            ]
            
            return [AffiliateOffer(d) for d in mock_offers[:limit]]
            
        except Exception as e:
            logger.error(f"Error fetching SEMrush offers: {e}")
            return []
    
    async def _fetch_hubspot_offers(self, limit: int) -> List[AffiliateOffer]:
        """Fetch offers from HubSpot Affiliate Program"""
        try:
            # HubSpot pays 30% recurring for first year (up to 12 months)
            # https://www.hubspot.com/partners/affiliates
            
            logger.info(f"HubSpot affiliate integration ready (using mock data for demo)")
            
            mock_offers = [
                {
                    'id': 'HUBSPOT001',
                    'network': 'hubspot',
                    'title': 'HubSpot CRM - Free Forever',
                    'description': 'Free CRM software for growing businesses. Contact management, deals, tasks, and more.',
                    'image_url': 'https://www.hubspot.com/hubfs/HubSpot_Logos/HubSpot-Inversed-Favicon.png',
                    'price': 0.00,
                    'original_price': 0.00,
                    'discount_percent': 0.0,
                    'commission_rate': 100.0,  # Lead gen bonus
                    'commission_amount': 15.00,  # $15 per qualified signup
                    'category': 'CRM',
                    'merchant': 'HubSpot',
                    'affiliate_url': f'https://www.hubspot.com/products/crm?hubs_signup-cta=getstarted-crm&hubs_signup-url=www.hubspot.com%2Fproducts%2Fcrm&ref={self.config.hubspot_affiliate_code if hasattr(self.config, "hubspot_affiliate_code") else "XXXXX"}',
                    'rating': 4.5,
                    'reviews': 8923
                },
                {
                    'id': 'HUBSPOT002',
                    'network': 'hubspot',
                    'title': 'HubSpot Marketing Hub - Professional',
                    'description': 'Advanced marketing automation, analytics, and reporting. Grow your business faster.',
                    'image_url': 'https://www.hubspot.com/hubfs/HubSpot_Logos/HubSpot-Inversed-Favicon.png',
                    'price': 800.00,
                    'original_price': 890.00,
                    'discount_percent': 10.1,
                    'commission_rate': 30.0,  # 30% recurring for 12 months
                    'commission_amount': 240.00,  # 30% of $800
                    'category': 'Marketing',
                    'merchant': 'HubSpot',
                    'affiliate_url': f'https://www.hubspot.com/products/marketing?ref={self.config.hubspot_affiliate_code if hasattr(self.config, "hubspot_affiliate_code") else "XXXXX"}',
                    'rating': 4.4,
                    'reviews': 6211
                },
                {
                    'id': 'HUBSPOT003',
                    'network': 'hubspot',
                    'title': 'HubSpot Sales Hub - Professional',
                    'description': 'Sales automation, pipeline management, and productivity tools for sales teams.',
                    'image_url': 'https://www.hubspot.com/hubfs/HubSpot_Logos/HubSpot-Inversed-Favicon.png',
                    'price': 450.00,
                    'original_price': 500.00,
                    'discount_percent': 10.0,
                    'commission_rate': 30.0,
                    'commission_amount': 135.00,
                    'category': 'CRM',
                    'merchant': 'HubSpot',
                    'affiliate_url': f'https://www.hubspot.com/products/sales?ref={self.config.hubspot_affiliate_code if hasattr(self.config, "hubspot_affiliate_code") else "XXXXX"}',
                    'rating': 4.6,
                    'reviews': 5109
                }
            ]
            
            return [AffiliateOffer(d) for d in mock_offers[:limit]]
            
        except Exception as e:
            logger.error(f"Error fetching HubSpot offers: {e}")
            return []
    
    async def _fetch_hostinger_offers(self, limit: int) -> List[AffiliateOffer]:
        """Fetch offers from Hostinger Affiliate Program"""
        try:
            # Hostinger pays 60% commission per sale
            # https://www.hostinger.com/affiliates
            
            logger.info(f"Hostinger affiliate integration ready (using mock data for demo)")
            
            mock_offers = [
                {
                    'id': 'HOSTINGER001',
                    'network': 'hostinger',
                    'title': 'Hostinger Premium Web Hosting - 75% OFF',
                    'description': 'Fast, secure web hosting with free domain, SSL, and daily backups. Perfect for WordPress.',
                    'image_url': 'https://www.hostinger.com/h-assets/images/logo-new.svg',
                    'price': 2.99,  # Monthly with discount
                    'original_price': 11.99,
                    'discount_percent': 75.0,
                    'commission_rate': 60.0,  # 60% commission
                    'commission_amount': 21.48,  # 60% of 12 months at $2.99
                    'category': 'Hosting',
                    'merchant': 'Hostinger',
                    'affiliate_url': f'https://www.hostinger.com/web-hosting?ref={self.config.hostinger_affiliate_id if hasattr(self.config, "hostinger_affiliate_id") else "XXXXX"}',
                    'rating': 4.7,
                    'reviews': 12453
                },
                {
                    'id': 'HOSTINGER002',
                    'network': 'hostinger',
                    'title': 'Hostinger VPS Hosting - Up to 73% OFF',
                    'description': 'High-performance VPS hosting with dedicated resources, root access, and full control.',
                    'image_url': 'https://www.hostinger.com/h-assets/images/logo-new.svg',
                    'price': 4.99,
                    'original_price': 18.99,
                    'discount_percent': 73.7,
                    'commission_rate': 60.0,
                    'commission_amount': 35.93,  # 60% of 12 months
                    'category': 'Hosting',
                    'merchant': 'Hostinger',
                    'affiliate_url': f'https://www.hostinger.com/vps-hosting?ref={self.config.hostinger_affiliate_id if hasattr(self.config, "hostinger_affiliate_id") else "XXXXX"}',
                    'rating': 4.8,
                    'reviews': 8921
                },
                {
                    'id': 'HOSTINGER003',
                    'network': 'hostinger',
                    'title': 'Hostinger Cloud Hosting - Save 70%',
                    'description': 'Blazing-fast cloud hosting with 99.99% uptime, auto-scaling, and premium performance.',
                    'image_url': 'https://www.hostinger.com/h-assets/images/logo-new.svg',
                    'price': 9.99,
                    'original_price': 33.99,
                    'discount_percent': 70.6,
                    'commission_rate': 60.0,
                    'commission_amount': 71.93,  # 60% of 12 months
                    'category': 'Hosting',
                    'merchant': 'Hostinger',
                    'affiliate_url': f'https://www.hostinger.com/cloud-hosting?ref={self.config.hostinger_affiliate_id if hasattr(self.config, "hostinger_affiliate_id") else "XXXXX"}',
                    'rating': 4.8,
                    'reviews': 6234
                }
            ]
            
            return [AffiliateOffer(d) for d in mock_offers[:limit]]
            
        except Exception as e:
            logger.error(f"Error fetching Hostinger offers: {e}")
            return []
