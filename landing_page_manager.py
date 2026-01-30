"""
Landing Page Manager - Creates and hosts affiliate landing pages
Generates static HTML pages with tracking and SEO optimization
"""

import os
import logging
from typing import Dict
from datetime import datetime
import hashlib
import json

logger = logging.getLogger(__name__)


class LandingPageManager:
    """Create and manage affiliate landing pages"""
    
    def __init__(self, config):
        self.config = config
        self.pages_dir = "/home/claude/landing_pages"
        self.pages_manifest = {}
        
        # Create pages directory
        os.makedirs(self.pages_dir, exist_ok=True)
    
    async def create_landing_page(self, offer, content: Dict) -> Dict:
        """Create a landing page for an offer"""
        
        offer_dict = offer.to_dict() if hasattr(offer, 'to_dict') else offer
        
        # Generate unique page ID
        page_id = self._generate_page_id(offer_dict)
        page_filename = f"{page_id}.html"
        page_path = os.path.join(self.pages_dir, page_filename)
        
        # Generate HTML content
        html = self._generate_html(offer_dict, content)
        
        # Write to file
        with open(page_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        # Generate public URL
        page_url = f"{self.config.site_url}/deals/{page_filename}"
        
        # Store in manifest
        self.pages_manifest[page_id] = {
            'offer_id': offer_dict['id'],
            'page_url': page_url,
            'created_at': datetime.now().isoformat(),
            'affiliate_url': offer_dict['affiliate_url']
        }
        
        logger.info(f"Created landing page: {page_url}")
        
        return {
            'page_id': page_id,
            'url': page_url,
            'path': page_path
        }
    
    def _generate_page_id(self, offer: Dict) -> str:
        """Generate unique page ID"""
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        offer_hash = hashlib.md5(offer['id'].encode()).hexdigest()[:8]
        return f"{timestamp}_{offer_hash}"
    
    def _generate_html(self, offer: Dict, content: Dict) -> str:
        """Generate complete HTML landing page"""
        
        # Extract content
        headline = content.get('headline', offer['title'])
        body_copy = content.get('landing_copy', offer['description'])
        affiliate_url = offer['affiliate_url']
        
        # Add UTM tracking
        tracked_url = self._add_tracking(affiliate_url, offer['id'])
        
        # Generate HTML
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{headline}</title>
    <meta name="description" content="{offer['description'][:160]}">
    
    <!-- Open Graph / Social Media -->
    <meta property="og:title" content="{headline}">
    <meta property="og:description" content="{offer['description'][:200]}">
    <meta property="og:image" content="{offer['image_url']}">
    <meta property="og:type" content="product">
    
    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{headline}">
    <meta name="twitter:description" content="{offer['description'][:200]}">
    <meta name="twitter:image" content="{offer['image_url']}">
    
    <!-- Google Analytics -->
    {self._get_analytics_code()}
    
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
        }}
        
        .container {{
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background: white;
            min-height: 100vh;
        }}
        
        .header {{
            text-align: center;
            margin-bottom: 30px;
            padding: 20px 0;
        }}
        
        .deal-badge {{
            display: inline-block;
            background: #ff4444;
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            font-weight: bold;
            margin-bottom: 15px;
            font-size: 14px;
        }}
        
        h1 {{
            font-size: 2em;
            margin-bottom: 10px;
            color: #1a1a1a;
        }}
        
        .product-image {{
            width: 100%;
            max-width: 500px;
            height: auto;
            border-radius: 8px;
            margin: 20px auto;
            display: block;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        
        .price-section {{
            text-align: center;
            margin: 30px 0;
            padding: 20px;
            background: #f9f9f9;
            border-radius: 8px;
        }}
        
        .original-price {{
            text-decoration: line-through;
            color: #999;
            font-size: 1.2em;
            margin-right: 10px;
        }}
        
        .sale-price {{
            color: #ff4444;
            font-size: 2em;
            font-weight: bold;
        }}
        
        .savings {{
            color: #00aa00;
            font-size: 1.2em;
            margin-top: 10px;
        }}
        
        .rating {{
            text-align: center;
            margin: 15px 0;
            font-size: 1.1em;
        }}
        
        .stars {{
            color: #ffa500;
            margin-right: 5px;
        }}
        
        .content {{
            margin: 30px 0;
            line-height: 1.8;
            font-size: 1.05em;
        }}
        
        .cta-button {{
            display: block;
            width: 100%;
            max-width: 400px;
            margin: 30px auto;
            padding: 18px 36px;
            background: #ff4444;
            color: white;
            text-align: center;
            text-decoration: none;
            border-radius: 8px;
            font-size: 1.3em;
            font-weight: bold;
            transition: background 0.3s;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        
        .cta-button:hover {{
            background: #cc0000;
            transform: translateY(-2px);
            box-shadow: 0 6px 8px rgba(0,0,0,0.15);
        }}
        
        .features {{
            margin: 30px 0;
        }}
        
        .features ul {{
            list-style: none;
            padding: 0;
        }}
        
        .features li {{
            padding: 10px 0;
            border-bottom: 1px solid #eee;
        }}
        
        .features li:before {{
            content: "✓ ";
            color: #00aa00;
            font-weight: bold;
            margin-right: 8px;
        }}
        
        .disclosure {{
            margin-top: 40px;
            padding: 20px;
            background: #f0f0f0;
            border-left: 4px solid #ff4444;
            font-size: 0.9em;
            color: #666;
        }}
        
        .urgency {{
            background: #fff3cd;
            border: 2px solid #ffc107;
            padding: 15px;
            border-radius: 8px;
            margin: 20px 0;
            text-align: center;
            font-weight: bold;
        }}
        
        @media (max-width: 600px) {{
            h1 {{
                font-size: 1.5em;
            }}
            
            .sale-price {{
                font-size: 1.5em;
            }}
            
            .container {{
                padding: 10px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="deal-badge">🔥 LIMITED TIME DEAL</div>
            <h1>{headline}</h1>
        </div>
        
        <img src="{offer['image_url']}" alt="{offer['title']}" class="product-image" onerror="this.src='https://via.placeholder.com/500x500?text=Product+Image'">
        
        <div class="price-section">
            <div>
                <span class="original-price">${offer['original_price']:.2f}</span>
                <span class="sale-price">${offer['price']:.2f}</span>
            </div>
            <div class="savings">
                Save {int(offer['discount_percent'])}% (${offer['original_price'] - offer['price']:.2f} OFF)
            </div>
        </div>
        
        <div class="rating">
            <span class="stars">{'⭐' * int(offer.get('rating', 0))}</span>
            {offer.get('rating', 0)}/5.0 ({offer.get('reviews', 0):,} reviews)
        </div>
        
        <div class="urgency">
            ⏰ Deal ends soon! Don't miss out on this exclusive offer
        </div>
        
        <a href="{tracked_url}" class="cta-button" target="_blank" rel="noopener">
            Get This Deal Now →
        </a>
        
        <div class="content">
            {self._format_content(body_copy)}
        </div>
        
        <a href="{tracked_url}" class="cta-button" target="_blank" rel="noopener">
            Claim Your Discount →
        </a>
        
        <div class="disclosure">
            <strong>Disclosure:</strong> This page contains affiliate links. We may earn a commission from purchases made through these links at no additional cost to you. We only recommend products we believe will provide value to our readers.
        </div>
    </div>
    
    <script>
        // Track clicks
        document.querySelectorAll('a[href*="{offer['id']}"]').forEach(link => {{
            link.addEventListener('click', function() {{
                if (typeof gtag !== 'undefined') {{
                    gtag('event', 'click', {{
                        'event_category': 'affiliate',
                        'event_label': '{offer['id']}',
                        'value': {offer['commission_amount']}
                    }});
                }}
            }});
        }});
    </script>
</body>
</html>"""
        
        return html
    
    def _format_content(self, text: str) -> str:
        """Format content text to HTML"""
        # Convert newlines to paragraphs
        paragraphs = text.split('\n\n')
        html_paragraphs = []
        
        for para in paragraphs:
            if para.strip():
                # Check if it's a list
                if para.strip().startswith('-') or para.strip().startswith('•'):
                    items = para.split('\n')
                    html_paragraphs.append('<ul class="features">')
                    for item in items:
                        clean_item = item.strip().lstrip('-•').strip()
                        if clean_item:
                            html_paragraphs.append(f'<li>{clean_item}</li>')
                    html_paragraphs.append('</ul>')
                else:
                    html_paragraphs.append(f'<p>{para.strip()}</p>')
        
        return '\n'.join(html_paragraphs)
    
    def _add_tracking(self, url: str, offer_id: str) -> str:
        """Add UTM tracking parameters"""
        separator = '&' if '?' in url else '?'
        tracking = f"utm_source=dealsite&utm_medium=landing&utm_campaign={offer_id}"
        return f"{url}{separator}{tracking}"
    
    def _get_analytics_code(self) -> str:
        """Get Google Analytics tracking code"""
        if not self.config.google_analytics_id:
            return ""
        
        return f"""
    <!-- Google Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id={self.config.google_analytics_id}"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){{dataLayer.push(arguments);}}
        gtag('js', new Date());
        gtag('config', '{self.config.google_analytics_id}');
    </script>
    """
    
    def save_manifest(self):
        """Save pages manifest to file"""
        manifest_path = os.path.join(self.pages_dir, 'manifest.json')
        with open(manifest_path, 'w') as f:
            json.dump(self.pages_manifest, f, indent=2)
