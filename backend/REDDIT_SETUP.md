# 🔥 Getting Live Reddit Rants - API Setup Guide

Right now your API is using **sample hardcoded rants**. To get **real angry Reddit rants**, follow this quick setup:

## Step 1: Create Reddit App

1. **Go to Reddit Apps**: https://www.reddit.com/prefs/apps
2. **Click "Create App"** or **"Create Another App"**
3. **Fill out the form**:
   - **Name**: `Reddit Rant Roulette`
   - **App type**: Choose **"script"** (important!)
   - **Description**: `Hackathon project for converting rants to poetry`
   - **About URL**: Leave blank
   - **Redirect URI**: `http://localhost:8080`

4. **Click "Create app"**

## Step 2: Get Your Credentials

After creating the app, you'll see:
- **Client ID**: 14-character string (under the app name)
- **Secret**: 27-character string (labeled "secret")

## Step 3: Create .env File

In your `redditRantScrapper` folder, create a `.env` file:

```bash
# In redditRantScrapper folder
touch .env
```

Add your credentials:
```env
REDDIT_CLIENT_ID=your_14_character_client_id_here
REDDIT_CLIENT_SECRET=your_27_character_secret_here
REDDIT_USER_AGENT=RedditRantRoulette/1.0
```

## Step 4: Restart Your Server

```bash
python start_server.py
```

You should see:
```
✅ Reddit API credentials found - will use live data
```

## Step 5: Test Live Rants

```bash
curl http://localhost:5001/api/rant
```

You should get real Reddit rants like:
```json
{
  "success": true,
  "rant": {
    "title": "Actual angry Reddit post title",
    "content": "Real rant content from r/rant or r/mildlyinfuriating...",
    "subreddit": "rant",
    "score": 1547,
    "url": "https://reddit.com/r/rant/actual_post"
  },
  "using_live_data": true
}
```

## 🚀 You're Now Getting Real Rants!

Your app will now pull from these subreddits:
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

## Troubleshooting

**Still seeing sample rants?**
- Check your `.env` file is in the `redditRantScrapper` folder
- Verify your credentials are correct
- Restart the server: `python start_server.py`

**Getting rate limit errors?**
- Reddit has rate limits - wait a few minutes
- The app automatically retries different subreddits

**App not working at all?**
- The fallback system ensures your demo always works
- Even without Reddit API, you'll get sample rants

## 🎭 Ready for Your Demo!

Your hackathon project now has:
- ✅ **Live Reddit rant scraping**
- ✅ **Intelligent rant detection**  
- ✅ **Fallback system for demos**
- ✅ **Clean API for your frontend**

Connect your React frontend and you're ready to turn internet rage into poetry! 🚀 