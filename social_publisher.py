"""
Social Publisher - Posts content to multiple social media platforms
Supports: Twitter/X, TikTok, Bluesky, Instagram, Telegram
"""

import aiohttp
import logging
from typing import Dict, List
from datetime import datetime
import json

logger = logging.getLogger(__name__)


class SocialPublisher:
    """Publish content to multiple social platforms"""
    
    def __init__(self, config):
        self.config = config
        self.platforms_enabled = self._detect_enabled_platforms()
    
    def _detect_enabled_platforms(self) -> List[str]:
        """Detect which platforms have valid API credentials"""
        enabled = []
        
        if self.config.twitter_api_key and self.config.twitter_api_secret:
            enabled.append('twitter')
        
        # Add other platforms as credentials are configured
        # if self.config.tiktok_api_key:
        #     enabled.append('tiktok')
        # if self.config.bluesky_handle:
        #     enabled.append('bluesky')
        
        logger.info(f"Enabled social platforms: {enabled}")
        return enabled
    
    async def publish(self, content: Dict) -> bool:
        """Publish content to all enabled platforms"""
        success = False
        
        for platform in self.platforms_enabled:
            try:
                if platform == 'twitter':
                    await self._publish_to_twitter(content)
                    success = True
                elif platform == 'tiktok':
                    await self._publish_to_tiktok(content)
                    success = True
                elif platform == 'bluesky':
                    await self._publish_to_bluesky(content)
                    success = True
                elif platform == 'telegram':
                    await self._publish_to_telegram(content)
                    success = True
                
            except Exception as e:
                logger.error(f"Error publishing to {platform}: {e}")
        
        return success
    
    async def _publish_to_twitter(self, content: Dict):
        """Publish to Twitter/X using API v2"""
        
        # Twitter API v2 endpoint
        url = "https://api.twitter.com/2/tweets"
        
        # Create the tweet text with link
        tweet_text = content['social_post']
        
        # Add landing page URL
        landing_url = content.get('landing_url', content['affiliate_url'])
        tweet_text += f"\n\n{landing_url}"
        
        payload = {
            "text": tweet_text
        }
        
        # OAuth 1.0a is required for Twitter API
        # For production, use tweepy or python-twitter library
        # This is a simplified example
        
        logger.info(f"Would publish to Twitter: {tweet_text[:100]}...")
        
        # Mock successful post for demo
        # In production, uncomment actual API call:
        """
        import tweepy
        
        client = tweepy.Client(
            consumer_key=self.config.twitter_api_key,
            consumer_secret=self.config.twitter_api_secret,
            access_token=self.config.twitter_access_token,
            access_token_secret=self.config.twitter_access_secret
        )
        
        response = client.create_tweet(text=tweet_text)
        logger.info(f"Published to Twitter: {response.data['id']}")
        """
        
        return True
    
    async def _publish_to_tiktok(self, content: Dict):
        """Publish to TikTok (requires video content)"""
        
        # TikTok Content Posting API
        # Note: TikTok primarily supports video content
        # For affiliate marketing, consider using TikTok Shop Creator API
        
        logger.info("TikTok publishing requires video content - skipping for text-based deals")
        
        # Alternative: Post to TikTok Shop if integrated
        # https://developers.tiktok.com/doc/content-posting-api-get-started
        
        return False
    
    async def _publish_to_bluesky(self, content: Dict):
        """Publish to Bluesky using AT Protocol"""
        
        # Bluesky uses AT Protocol
        url = "https://bsky.social/xrpc/com.atproto.repo.createRecord"
        
        post_text = content['social_post']
        landing_url = content.get('landing_url', content['affiliate_url'])
        
        # Bluesky post format
        record = {
            "repo": "YOUR_BLUESKY_HANDLE.bsky.social",  # Set via config
            "collection": "app.bsky.feed.post",
            "record": {
                "text": f"{post_text}\n\n{landing_url}",
                "createdAt": datetime.now().isoformat(),
                "$type": "app.bsky.feed.post"
            }
        }
        
        logger.info(f"Would publish to Bluesky: {post_text[:100]}...")
        
        # In production, use actual API call with auth
        # Requires session token from authentication
        
        return True
    
    async def _publish_to_telegram(self, content: Dict):
        """Publish to Telegram channel"""
        
        # Telegram Bot API
        bot_token = self.config.telegram_bot_token if hasattr(self.config, 'telegram_bot_token') else None
        channel_id = self.config.telegram_channel_id if hasattr(self.config, 'telegram_channel_id') else None
        
        if not bot_token or not channel_id:
            logger.info("Telegram credentials not configured")
            return False
        
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        
        post_text = content['social_post']
        landing_url = content.get('landing_url', content['affiliate_url'])
        
        payload = {
            "chat_id": channel_id,
            "text": f"{post_text}\n\n{landing_url}",
            "parse_mode": "HTML",
            "disable_web_page_preview": False
        }
        
        logger.info(f"Would publish to Telegram: {post_text[:100]}...")
        
        # In production, uncomment:
        """
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as response:
                if response.status == 200:
                    logger.info("Published to Telegram successfully")
                    return True
                else:
                    error = await response.text()
                    logger.error(f"Telegram error: {error}")
                    return False
        """
        
        return True
    
    async def _publish_to_instagram(self, content: Dict):
        """Publish to Instagram (requires media)"""
        
        # Instagram Graph API
        # Requires Facebook Page and Instagram Business Account
        # Only supports photo/video posts, not text-only
        
        logger.info("Instagram publishing requires image/video content")
        
        # For affiliate links, use link in bio or Instagram Shopping
        # https://developers.facebook.com/docs/instagram-api/guides/content-publishing
        
        return False
    
    def get_best_posting_times(self) -> List[int]:
        """Get optimal posting hours based on platform analytics"""
        
        # Based on general social media research:
        # - Twitter/X: 8-10am, 12-1pm, 5-6pm
        # - Facebook: 1-4pm
        # - Instagram: 11am-1pm
        
        # Return hours in 24h format
        return [8, 9, 12, 13, 17, 18]
    
    def should_post_now(self) -> bool:
        """Check if current time is optimal for posting"""
        current_hour = datetime.now().hour
        return current_hour in self.get_best_posting_times()
