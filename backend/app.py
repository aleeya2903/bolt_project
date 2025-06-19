from flask import Flask, jsonify, request
from flask_cors import CORS
from reddit_scraper import RedditRantScraper, FallbackRantScraper
from aiPoem import convert_rant_to_poem_mistral_new
from cache_manager import get_cache_manager, initialize_cache
import os
import time
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize cache system for high performance
print("🚀 Initializing high-performance cache system...")
cache_manager = initialize_cache(target_size=20, min_size=5)
print("✅ Cache system ready!")

# Initialize scrapers (fallback for non-cached requests)
try:
    # Try to initialize the main scraper
    if os.getenv('REDDIT_CLIENT_ID') and os.getenv('REDDIT_CLIENT_SECRET'):
        scraper = RedditRantScraper()
        use_main_scraper = True
        print("Using Reddit API scraper for fallback")
    else:
        scraper = FallbackRantScraper()
        use_main_scraper = False
        print("Using fallback scraper for non-cached requests")
except Exception as e:
    print(f"Error initializing main scraper: {e}")
    scraper = FallbackRantScraper()
    use_main_scraper = False
    print("Using fallback scraper")

@app.route('/api/rant', methods=['GET'])
def get_random_rant():
    """Get a single random rant."""
    try:
        rant = scraper.get_random_rant()
        if rant:
            return jsonify({
                'success': True,
                'rant': rant,
                'using_live_data': use_main_scraper
            })
        else:
            return jsonify({
                'success': False,
                'error': 'No rant found',
                'using_live_data': use_main_scraper
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'using_live_data': use_main_scraper
        }), 500

@app.route('/api/rants', methods=['GET'])
def get_multiple_rants():
    """Get multiple rants."""
    try:
        count = request.args.get('count', 5, type=int)
        count = min(max(count, 1), 10)  # Limit between 1 and 10
        
        rants = scraper.get_multiple_rants(count)
        
        return jsonify({
            'success': True,
            'rants': rants,
            'count': len(rants),
            'using_live_data': use_main_scraper
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'using_live_data': use_main_scraper
        }), 500

@app.route('/api/poem', methods=['POST'])
def generate_poem():
    """Generate a poem from a rant text."""
    try:
        data = request.get_json()
        
        if not data or 'rant_text' not in data:
            return jsonify({
                'success': False,
                'error': 'rant_text is required in request body'
            }), 400
        
        rant_text = data['rant_text']
        
        if not rant_text.strip():
            return jsonify({
                'success': False,
                'error': 'rant_text cannot be empty'
            }), 400
        
        # Generate the poem using the AI
        poem = convert_rant_to_poem_mistral_new(rant_text)
        
        # Check if there was an error in poem generation
        if poem.startswith("Error:") or poem.startswith("The muses are silent") or poem.startswith("The poet's ink ran dry"):
            return jsonify({
                'success': False,
                'error': poem
            }), 500
        
        return jsonify({
            'success': True,
            'original_rant': rant_text,
            'poem': poem
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Internal server error: {str(e)}'
        }), 500

@app.route('/api/rant-and-poem', methods=['GET'])
def get_rant_and_poem():
    """Get a random rant and generate a poem from it - CACHED VERSION for instant performance!"""
    start_time = time.time()
    
    try:
        # Try to get from cache first for instant response!
        cached_item = cache_manager.get_cached_rant_poem()
        
        if cached_item:
            # INSTANT RESPONSE from cache! 🚀
            response_time = (time.time() - start_time) * 1000
            
            return jsonify({
                'success': True,
                'rant': cached_item['rant'],
                'poem': cached_item['poem'],
                'is_ai': cached_item['is_ai'],
                'using_live_data': cached_item['using_live_data'],
                'cached': True,
                'response_time_ms': round(response_time, 2),
                'generated_at': cached_item['generated_at']
            })
        
        else:
            # Cache miss - generate on-demand (slower fallback)
            print("⚠️ Cache miss - generating on-demand")
            
            # First get a random rant
            rant = scraper.get_random_rant()
            if not rant:
                return jsonify({
                    'success': False,
                    'error': 'No rant found',
                    'using_live_data': use_main_scraper,
                    'cached': False
                }), 404
            
            # Combine title and content for the poem generation
            full_rant_text = f"{rant['title']}. {rant['content']}"
            
            # Generate the poem
            poem = convert_rant_to_poem_mistral_new(full_rant_text)
            is_ai = True
            
            # Check if there was an error in poem generation
            if poem.startswith("Error:") or poem.startswith("The muses are silent") or poem.startswith("The poet's ink ran dry"):
                # Use fallback poem generation
                emotion_words = ['angry', 'frustrated', 'annoying', 'hate', 'love', 'beautiful']
                found_emotions = [word for word in emotion_words if word in full_rant_text.lower()]
                
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
                
                import random
                poem = random.choice(poem_templates)
                is_ai = False
            
            response_time = (time.time() - start_time) * 1000
            
            return jsonify({
                'success': True,
                'rant': rant,
                'poem': poem,
                'is_ai': is_ai,
                'using_live_data': use_main_scraper,
                'cached': False,
                'response_time_ms': round(response_time, 2)
            })
        
    except Exception as e:
        response_time = (time.time() - start_time) * 1000
        return jsonify({
            'success': False,
            'error': str(e),
            'using_live_data': use_main_scraper,
            'cached': False,
            'response_time_ms': round(response_time, 2)
        }), 500

