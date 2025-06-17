# Reddit Rant Roulette - Backend Scraper

This is the backend component for the Reddit Rant Roulette hackathon project. It scrapes angry rants from Reddit and serves them via a Flask API for the frontend to consume and convert into poems.

## Features

- 🔥 Scrapes angry rants from popular subreddits
- 🎯 Intelligent rant detection using keyword analysis and text patterns
- 🔄 Fallback system with sample rants for testing
- 🌐 RESTful API for frontend integration
- 🚀 Easy setup and deployment

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Reddit API (Optional but Recommended)

For live data, you need Reddit API credentials:

1. Go to [Reddit Apps](https://www.reddit.com/prefs/apps)
2. Click "Create App" or "Create Another App"
3. Choose **"script"** as the app type
4. Fill in the form:
   - Name: `Reddit Rant Roulette`
   - Description: `Hackathon project for converting rants to poetry`
   - About URL: (leave blank)
   - Redirect URI: `http://localhost:8080`

5. Copy your credentials and create a `.env` file:

```bash
# Copy the template
cp env_template.txt .env

# Edit .env with your credentials
REDDIT_CLIENT_ID=your_14_character_client_id
REDDIT_CLIENT_SECRET=your_27_character_secret
REDDIT_USER_AGENT=RedditRantRoulette/1.0
```

### 3. Run the Server

```bash
python app.py
```

The API will be available at `http://localhost:5001`

## API Endpoints

### Get Random Rant
```
GET /api/rant
```

Response:
```json
{
  "success": true,
  "rant": {
    "title": "People who don't use turn signals",
    "content": "I am SO sick and tired of people who...",
    "subreddit": "rant",
    "score": 1234,
    "url": "https://reddit.com/r/rant/..."
  },
  "using_live_data": true
}
```

### Get Multiple Rants
```
GET /api/rants?count=3
```

### Health Check
```
GET /api/health
```

### Setup Information
```
GET /api/setup-info
```

## Testing Without Reddit API

The scraper includes a fallback system with sample rants, so you can test the entire system without setting up Reddit API credentials. Simply run `python app.py` and it will use the fallback data.

## Subreddits Used

The scraper targets these subreddits known for rants:
- r/rant
- r/offmychest
- r/TrueOffMyChest
- r/mildlyinfuriating
- r/unpopularopinion
- r/AmItheAsshole
- r/petpeeves
- r/Vent
- r/angry
- r/frustrating

## Rant Detection Algorithm

The scraper uses multiple criteria to identify rants:
- **Angry keywords**: frustrated, pissed, hate, annoying, etc.
- **Capitalization patterns**: Excessive caps indicating shouting
- **Punctuation**: Multiple exclamation marks
- **Text length**: Substantial content (100+ characters)

## Frontend Integration

Your frontend can fetch rants like this:

```javascript
// Get a single random rant
const response = await fetch('http://localhost:5001/api/rant');
const data = await response.json();

if (data.success) {
  const rant = data.rant;
  console.log(rant.title, rant.content);
}
```

## Troubleshooting

### "No rant found" errors
- The scraper might be hitting rate limits
- Try again in a few minutes
- Check if your Reddit API credentials are correct

### CORS errors
- Make sure the Flask server is running on port 5001
- The server includes CORS headers for frontend integration

### Import errors
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Check your Python version (3.7+ recommended)

## Rate Limiting & Ethics

- The scraper respects Reddit's rate limits
- Uses the official PRAW library for proper API usage
- Includes user agent identification
- Only scrapes public posts
- No personal information is collected

## 🎯 Frontend Integration with Bolt Project

Your React frontend (`/bolt_project`) is ready to connect! Here's how to integrate:

### 1. Update the Frontend API Call

Replace the hardcoded rants in your `bolt_project/src/App.tsx` with live Reddit data:

```typescript
// Add this interface for Reddit API response
interface RedditRantResponse {
  success: boolean;
  rant: {
    title: string;
    content: string;
    subreddit: string;
    score: number;
    url: string;
  };
  using_live_data: boolean;
}

// Replace the spinRant function with this:
const spinRant = async () => {
  setIsSpinning(true);
  
  try {
    // Fetch real Reddit rant from your API
    const response = await fetch('http://localhost:5001/api/rant');
    const data: RedditRantResponse = await response.json();
    
    if (data.success) {
      const rant = data.rant;
      
      // Create a poem using AI (you'll need to add your AI service here)
      const poem = await generatePoem(rant.content); // Replace with your AI integration
      
      setCurrentRant({
        id: Date.now(),
        rant: `${rant.title}\n\n${rant.content}`,
        poem: poem
      });
    } else {
      // Fallback to hardcoded rants if API fails
      const randomIndex = Math.floor(Math.random() * hardcodedRants.length);
      setCurrentRant(hardcodedRants[randomIndex]);
    }
  } catch (error) {
    console.error('API Error:', error);
    // Fallback to hardcoded rants
    const randomIndex = Math.floor(Math.random() * hardcodedRants.length);
    setCurrentRant(hardcodedRants[randomIndex]);
  }
  
  setSpinCount(prev => prev + 1);
  setIsSpinning(false);
};
```

### 2. Start Both Servers

**Terminal 1 - Backend (Reddit Scraper):**
```bash
cd redditRantScrapper
python start_server.py
```

**Terminal 2 - Frontend (React App):**
```bash
cd bolt_project
npm run dev
```

### 3. Your App Flow

1. **User clicks "SPIN THE RANT!"** 🎰
2. **Frontend calls** → `http://localhost:5001/api/rant`
3. **Backend returns** → Real Reddit rant data
4. **Frontend sends rant to AI** → Your poem generator
5. **Display both** → Original rant + Generated poem

### 4. API Response Structure

Your backend returns this format:
```json
{
  "success": true,
  "rant": {
    "title": "People who don't use turn signals",
    "content": "I am SO sick and tired of people who...",
    "subreddit": "rant",
    "score": 1234,
    "url": "https://reddit.com/r/rant/..."
  },
  "using_live_data": true
}
```

### 5. Add AI Poem Generation

You'll need to integrate with an AI service (OpenAI, Anthropic, etc.):

```typescript
const generatePoem = async (rantText: string): Promise<string> => {
  // Replace with your AI service
  const response = await fetch('YOUR_AI_API_ENDPOINT', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      prompt: `Turn this angry rant into a beautiful poem: ${rantText}`,
      // Add your AI service parameters
    })
  });
  
  const aiResponse = await response.json();
  return aiResponse.poem; // Adjust based on your AI service response
};
```

## For Your Hackathon Team

This backend provides:
1. **Reliable rant data** for your poem generator
2. **Fallback system** so your demo always works
3. **RESTful API** that's easy to integrate
4. **CORS enabled** for frontend development

Your frontend is at: `http://localhost:5173` (Vite dev server)
Your backend is at: `http://localhost:5001` (Flask API)

## Development

To run in development mode:
```bash
python app.py
```

To test the scraper directly:
```bash
python reddit_scraper.py
``` 