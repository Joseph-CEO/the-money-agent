"""
Content Generator - Creates engaging marketing content using Claude AI
Generates social posts, headlines, descriptions, and landing page copy
"""

import aiohttp
import json
import logging
from typing import Dict, List
from datetime import datetime

logger = logging.getLogger(__name__)


class ContentGenerator:
    """AI-powered content generation for affiliate marketing"""
    
    def __init__(self, config):
        self.config = config
        self.api_url = "https://api.anthropic.com/v1/messages"
    
    async def generate_content(self, offer) -> Dict:
        """Generate all marketing content for an offer"""
        
        offer_dict = offer.to_dict() if hasattr(offer, 'to_dict') else offer
        
        # Generate multiple content variations
        social_post = await self._generate_social_post(offer_dict)
        headline = await self._generate_headline(offer_dict)
        landing_copy = await self._generate_landing_page_copy(offer_dict)
        email_subject = await self._generate_email_subject(offer_dict)
        
        return {
            'offer_id': offer_dict['id'],
            'social_post': social_post,
            'headline': headline,
            'landing_copy': landing_copy,
            'email_subject': email_subject,
            'image_url': offer_dict['image_url'],
            'affiliate_url': offer_dict['affiliate_url'],
            'generated_at': datetime.now().isoformat()
        }
    
    async def _generate_social_post(self, offer: Dict) -> str:
        """Generate engaging social media post"""
        
        discount = int(offer['discount_percent'])
        price = offer['price']
        title = offer['title']
        
        prompt = f"""Create a short, engaging social media post (Twitter/X style) for this product deal:

Product: {title}
Original Price: ${offer['original_price']:.2f}
Sale Price: ${price:.2f}
Discount: {discount}% off
Rating: {offer.get('rating', 'N/A')} stars ({offer.get('reviews', 0)} reviews)

Requirements:
- Maximum 240 characters (leave room for link)
- Start with an attention-grabbing hook
- Highlight the discount and key benefit
- Create urgency
- Use 1-2 relevant emojis
- Don't use hashtags
- Be enthusiastic but authentic
- Don't say "click the link" or "link in bio"

Write ONLY the post text, nothing else."""

        try:
            content = await self._call_claude_api(prompt, max_tokens=150)
            
            # Ensure FTC compliance
            content += "\n\n#ad"
            
            return content.strip()
            
        except Exception as e:
            logger.error(f"Error generating social post: {e}")
            # Fallback template
            return f"🔥 {discount}% OFF: {title[:80]}... Now ${price:.2f}! ⭐ {offer.get('rating', 0)}/5 stars #ad"
    
    async def _generate_headline(self, offer: Dict) -> str:
        """Generate compelling headline for landing page"""
        
        prompt = f"""Create a compelling headline for this product deal:

Product: {offer['title']}
Discount: {int(offer['discount_percent'])}% off
Price: ${offer['price']:.2f}

Requirements:
- 8-12 words maximum
- Focus on the benefit and savings
- Create urgency or excitement
- Use power words
- No clickbait

Write ONLY the headline, nothing else."""

        try:
            headline = await self._call_claude_api(prompt, max_tokens=50)
            return headline.strip()
        except Exception as e:
            logger.error(f"Error generating headline: {e}")
            return f"Save {int(offer['discount_percent'])}% on {offer['title'][:50]}"
    
    async def _generate_landing_page_copy(self, offer: Dict) -> str:
        """Generate landing page body copy"""
        
        prompt = f"""Write persuasive landing page copy for this product:

Product: {offer['title']}
Description: {offer['description']}
Regular Price: ${offer['original_price']:.2f}
Sale Price: ${offer['price']:.2f}
Discount: {int(offer['discount_percent'])}% OFF
Rating: {offer.get('rating', 0)}/5 stars
Reviews: {offer.get('reviews', 0)}

Structure:
1. Opening hook (1-2 sentences about the problem/desire)
2. Product benefits (3-4 bullet points)
3. Social proof mention
4. Urgency/scarcity element
5. Clear call-to-action

Keep it concise (150-200 words). Be persuasive but honest. Don't make health claims."""

        try:
            copy = await self._call_claude_api(prompt, max_tokens=400)
            
            # Add affiliate disclosure
            disclosure = "\n\n---\n*Disclosure: This page contains affiliate links. We may earn a commission from purchases made through these links at no extra cost to you.*"
            
            return copy.strip() + disclosure
            
        except Exception as e:
            logger.error(f"Error generating landing copy: {e}")
            return f"{offer['description']}\n\n**Special Price: ${offer['price']:.2f}** (Save {int(offer['discount_percent'])}%)\n\n{offer.get('reviews', 0)} verified reviews. Don't miss this deal!"
    
    async def _generate_email_subject(self, offer: Dict) -> str:
        """Generate email subject line"""
        
        prompt = f"""Create an email subject line for this deal:

Product: {offer['title']}
Discount: {int(offer['discount_percent'])}% off

Requirements:
- 6-8 words
- Create curiosity and urgency
- Mention discount percentage
- No spam words (Free, !!!, Act Now)

Write ONLY the subject line, nothing else."""

        try:
            subject = await self._call_claude_api(prompt, max_tokens=40)
            return subject.strip()
        except Exception as e:
            logger.error(f"Error generating email subject: {e}")
            return f"{int(offer['discount_percent'])}% Off {offer['title'][:40]}"
    
    async def _call_claude_api(self, prompt: str, max_tokens: int = 300) -> str:
        """Call Claude API for content generation"""
        
        headers = {
            "x-api-key": self.config.anthropic_api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        
        payload = {
            "model": "claude-sonnet-4-20250514",
            "max_tokens": max_tokens,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(self.api_url, headers=headers, json=payload) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"API error {response.status}: {error_text}")
                
                data = await response.json()
                content = data['content'][0]['text']
                return content
    
    def create_utm_link(self, affiliate_url: str, source: str, medium: str, campaign: str) -> str:
        """Add UTM parameters for tracking"""
        separator = '&' if '?' in affiliate_url else '?'
        utm_params = f"utm_source={source}&utm_medium={medium}&utm_campaign={campaign}"
        return f"{affiliate_url}{separator}{utm_params}"
