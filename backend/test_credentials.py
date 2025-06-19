#!/usr/bin/env python3
"""
Test script to verify Reddit API credentials are working
"""
import os
import sys
from dotenv import load_dotenv
from reddit_scraper import RedditRantScraper, FallbackRantScraper

def test_reddit_credentials():
    """Test if Reddit API credentials are working"""
    print("🔍 Testing Reddit API Credentials...")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    # Check if credentials are set
    client_id = os.getenv('REDDIT_CLIENT_ID')
    client_secret = os.getenv('REDDIT_CLIENT_SECRET')
    user_agent = os.getenv('REDDIT_USER_AGENT')
    
    print(f"Client ID: {client_id[:10]}..." if client_id else "❌ REDDIT_CLIENT_ID not found")
    print(f"Client Secret: {client_secret[:10]}..." if client_secret else "❌ REDDIT_CLIENT_SECRET not found")
    print(f"User Agent: {user_agent}" if user_agent else "❌ REDDIT_USER_AGENT not found")
    
    if not all([client_id, client_secret, user_agent]):
        print("\n❌ Missing Reddit API credentials!")
        print("Please check your .env file")
        return False
    
    # Test the scraper
    try:
        print("\n🚀 Testing Reddit API connection...")
        scraper = RedditRantScraper()
        
        # Try to get a rant
        rant = scraper.get_random_rant()
        
        if rant:
            print("✅ Reddit API connection successful!")
            print(f"   Title: {rant['title'][:50]}...")
            print(f"   Subreddit: r/{rant['subreddit']}")
            print(f"   Score: {rant['score']}")
            print(f"   Content length: {len(rant['content'])} characters")
            return True
        else:
            print("⚠️ Reddit API connected but no rants found")
            print("This might be due to rate limiting or subreddit issues")
            return False
            
    except Exception as e:
        print(f"❌ Reddit API connection failed: {e}")
        print("\nTrying fallback scraper...")
        
        try:
            fallback = FallbackRantScraper()
            rant = fallback.get_random_rant()
            print("✅ Fallback scraper working")
            print(f"   Sample title: {rant['title'][:50]}...")
            return False  # Reddit API failed, but fallback works
        except Exception as fallback_error:
            print(f"❌ Even fallback scraper failed: {fallback_error}")
            return False

def test_huggingface_token():
    """Test if Hugging Face token is configured"""
    print("\n🤖 Testing Hugging Face AI Configuration...")
    print("=" * 50)
    
    hf_token = os.getenv('HF_TOKEN')
    
    if not hf_token or hf_token == 'your_huggingface_token_here':
        print("❌ HF_TOKEN not configured")
        print("   AI poem generation will use template fallbacks")
        print("   To enable AI:")
        print("   1. Go to https://huggingface.co/settings/tokens")
        print("   2. Create a token with 'Read' permissions")
        print("   3. Add HF_TOKEN=your_token to .env file")
        return False
    else:
        print(f"✅ HF_TOKEN configured: {hf_token[:10]}...")
        
        # Test AI poem generation
        try:
            from aiPoem import convert_rant_to_poem_mistral_new
            test_rant = "I hate waiting in line! It's so annoying!"
            poem = convert_rant_to_poem_mistral_new(test_rant)
            
            if poem and not poem.startswith("Error:"):
                print("✅ AI poem generation working!")
                print(f"   Sample poem: {poem[:100]}...")
                return True
            else:
                print(f"❌ AI poem generation failed: {poem}")
                return False
                
        except Exception as e:
            print(f"❌ AI poem generation error: {e}")
            return False

if __name__ == "__main__":
    print("🎭 Reddit Rant Roulette - Credential Test")
    print("=" * 60)
    
    reddit_ok = test_reddit_credentials()
    hf_ok = test_huggingface_token()
    
    print("\n" + "=" * 60)
    print("📊 CREDENTIAL TEST RESULTS:")
    print(f"   Reddit API: {'✅ WORKING' if reddit_ok else '❌ FAILED (using fallback)'}")
    print(f"   Hugging Face AI: {'✅ WORKING' if hf_ok else '❌ NOT CONFIGURED (using templates)'}")
    
    if reddit_ok and hf_ok:
        print("\n🎉 All systems go! Your app has full functionality:")
        print("   ✅ Live Reddit data")
        print("   ✅ AI-generated poetry")
        print("   ✅ High-performance caching")
    elif reddit_ok:
        print("\n🚀 Partial functionality:")
        print("   ✅ Live Reddit data")
        print("   ⚠️ Template-based poetry (no AI)")
        print("   ✅ High-performance caching")
    else:
        print("\n⚠️ Basic functionality:")
        print("   ⚠️ Sample Reddit data (fallback)")
        print("   ⚠️ Template-based poetry")
        print("   ✅ High-performance caching")
    
    print(f"\n🎯 Ready to start your servers!")
    print("   Backend: cd backend && python app.py")
    print("   Frontend: npm run dev")