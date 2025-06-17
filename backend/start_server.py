#!/usr/bin/env python3
"""
Simple server startup script for Reddit Rant Roulette
"""

import os
import sys
from reddit_scraper import RedditRantScraper, FallbackRantScraper

def test_scraper_setup():
    """Test the scraper setup"""
    print("🔍 Testing scraper setup...")
    
    try:
        # Test if we can import and use the scraper
        fallback = FallbackRantScraper()
        rant = fallback.get_random_rant()
        
        print("✅ Scraper working!")
        print(f"   Sample rant: {rant['title']}")
        return True
    except Exception as e:
        print(f"❌ Scraper failed: {e}")
        return False

def start_api_server():
    """Start the Flask API server"""
    print("\n🚀 Starting Reddit Rant API server...")
    
    try:
        from app import app
        print("✅ Flask app imported successfully")
        print("🌐 Starting server on http://localhost:5001")
        print("\n📝 Available endpoints:")
        print("   GET /api/rant - Get a random rant")
        print("   GET /api/rants?count=3 - Get multiple rants")
        print("   GET /api/health - Health check")
        print("   GET /api/setup-info - Setup information")
        
        print("\n🎯 Ready for your frontend integration!")
        print("   Your frontend can fetch rants from: http://localhost:5001/api/rant")
        
        # Start the server
        app.run(debug=True, host='0.0.0.0', port=5001, use_reloader=False)
        
    except Exception as e:
        print(f"❌ Server startup failed: {e}")
        return False

if __name__ == "__main__":
    print("🎭 Reddit Rant Roulette - Backend Server")
    print("=" * 50)
    
    # Test scraper first
    if not test_scraper_setup():
        print("❌ Scraper setup failed. Exiting.")
        sys.exit(1)
    
    # Check for Reddit API credentials
    if os.getenv('REDDIT_CLIENT_ID') and os.getenv('REDDIT_CLIENT_SECRET'):
        print("✅ Reddit API credentials found - will use live data")
    else:
        print("⚠️  No Reddit API credentials - using sample data")
        print("   To get live data:")
        print("   1. Go to https://www.reddit.com/prefs/apps")
        print("   2. Create a script app")
        print("   3. Copy credentials to .env file")
    
    # Start the server
    start_api_server() 