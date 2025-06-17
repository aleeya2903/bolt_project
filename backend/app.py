from flask import Flask, jsonify, request
from flask_cors import CORS
from reddit_scraper import RedditRantScraper, FallbackRantScraper
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

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'scraper_type': 'live' if use_main_scraper else 'fallback',
        'message': 'Reddit Rant Scraper API is running'
    })

@app.route('/api/setup-info', methods=['GET'])
def setup_info():
    """Provide setup information for the API."""
    return jsonify({
        'using_live_data': use_main_scraper,
        'reddit_api_configured': bool(os.getenv('REDDIT_CLIENT_ID') and os.getenv('REDDIT_CLIENT_SECRET')),
        'setup_instructions': {
            'step1': 'Go to https://www.reddit.com/prefs/apps',
            'step2': 'Click "Create App" or "Create Another App"',
            'step3': 'Choose "script" for the app type',
            'step4': 'Copy the client ID and secret to your .env file',
            'step5': 'Restart the server'
        } if not use_main_scraper else None
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001) 