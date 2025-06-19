"""
Cache Manager for Reddit Rant Roulette
Pre-generates and caches rant-poem pairs for instant serving
"""
import threading
import time
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from collections import deque
import random
import logging

from reddit_scraper import RedditRantScraper, FallbackRantScraper
from aiPoem import convert_rant_to_poem_mistral_new

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RantPoemCache:
    """
    High-performance cache system for rant-poem pairs
    Features:
    - Pre-generates content in background
    - Maintains hot cache of ready-to-serve pairs
    - Intelligent cache warming
    - Graceful fallbacks
    """
    
    def __init__(self, target_cache_size=20, min_cache_size=5):
        self.target_cache_size = target_cache_size
        self.min_cache_size = min_cache_size
        
        # Thread-safe cache storage
        self._cache_lock = threading.RLock()
        self._hot_cache = deque(maxlen=target_cache_size)  # Ready-to-serve items
        self._generating = False  # Flag to prevent multiple background jobs
        
        # Statistics
        self.stats = {
            'cache_hits': 0,
            'cache_misses': 0,
            'generation_attempts': 0,
            'generation_successes': 0,
            'generation_failures': 0,
            'last_generated': None,
            'cache_size': 0
        }
        
        # Initialize scrapers
        try:
            if os.getenv('REDDIT_CLIENT_ID') and os.getenv('REDDIT_CLIENT_SECRET'):
                self.scraper = RedditRantScraper()
                self.using_live_data = True
                logger.info("✅ Using live Reddit data for cache")
            else:
                self.scraper = FallbackRantScraper()
                self.using_live_data = False
                logger.info("⚠️ Using fallback data for cache")
        except Exception as e:
            logger.error(f"❌ Error initializing scraper: {e}")
            self.scraper = FallbackRantScraper()
            self.using_live_data = False
        
        # Background worker thread
        self._worker_thread = None
        self._stop_worker = threading.Event()
        
        # Start the background cache warming
        self.start_background_worker()
        
        # Initial cache warm-up (blocking)
        self._initial_warmup()
    
    def _initial_warmup(self):
        """Initial synchronous cache warming to ensure we have some content"""
        logger.info("🔥 Starting initial cache warm-up...")
        
        # Generate a few items synchronously for immediate availability
        warmup_items = min(3, self.min_cache_size)
        for i in range(warmup_items):
            try:
                item = self._generate_single_item()
                if item:
                    with self._cache_lock:
                        self._hot_cache.append(item)
                    logger.info(f"✅ Initial warm-up item {i+1}/{warmup_items} generated")
                else:
                    logger.warning(f"⚠️ Failed to generate initial warm-up item {i+1}")
            except Exception as e:
                logger.error(f"❌ Error during initial warm-up: {e}")
        
        logger.info(f"🎯 Initial warm-up complete. Cache size: {len(self._hot_cache)}")
    
    def get_cached_rant_poem(self) -> Optional[Dict]:
        """
        Get a pre-generated rant-poem pair instantly
        Returns None if cache is empty
        """
        with self._cache_lock:
            if self._hot_cache:
                item = self._hot_cache.popleft()
                self.stats['cache_hits'] += 1
                self.stats['cache_size'] = len(self._hot_cache)
                
                logger.info(f"🚀 Cache hit! Serving instant result. Remaining: {len(self._hot_cache)}")
                
                # Trigger background refill if cache is getting low
                if len(self._hot_cache) < self.min_cache_size:
                    self._trigger_background_generation()
                
                return item
            else:
                self.stats['cache_misses'] += 1
                logger.warning("💔 Cache miss! No pre-generated content available")
                return None
    
    def _generate_single_item(self) -> Optional[Dict]:
        """Generate a single rant-poem pair"""
        try:
            self.stats['generation_attempts'] += 1
            
            # Get a rant
            rant = self.scraper.get_random_rant()
            if not rant:
                logger.warning("⚠️ No rant available from scraper")
                return None
            
            # Generate poem with timeout and retry logic
            full_rant_text = f"{rant['title']}. {rant['content']}"
            
            # Check if AI is available
            if os.getenv('HF_TOKEN'):
                try:
                    poem = convert_rant_to_poem_mistral_new(full_rant_text)
                    
                    # Check if AI generation actually worked
                    if poem.startswith("Error:") or poem.startswith("The muses are silent") or poem.startswith("The poet's ink ran dry"):
                        logger.warning(f"⚠️ AI generation failed: {poem[:50]}...")
                        poem = self._generate_fallback_poem(full_rant_text)
                        is_ai = False
                    else:
                        is_ai = True
                        logger.info("🤖 AI poem generated successfully")
                except Exception as e:
                    logger.error(f"❌ AI generation error: {e}")
                    poem = self._generate_fallback_poem(full_rant_text)
                    is_ai = False
            else:
                poem = self._generate_fallback_poem(full_rant_text)
                is_ai = False
            
            # Create the cached item
            cached_item = {
                'rant': rant,
                'poem': poem,
                'is_ai': is_ai,
                'generated_at': datetime.now().isoformat(),
                'using_live_data': self.using_live_data
            }
            
            self.stats['generation_successes'] += 1
            self.stats['last_generated'] = datetime.now().isoformat()
            
            return cached_item
            
        except Exception as e:
            logger.error(f"❌ Error generating cache item: {e}")
            self.stats['generation_failures'] += 1
            return None
    
    def _generate_fallback_poem(self, rant_text: str) -> str:
        """Generate a simple template-based poem as fallback"""
        emotion_words = ['angry', 'frustrated', 'annoying', 'hate', 'love', 'beautiful']
        found_emotions = [word for word in emotion_words if word in rant_text.lower()]
        
        poem_templates = [
            f"""Oh world of frustration and endless dismay,
Where {found_emotions[0] if found_emotions else 'anger'} rules both night and day,
Let patience flow like a gentle stream,
And turn your {found_emotions[1] if len(found_emotions) > 1 else 'frustration'} into a peaceful dream.""",
            
            f"""In the realm where complaints do dwell,
Your passionate words ring like a bell,
Though {found_emotions[0] if found_emotions else 'irritation'} may cloud your sight,
Beauty emerges when we shed some light.""",
            
            f"""From depths of {found_emotions[0] if found_emotions else 'annoyance'} comes this tale,
Where ordinary moments often fail,
But in your words, though fierce they may be,
Lies poetry for all the world to see."""
        ]
        
        return random.choice(poem_templates)
    
    def _background_worker(self):
        """Background thread that continuously fills the cache"""
        logger.info("🔄 Background cache worker started")
        
        while not self._stop_worker.is_set():
            try:
                # Check if we need to generate more items
                with self._cache_lock:
                    current_size = len(self._hot_cache)
                
                if current_size < self.target_cache_size:
                    logger.info(f"🎯 Cache below target ({current_size}/{self.target_cache_size}), generating new item...")
                    
                    item = self._generate_single_item()
                    if item:
                        with self._cache_lock:
                            self._hot_cache.append(item)
                        logger.info(f"✅ Added item to cache. New size: {len(self._hot_cache)}")
                    else:
                        logger.warning("⚠️ Failed to generate cache item")
                
                # Sleep before next generation attempt
                # Longer sleep if cache is full, shorter if cache is low
                if current_size >= self.target_cache_size:
                    sleep_time = 30  # 30 seconds when cache is full
                elif current_size < self.min_cache_size:
                    sleep_time = 5   # 5 seconds when cache is critically low
                else:
                    sleep_time = 15  # 15 seconds when cache is moderate
                
                self._stop_worker.wait(sleep_time)
                
            except Exception as e:
                logger.error(f"❌ Background worker error: {e}")
                self._stop_worker.wait(10)  # Wait 10s on error
        
        logger.info("🔄 Background cache worker stopped")
    
    def _trigger_background_generation(self):
        """Trigger background generation if not already running"""
        if not self._generating:
            self._generating = True
            logger.info("🚀 Triggered background cache generation")
            # The background worker will pick this up automatically
    
    def start_background_worker(self):
        """Start the background cache worker thread"""
        if self._worker_thread and self._worker_thread.is_alive():
            return
        
        self._stop_worker.clear()
        self._worker_thread = threading.Thread(target=self._background_worker, daemon=True)
        self._worker_thread.start()
        logger.info("🔄 Background cache worker started")
    
    def stop_background_worker(self):
        """Stop the background cache worker thread"""
        if self._worker_thread and self._worker_thread.is_alive():
            self._stop_worker.set()
            self._worker_thread.join(timeout=5)
            logger.info("🔄 Background cache worker stopped")
    
    def get_cache_stats(self) -> Dict:
        """Get cache statistics"""
        with self._cache_lock:
            self.stats['cache_size'] = len(self._hot_cache)
        
        return self.stats.copy()
    
    def warm_cache(self, count: int = None) -> int:
        """Manually warm the cache with specified number of items"""
        if count is None:
            count = self.target_cache_size
        
        logger.info(f"🔥 Manual cache warming: generating {count} items...")
        
        generated = 0
        for i in range(count):
            item = self._generate_single_item()
            if item:
                with self._cache_lock:
                    self._hot_cache.append(item)
                generated += 1
                logger.info(f"✅ Generated cache item {i+1}/{count}")
            else:
                logger.warning(f"⚠️ Failed to generate cache item {i+1}/{count}")
        
        logger.info(f"🎯 Cache warming complete: {generated}/{count} items generated")
        return generated
    
    def clear_cache(self):
        """Clear all cached items"""
        with self._cache_lock:
            self._hot_cache.clear()
        logger.info("🗑️ Cache cleared")
    
    def __del__(self):
        """Cleanup when cache manager is destroyed"""
        self.stop_background_worker()

