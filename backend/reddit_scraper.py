import praw
import random
import os
from dotenv import load_dotenv
from typing import List, Dict
import re

# Load environment variables
load_dotenv()

class RedditRantScraper:
    def __init__(self):
        """Initialize the Reddit scraper with API credentials."""
        self.reddit = praw.Reddit(
            client_id=os.getenv('REDDIT_CLIENT_ID'),
            client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
            user_agent=os.getenv('REDDIT_USER_AGENT', 'RedditRantRoulette/1.0')
        )
        
        # Subreddits known for rants and angry posts
        self.rant_subreddits = [
            'rant',
            'offmychest',
            'TrueOffMyChest',
            'mildlyinfuriating',
            'unpopularopinion',
            'AmItheAsshole',
            'petpeeves',
            'Vent',
            'angry',
            'frustrating'
        ]
        
        # Keywords that indicate angry/rant content
        self.angry_keywords = [
            'annoying', 'frustrated', 'pissed', 'angry', 'hate', 'can\'t stand',
            'sick of', 'tired of', 'furious', 'irritating', 'ridiculous',
            'stupid', 'idiotic', 'infuriating', 'drives me crazy', 'wtf',
            'bullshit', 'nonsense', 'unbelievable', 'outrageous'
        ]
    
    def is_rant_like(self, text: str) -> bool:
        """Check if the text contains rant-like language."""
        text_lower = text.lower()
        
        # Check for angry keywords
        angry_count = sum(1 for keyword in self.angry_keywords if keyword in text_lower)
        
        # Check for excessive capitalization (shouting)
        caps_ratio = sum(1 for c in text if c.isupper()) / len(text) if text else 0
        
        # Check for excessive punctuation
        exclamation_count = text.count('!')
        
        # Scoring system
        score = 0
        score += angry_count * 2  # Angry keywords are worth 2 points each
        score += caps_ratio * 10  # High caps ratio adds points
        score += min(exclamation_count, 5)  # Max 5 points for exclamations
        
        return score >= 3  # Threshold for considering it a rant
    
    def clean_text(self, text: str) -> str:
        """Clean and format the text for better readability."""
        # Remove excessive newlines
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        # Remove Reddit-specific formatting
        text = re.sub(r'\[removed\]|\[deleted\]', '', text)
        
        # Remove excessive spaces
        text = re.sub(r' {2,}', ' ', text)
        
        return text.strip()
    
    def get_random_rant(self, limit: int = 50) -> Dict[str, str]:
        """Get a random rant from Reddit."""
        try:
            # Randomly select a subreddit
            subreddit_name = random.choice(self.rant_subreddits)
            subreddit = self.reddit.subreddit(subreddit_name)
            
            # Get hot posts from the subreddit
            posts = list(subreddit.hot(limit=limit))
            
            # Filter for rant-like posts
            rant_posts = []
            for post in posts:
                if post.selftext and len(post.selftext) > 100:  # Ensure there's substantial text
                    full_text = f"{post.title} {post.selftext}"
                    if self.is_rant_like(full_text):
                        rant_posts.append({
                            'title': post.title,
                            'content': post.selftext,
                            'subreddit': subreddit_name,
                            'score': post.score,
                            'url': f"https://reddit.com{post.permalink}"
                        })
            
            if rant_posts:
                # Return a random rant from the filtered list
                selected_rant = random.choice(rant_posts)
                selected_rant['content'] = self.clean_text(selected_rant['content'])
                return selected_rant
            else:
                # Fallback: return any post with substantial text
                text_posts = [p for p in posts if p.selftext and len(p.selftext) > 100]
                if text_posts:
                    fallback_post = random.choice(text_posts)
                    return {
                        'title': fallback_post.title,
                        'content': self.clean_text(fallback_post.selftext),
                        'subreddit': subreddit_name,
                        'score': fallback_post.score,
                        'url': f"https://reddit.com{fallback_post.permalink}"
                    }
                
        except Exception as e:
            print(f"Error fetching from subreddit {subreddit_name}: {e}")
            return None
    
    def get_multiple_rants(self, count: int = 5) -> List[Dict[str, str]]:
        """Get multiple rants for variety."""
        rants = []
        attempts = 0
        max_attempts = count * 3  # Try up to 3 times per requested rant
        
        while len(rants) < count and attempts < max_attempts:
            rant = self.get_random_rant()
            if rant:
                rants.append(rant)
            attempts += 1
        
        return rants

# Fallback scraper without API (for testing or if API fails)
class FallbackRantScraper:
    def __init__(self):
        """Initialize fallback scraper with some sample rants."""
        self.sample_rants = [
            {
                'title': "People who don't use turn signals",
                'content': "I am SO sick and tired of people who don't use their turn signals! How hard is it to move your finger like 2 inches to let other drivers know what you're planning to do? It's not optional, it's the LAW! And don't even get me started on people who put their signal on AFTER they've already started turning. What's the point?! You're supposed to signal your INTENTION, not announce what you're already doing!",
                'subreddit': 'rant',
                'score': 1234,
                'url': 'https://reddit.com/r/rant/sample'
            },
            {
                'title': "Grocery store checkout lines",
                'content': "Why do I always pick the slowest line at the grocery store?! Every. Single. Time. I'll carefully observe all the lines, count the people, look at their cart sizes, and somehow I STILL end up behind the person who wants to pay with exact change, has 47 coupons, and needs a price check on every item. Meanwhile, the line I almost chose is flying through customers like they're in a NASCAR pit stop!",
                'subreddit': 'mildlyinfuriating',
                'score': 892,
                'url': 'https://reddit.com/r/mildlyinfuriating/sample'
            }
        ]
    
    def get_random_rant(self) -> Dict[str, str]:
        """Return a random sample rant."""
        return random.choice(self.sample_rants)
    
    def get_multiple_rants(self, count: int = 5) -> List[Dict[str, str]]:
        """Return multiple sample rants."""
        return [self.get_random_rant() for _ in range(min(count, len(self.sample_rants)))]

if __name__ == "__main__":
    # Test the scraper
    print("Testing Reddit Rant Scraper...")
    
    try:
        scraper = RedditRantScraper()
        rant = scraper.get_random_rant()
        if rant:
            print(f"\nTitle: {rant['title']}")
            print(f"Subreddit: r/{rant['subreddit']}")
            print(f"Score: {rant['score']}")
            print(f"Content: {rant['content'][:200]}...")
        else:
            print("No rant found, using fallback...")
            fallback = FallbackRantScraper()
            rant = fallback.get_random_rant()
            print(f"\nSample Title: {rant['title']}")
            print(f"Sample Content: {rant['content'][:200]}...")
    except Exception as e:
        print(f"Error with main scraper: {e}")
        print("Using fallback scraper...")
        fallback = FallbackRantScraper()
        rant = fallback.get_random_rant()
        print(f"\nSample Title: {rant['title']}")
        print(f"Sample Content: {rant['content'][:200]}...") 