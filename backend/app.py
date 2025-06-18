from flask import Flask, jsonify, request
from flask_cors import CORS
from reddit_scraper import RedditRantScraper, FallbackRantScraper
from aiPoem import convert_rant_to_poem_mistral_new
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize scrapers
try:
    # Try to initialize the main scraper
    if os.getenv('REDDIT_CLIENT_ID') and os.getenv('REDDIT_CLIENT_SECRET'):
        scraper = RedditRantScraper()
        use_main_scraper = True
        print("Using Reddit API scraper")
    else:
        scraper = FallbackRantScraper()
        use_main_scraper = False
        print("Using fallback scraper - set up Reddit API credentials for live data")
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
    """Get a random rant and generate a poem from it."""
    try:
        # First get a random rant
        rant = scraper.get_random_rant()
        if not rant:
            return jsonify({
                'success': False,
                'error': 'No rant found',
                'using_live_data': use_main_scraper
            }), 404
        
        # Combine title and content for the poem generation
        full_rant_text = f"{rant['title']}. {rant['content']}"
        
        # Generate the poem
        poem = convert_rant_to_poem_mistral_new(full_rant_text)
        
        # Check if there was an error in poem generation
        if poem.startswith("Error:") or poem.startswith("The muses are silent") or poem.startswith("The poet's ink ran dry"):
            # Return rant without poem if AI fails
            return jsonify({
                'success': True,
                'rant': rant,
                'poem': None,
                'poem_error': poem,
                'using_live_data': use_main_scraper
            })
        
        return jsonify({
            'success': True,
            'rant': rant,
            'poem': poem,
            'using_live_data': use_main_scraper
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'using_live_data': use_main_scraper
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    # Check if HF token is configured
    hf_token_configured = bool(os.getenv('HF_TOKEN'))
    
    return jsonify({
        'status': 'healthy',
        'scraper_type': 'live' if use_main_scraper else 'fallback',
        'ai_poem_configured': hf_token_configured,
        'message': 'Reddit Rant Scraper API is running'
    })

@app.route('/api/setup-info', methods=['GET'])
def setup_info():
    """Provide setup information for the API."""
    hf_token_configured = bool(os.getenv('HF_TOKEN'))
    
    return jsonify({
        'using_live_data': use_main_scraper,
        'reddit_api_configured': bool(os.getenv('REDDIT_CLIENT_ID') and os.getenv('REDDIT_CLIENT_SECRET')),
        'ai_poem_configured': hf_token_configured,
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
    app.run(debug=True, host='0.0.0.0', port=5001) 