# Global cache instance
_cache_instance = None

def get_cache_manager() -> RantPoemCache:
    """Get the global cache manager instance"""
    global _cache_instance
    if _cache_instance is None:
        _cache_instance = RantPoemCache()
    return _cache_instance

def initialize_cache(target_size=20, min_size=5):
    """Initialize the global cache with specific parameters"""
    global _cache_instance
    if _cache_instance is not None:
        _cache_instance.stop_background_worker()
    
    _cache_instance = RantPoemCache(target_size, min_size)
    return _cache_instance

if __name__ == "__main__":
    # Test the cache system
    print("🧪 Testing Cache Manager")
    print("=" * 50)
    
    cache = RantPoemCache(target_cache_size=5, min_cache_size=2)
    
    # Test getting cached items
    for i in range(10):
        print(f"\n🎯 Test {i+1}: Getting cached item...")
        item = cache.get_cached_rant_poem()
        
        if item:
            print(f"✅ Got cached item!")
            print(f"   - Title: {item['rant']['title'][:50]}...")
            print(f"   - AI Generated: {item['is_ai']}")
            print(f"   - Generated at: {item['generated_at']}")
        else:
            print("❌ No cached item available")
        
        # Wait a bit between requests
        time.sleep(2)
    
    # Print final stats
    print(f"\n📊 Final Cache Stats:")
    stats = cache.get_cache_stats()
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    cache.stop_background_worker()
    print("\n🎯 Cache test complete!") 