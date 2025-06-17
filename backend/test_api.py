#!/usr/bin/env python3
"""
Test script for Reddit Rant Scraper API
This script tests both the scraper and the Flask API endpoints
"""

import requests
import json
import sys
import time
from reddit_scraper import FallbackRantScraper, RedditRantScraper

def test_scraper():
    """Test the scraper directly"""
    print("🔍 Testing Reddit Scraper...")
    
    try:
        # Test fallback scraper
        fallback = FallbackRantScraper()
        rant = fallback.get_random_rant()
        
        print(f"✅ Fallback scraper working!")
        print(f"   Title: {rant['title']}")
        print(f"   Preview: {rant['content'][:80]}...")
        print(f"   Subreddit: r/{rant['subreddit']}")
        
        # Test multiple rants
        rants = fallback.get_multiple_rants(3)
        print(f"✅ Multiple rants: Got {len(rants)} rants")
        
    except Exception as e:
        print(f"❌ Scraper test failed: {e}")
        return False
    
    return True

def test_api():
    """Test the Flask API endpoints"""
    print("\n🌐 Testing Flask API...")
    
    base_url = "http://localhost:5001"
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/api/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check: {data['message']}")
            print(f"   Scraper type: {data['scraper_type']}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False
    
    # Test random rant endpoint
    try:
        response = requests.get(f"{base_url}/api/rant", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                rant = data['rant']
                print(f"✅ Random rant endpoint working!")
                print(f"   Title: {rant['title']}")
                print(f"   Preview: {rant['content'][:80]}...")
                print(f"   Using live data: {data['using_live_data']}")
            else:
                print(f"❌ Rant endpoint returned error: {data.get('error')}")
                return False
        else:
            print(f"❌ Rant endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Rant endpoint failed: {e}")
        return False
    
    # Test multiple rants endpoint
    try:
        response = requests.get(f"{base_url}/api/rants?count=2", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                print(f"✅ Multiple rants endpoint: Got {data['count']} rants")
            else:
                print(f"❌ Multiple rants endpoint error: {data.get('error')}")
                return False
        else:
            print(f"❌ Multiple rants endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Multiple rants endpoint failed: {e}")
        return False
    
    return True

def test_frontend_integration():
    """Test frontend integration example"""
    print("\n🎨 Testing Frontend Integration...")
    
    try:
        # Simulate frontend request
        response = requests.get("http://localhost:5001/api/rant", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                rant_data = data['rant']
                
                # This is what your frontend would receive
                frontend_payload = {
                    'title': rant_data['title'],
                    'content': rant_data['content'],
                    'source': f"r/{rant_data['subreddit']}",
                    'score': rant_data['score']
                }
                
                print("✅ Frontend integration ready!")
                print("   Sample payload for your poem generator:")
                print(f"   Title: {frontend_payload['title']}")
                print(f"   Content: {frontend_payload['content'][:100]}...")
                print(f"   Source: {frontend_payload['source']}")
                
                return True
        
        print("❌ Frontend integration test failed")
        return False
        
    except Exception as e:
        print(f"❌ Frontend integration test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Reddit Rant Roulette - Backend Test Suite")
    print("=" * 50)
    
    # Test scraper
    scraper_ok = test_scraper()
    
    if not scraper_ok:
        print("❌ Scraper tests failed!")
        sys.exit(1)
    
    # Test API (only if we can connect)
    print("\nStarting API tests...")
    print("Note: Make sure Flask server is running (python app.py)")
    
    # Give user time to start the server if needed
    time.sleep(2)
    
    api_ok = test_api()
    frontend_ok = test_frontend_integration()
    
    print("\n" + "=" * 50)
    print("📊 Test Results:")
    print(f"   Scraper: {'✅ PASS' if scraper_ok else '❌ FAIL'}")
    print(f"   API: {'✅ PASS' if api_ok else '❌ FAIL'}")
    print(f"   Frontend Integration: {'✅ PASS' if frontend_ok else '❌ FAIL'}")
    
    if scraper_ok and api_ok and frontend_ok:
        print("\n🎉 All tests passed! Your Reddit Rant Scraper is ready!")
        print("\n📝 Next steps:")
        print("   1. Connect your frontend to http://localhost:5001/api/rant")
        print("   2. Send the rant content to your AI poem generator")
        print("   3. Display the poem alongside the original rant")
        print("\n💡 Optional: Set up Reddit API credentials for live data")
    else:
        print("\n⚠️  Some tests failed. Check the error messages above.")
        if not api_ok:
            print("   💡 Make sure Flask server is running on port 5001: python app.py") 