@app.route('/api/rant-and-poem-fast', methods=['GET'])
def get_rant_and_poem_fast():
    """
    ULTRA-FAST endpoint - only serves cached content for guaranteed instant response
    Returns 503 if no cached content available
    """
    start_time = time.time()
    
    cached_item = cache_manager.get_cached_rant_poem()
    
    if cached_item:
        response_time = (time.time() - start_time) * 1000
        
        return jsonify({
            'success': True,
            'rant': cached_item['rant'],
            'poem': cached_item['poem'],
            'is_ai': cached_item['is_ai'],
            'using_live_data': cached_item['using_live_data'],
            'cached': True,
            'response_time_ms': round(response_time, 2),
            'generated_at': cached_item['generated_at']
        })
    else:
        return jsonify({
            'success': False,
            'error': 'No cached content available. Please try the regular endpoint.',
            'cached': False,
            'response_time_ms': round((time.time() - start_time) * 1000, 2)
        }), 503

@app.route('/api/cache/stats', methods=['GET'])
def get_cache_stats():
    """Get cache performance statistics"""
    try:
        stats = cache_manager.get_cache_stats()
        
        # Calculate cache hit ratio
        total_requests = stats['cache_hits'] + stats['cache_misses']
        hit_ratio = (stats['cache_hits'] / total_requests * 100) if total_requests > 0 else 0
        
        # Add computed metrics
        stats['hit_ratio_percent'] = round(hit_ratio, 2)
        stats['total_requests'] = total_requests
        
        return jsonify({
            'success': True,
            'cache_stats': stats
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/cache/warm', methods=['POST'])
def warm_cache():
    """Manually warm the cache"""
    try:
        data = request.get_json() or {}
        count = data.get('count', 5)
        count = min(max(count, 1), 20)  # Limit between 1 and 20
        
        generated = cache_manager.warm_cache(count)
        
        return jsonify({
            'success': True,
            'message': f'Cache warming initiated',
            'requested': count,
            'generated': generated
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/cache/clear', methods=['POST'])
def clear_cache():
    """Clear the cache"""
    try:
        cache_manager.clear_cache()
        
        return jsonify({
            'success': True,
            'message': 'Cache cleared successfully'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint with cache information."""
    # Check if HF token is configured
    hf_token_configured = bool(os.getenv('HF_TOKEN'))
    
    # Get cache stats
    cache_stats = cache_manager.get_cache_stats()
    
    return jsonify({
        'status': 'healthy',
        'scraper_type': 'live' if use_main_scraper else 'fallback',
        'ai_poem_configured': hf_token_configured,
        'cache_enabled': True,
        'cache_size': cache_stats['cache_size'],
        'cache_hit_ratio': f"{cache_stats['cache_hits']}/{cache_stats['cache_hits'] + cache_stats['cache_misses']}" if (cache_stats['cache_hits'] + cache_stats['cache_misses']) > 0 else "0/0",
        'message': 'Reddit Rant Scraper API is running with high-performance caching'
    })

@app.route('/api/setup-info', methods=['GET'])
def setup_info():
    """Provide setup information for the API."""
    hf_token_configured = bool(os.getenv('HF_TOKEN'))
    cache_stats = cache_manager.get_cache_stats()
    
    return jsonify({
        'using_live_data': use_main_scraper,
        'reddit_api_configured': bool(os.getenv('REDDIT_CLIENT_ID') and os.getenv('REDDIT_CLIENT_SECRET')),
        'ai_poem_configured': hf_token_configured,
        'cache_system': {
            'enabled': True,
            'current_size': cache_stats['cache_size'],
            'target_size': cache_manager.target_cache_size,
            'hit_ratio': f"{round((cache_stats['cache_hits'] / (cache_stats['cache_hits'] + cache_stats['cache_misses']) * 100), 2)}%" if (cache_stats['cache_hits'] + cache_stats['cache_misses']) > 0 else "N/A"
        },
        'performance_features': [
            '🚀 Pre-generated content cache',
            '⚡ Sub-100ms response times',
            '🔄 Background cache warming',
            '📊 Performance monitoring'
        ],
        'setup_instructions': {
            'reddit': {
                'step1': 'Go to https://www.reddit.com/prefs/apps',
                'step2': 'Click "Create App" or "Create Another App"',
                'step3': 'Choose "script" for the app type',
                'step4': 'Copy the client ID and secret to your .env file',
                'step5': 'Restart the server'
            } if not use_main_scraper else None,
            'huggingface': {
                'step1': 'Go to https://huggingface.co/settings/tokens',
                'step2': 'Create a new token with "Read" permissions',
                'step3': 'Add HF_TOKEN=your_token_here to your .env file',
                'step4': 'Restart the server'
            } if not hf_token_configured else None
        }
    })

if __name__ == '__main__':
    print("🎭 Starting Reddit Rant Roulette with High-Performance Caching!")
    print("🚀 Cache system warming up in background...")
    app.run(debug=True, host='0.0.0.0', port=5001) 