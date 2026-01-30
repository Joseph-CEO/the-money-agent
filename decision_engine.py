"""
Decision Engine - Filters and ranks affiliate offers
Uses rules and ML signals to select the most profitable offers
"""

import logging
from typing import List, Dict
from datetime import datetime

logger = logging.getLogger(__name__)


class DecisionEngine:
    """Intelligent offer selection based on profit potential"""
    
    def __init__(self, config):
        self.config = config
        self.performance_history = {}  # Track which types of offers perform best
    
    def select_best_offers(self, offers: List, count: int = 2) -> List:
        """Filter and rank offers, return top N"""
        
        # Step 1: Apply hard filters
        filtered = self._apply_filters(offers)
        logger.info(f"After filtering: {len(filtered)} offers remain")
        
        if not filtered:
            return []
        
        # Step 2: Score and rank offers
        scored = self._score_offers(filtered)
        
        # Step 3: Select top N diverse offers
        selected = self._select_diverse(scored, count)
        
        logger.info(f"Selected {len(selected)} offers for promotion")
        return selected
    
    def _apply_filters(self, offers: List) -> List:
        """Apply business rules to filter offers"""
        filtered = []
        
        for offer in offers:
            # Convert to dict if needed
            offer_dict = offer.to_dict() if hasattr(offer, 'to_dict') else offer
            
            # Filter 1: Minimum commission rate
            if offer_dict['commission_rate'] < self.config.min_commission_rate:
                continue
            
            # Filter 2: Minimum discount
            if offer_dict['discount_percent'] < self.config.min_discount_percent:
                continue
            
            # Filter 3: Price range
            if offer_dict['price'] < self.config.min_price or offer_dict['price'] > self.config.max_price:
                continue
            
            # Filter 4: Must have image
            if not offer_dict.get('image_url'):
                continue
            
            # Filter 5: Must have valid affiliate URL
            if not offer_dict.get('affiliate_url'):
                continue
            
            # Filter 6: Quality score (rating and reviews)
            if offer_dict.get('rating', 0) < 4.0 or offer_dict.get('reviews', 0) < 50:
                continue
            
            filtered.append(offer)
        
        return filtered
    
    def _score_offers(self, offers: List) -> List[Dict]:
        """Score each offer based on profit potential"""
        scored = []
        
        for offer in offers:
            offer_dict = offer.to_dict() if hasattr(offer, 'to_dict') else offer
            
            score = 0.0
            
            # Score component 1: Expected commission (40% weight)
            commission_score = offer_dict['commission_amount'] * 0.4
            score += commission_score
            
            # Score component 2: Discount appeal (25% weight)
            # Higher discounts are more attractive to customers
            discount_score = (offer_dict['discount_percent'] / 100) * 25
            score += discount_score
            
            # Score component 3: Social proof (20% weight)
            # Rating and review count indicate quality
            rating_score = (offer_dict.get('rating', 0) / 5.0) * 10
            review_score = min(offer_dict.get('reviews', 0) / 1000, 1.0) * 10
            score += rating_score + review_score
            
            # Score component 4: Price point appeal (15% weight)
            # Mid-range prices ($50-$200) tend to convert best
            price = offer_dict['price']
            if 50 <= price <= 200:
                price_score = 15
            elif 20 <= price < 50 or 200 < price <= 350:
                price_score = 10
            else:
                price_score = 5
            score += price_score
            
            # Bonus: Trending categories
            trending_categories = ['Electronics', 'Smart Home', 'Fitness', 'Kitchen']
            if offer_dict.get('category') in trending_categories:
                score *= 1.1  # 10% boost
            
            # Historical performance boost
            offer_id = offer_dict['id']
            if offer_id in self.performance_history:
                historical_ctr = self.performance_history[offer_id].get('ctr', 0)
                score *= (1 + historical_ctr)  # Boost by historical CTR
            
            scored.append({
                'offer': offer,
                'score': score,
                'components': {
                    'commission': commission_score,
                    'discount': discount_score,
                    'social_proof': rating_score + review_score,
                    'price_appeal': price_score
                }
            })
        
        # Sort by score descending
        scored.sort(key=lambda x: x['score'], reverse=True)
        
        return scored
    
    def _select_diverse(self, scored: List[Dict], count: int) -> List:
        """Select top N offers while maintaining diversity"""
        selected = []
        categories_used = set()
        networks_used = {}
        
        for item in scored:
            if len(selected) >= count:
                break
            
            offer = item['offer']
            offer_dict = offer.to_dict() if hasattr(offer, 'to_dict') else offer
            
            category = offer_dict.get('category', 'General')
            network = offer_dict.get('network', 'unknown')
            
            # Try to diversify by category
            if len(selected) < count - 1:
                # For first N-1 selections, prefer different categories
                if category in categories_used:
                    continue
            
            # Limit offers from same network
            if networks_used.get(network, 0) >= count // 2:
                continue
            
            selected.append(offer)
            categories_used.add(category)
            networks_used[network] = networks_used.get(network, 0) + 1
            
            logger.info(
                f"Selected: {offer_dict['title'][:50]}... "
                f"(Score: {item['score']:.2f}, "
                f"Commission: ${offer_dict['commission_amount']:.2f})"
            )
        
        # If we couldn't get enough diverse offers, fill with top scorers
        if len(selected) < count:
            for item in scored:
                if len(selected) >= count:
                    break
                offer = item['offer']
                if offer not in selected:
                    selected.append(offer)
        
        return selected
    
    def update_performance(self, offer_id: str, metrics: Dict):
        """Update historical performance data"""
        if offer_id not in self.performance_history:
            self.performance_history[offer_id] = {
                'impressions': 0,
                'clicks': 0,
                'conversions': 0,
                'revenue': 0.0,
                'ctr': 0.0,
                'conversion_rate': 0.0
            }
        
        history = self.performance_history[offer_id]
        history['impressions'] += metrics.get('impressions', 0)
        history['clicks'] += metrics.get('clicks', 0)
        history['conversions'] += metrics.get('conversions', 0)
        history['revenue'] += metrics.get('revenue', 0.0)
        
        # Calculate rates
        if history['impressions'] > 0:
            history['ctr'] = history['clicks'] / history['impressions']
        if history['clicks'] > 0:
            history['conversion_rate'] = history['conversions'] / history['clicks']
        
        logger.info(f"Updated performance for {offer_id}: CTR={history['ctr']:.3f}")
