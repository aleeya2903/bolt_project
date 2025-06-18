#!/usr/bin/env python3
"""
Test script to verify the AI poem integration is working correctly.
"""
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

def test_endpoints():
    """Test all the endpoints to make sure everything is working."""
    base_url = "http://localhost:5001"
    
    print("🧪 Testing Reddit Rant to AI Poem Integration")
    print("=" * 50)
    
    # Test 1: Health check
    print("\n1. Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/api/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed")
            print(f"   - Scraper type: {data['scraper_type']}")
            print(f"   - AI configured: {data['ai_poem_configured']}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure Flask app is running on port 5001")
        return False
    
    # Test 2: Setup info
    print("\n2. Testing setup info...")
    try:
        response = requests.get(f"{base_url}/api/setup-info")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Setup info retrieved")
            print(f"   - Reddit API: {data['reddit_api_configured']}")
            print(f"   - HF Token: {data['ai_poem_configured']}")
            
            if not data['ai_poem_configured']:
                print("⚠️  Warning: HF_TOKEN not found in environment")
        else:
            print(f"❌ Setup info failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Setup info error: {e}")
    
    # Test 3: Get a rant
    print("\n3. Testing rant endpoint...")
    try:
        response = requests.get(f"{base_url}/api/rant")
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                print(f"✅ Rant retrieved successfully")
                print(f"   - Title: {data['rant']['title'][:50]}...")
                print(f"   - Subreddit: r/{data['rant']['subreddit']}")
                print(f"   - Using live data: {data['using_live_data']}")
            else:
                print(f"❌ Rant endpoint returned success=False")
        else:
            print(f"❌ Rant endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Rant endpoint error: {e}")
    
    # Test 4: Generate poem from custom text
    print("\n4. Testing AI poem generation...")
    test_rant = "I hate waiting in line at the grocery store! It takes forever and people are so slow!"
    
    try:
        response = requests.post(f"{base_url}/api/poem", 
                               json={"rant_text": test_rant})
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                print(f"✅ AI poem generated successfully")
                print(f"   - Poem preview: {data['poem'][:100]}...")
            else:
                print(f"❌ Poem generation failed: {data['error']}")
        else:
            print(f"❌ Poem endpoint failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Poem generation error: {e}")
    
    # Test 5: The main combined endpoint
    print("\n5. Testing combined rant-and-poem endpoint...")
    try:
        response = requests.get(f"{base_url}/api/rant-and-poem")
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                print(f"✅ Combined endpoint works!")
                print(f"   - Rant title: {data['rant']['title'][:50]}...")
                
                if data['poem']:
                    print(f"   - AI poem generated: ✅")
                    print(f"   - Poem preview: {data['poem'][:100]}...")
                else:
                    print(f"   - AI poem failed: {data.get('poem_error', 'Unknown error')}")
                    
                print(f"   - Using live data: {data['using_live_data']}")
            else:
                print(f"❌ Combined endpoint returned success=False")
        else:
            print(f"❌ Combined endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Combined endpoint error: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 Integration test complete!")
    
    # Environment check
    print("\n📋 Environment Status:")
    hf_token = os.getenv('HF_TOKEN')
    reddit_id = os.getenv('REDDIT_CLIENT_ID')
    reddit_secret = os.getenv('REDDIT_CLIENT_SECRET')
    
    print(f"   - HF_TOKEN: {'✅ Set' if hf_token else '❌ Missing'}")
    print(f"   - REDDIT_CLIENT_ID: {'✅ Set' if reddit_id else '❌ Missing'}")
    print(f"   - REDDIT_CLIENT_SECRET: {'✅ Set' if reddit_secret else '❌ Missing'}")
    
    if not hf_token:
        print("\n⚠️  To enable AI poetry:")
        print("   1. Get a Hugging Face token from https://huggingface.co/settings/tokens")
        print("   2. Add HF_TOKEN=your_token_here to your .env file")
        print("   3. Restart the Flask server")

if __name__ == "__main__":
    test_endpoints() 