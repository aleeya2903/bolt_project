# 🎭 Reddit Rant Roulette

> **Turn Internet Rage into Poetry!**

A fun and interactive web application that transforms everyday internet rants into beautiful, whimsical poetry. Experience the magic of turning digital frustration into artistic expression with just a click!

![Reddit Rant Roulette](https://img.shields.io/badge/React-18.3.1-61DAFB?style=for-the-badge&logo=react)
![TypeScript](https://img.shields.io/badge/TypeScript-5.5.3-3178C6?style=for-the-badge&logo=typescript)
![Vite](https://img.shields.io/badge/Vite-5.4.2-646CFF?style=for-the-badge&logo=vite)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-3.4.1-38B2AC?style=for-the-badge&logo=tailwind-css)

## ✨ Features

- 🎰 **Random Rant Generator**: Spin the wheel to get a random internet rant
- 🎭 **Poetry Transformation**: Each rant comes with its beautiful poetic counterpart
- 📋 **Copy to Clipboard**: Easily copy rants or poems to share
- 📱 **Responsive Design**: Works beautifully on all devices
- 🎨 **Beautiful UI**: Stunning gradients and smooth animations
- ⚡ **Fast Performance**: Built with Vite for lightning-fast development
- 🔄 **Spin Counter**: Track how many times you've spun the wheel
- 🎯 **Reset Functionality**: Start fresh anytime

## 🎮 How It Works

1. **Click "SPIN THE RANT!"** - Watch the magical spinning animation
2. **Read the Rant** - Enjoy a relatable internet frustration
3. **Discover the Poetry** - See how rage transforms into art
4. **Copy & Share** - Share your favorite rants or poems
5. **Spin Again** - Discover more entertaining combinations!

## 🛠️ Tech Stack

### Frontend
- **Framework**: React 18.3.1 with TypeScript
- **Build Tool**: Vite 5.4.2
- **Styling**: Tailwind CSS 3.4.1
- **Icons**: Lucide React 0.344.0
- **Development**: ESLint, PostCSS, Autoprefixer

### Backend
- **Framework**: Flask 2.3.3 (Python)
- **Reddit API**: PRAW 7.7.1
- **HTTP Client**: Requests 2.31.0
- **Web Scraping**: BeautifulSoup4 4.12.2
- **Environment**: python-dotenv 1.0.0
- **CORS**: Flask-CORS 4.0.0

## 🚀 Quick Start

### Prerequisites

- **Frontend**: Node.js (version 16 or higher), npm or yarn
- **Backend**: Python 3.7+, pip

### Full Stack Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/aleeya2903/bolt_project.git
   cd bolt_project
   ```

2. **Frontend Setup**
   ```bash
   # Install frontend dependencies
   npm install
   # or
   yarn install
   ```

3. **Backend Setup**
   ```bash
   # Navigate to backend directory
   cd backend
   
   # Install Python dependencies
   pip install -r requirements.txt
   
   # Set up Reddit API (Optional - app works with fallback data)
   cp env_template.txt .env
   # Edit .env with your Reddit API credentials (see Backend Configuration below)
   ```

4. **Start Both Servers**
   
   **Terminal 1 - Backend (API Server):**
   ```bash
   cd backend
   python app.py
   # Backend will run on http://localhost:5001
   ```
   
   **Terminal 2 - Frontend (React App):**
   ```bash
   # From project root
   npm run dev
   # or
   yarn dev
   # Frontend will run on http://localhost:5173
   ```

5. **Open your browser**
   ```
   Navigate to http://localhost:5173
   ```

### Frontend Only (Static Mode)

If you only want to run the frontend with hardcoded rants:

```bash
npm install
npm run dev
```

The app will work with 8 pre-written rant/poem pairs without needing the backend.

## 📜 Available Scripts

### Frontend Scripts
| Command | Description |
|---------|-------------|
| `npm run dev` | Start development server on port 5173 |
| `npm run build` | Build for production |
| `npm run preview` | Preview production build |
| `npm run lint` | Run ESLint for code quality |

### Backend Scripts
| Command | Description |
|---------|-------------|
| `python app.py` | Start Flask API server on port 5001 |
| `python test_api.py` | Test the API endpoints |
| `python reddit_scraper.py` | Test Reddit scraping functionality |

## 📁 Project Structure

```
bolt_project/
├── frontend/
│   ├── public/               # Static assets
│   ├── src/
│   │   ├── App.tsx          # Main React component
│   │   ├── main.tsx         # React entry point
│   │   ├── index.css        # Global styles
│   │   └── vite-env.d.ts    # Vite type definitions
│   ├── index.html           # HTML template
│   ├── package.json         # Frontend dependencies
│   ├── vite.config.ts       # Vite configuration
│   ├── tailwind.config.js   # Tailwind CSS configuration
│   └── tsconfig.json        # TypeScript configuration
├── backend/
│   ├── app.py              # Flask API server
│   ├── reddit_scraper.py   # Reddit data scraping logic
│   ├── start_server.py     # Alternative server starter
│   ├── test_api.py         # API testing utilities
│   ├── requirements.txt    # Python dependencies
│   ├── env_template.txt    # Environment variables template
│   ├── README.md          # Backend-specific documentation
│   └── REDDIT_SETUP.md    # Reddit API setup guide
├── .gitignore             # Git ignore rules
└── README.md             # This file
```

## 🎯 Core Components

### RantData Interface
```typescript
interface RantData {
  id: number;
  rant: string;
  poem: string;
}
```

### Key Features
- **Hardcoded Content**: 8 carefully curated rant/poem pairs
- **State Management**: React hooks for UI state
- **Responsive Layout**: Two-column grid for rants and poems
- **Interactive Animations**: Spinning wheels, hover effects, and transitions

## 🎨 Design Features

- **Gradient Backgrounds**: Beautiful purple-to-blue gradients
- **Animated Text**: Pulsing rainbow headers
- **Card Layouts**: Distinct styling for rants (red/orange) vs poems (green/teal)
- **Hover Effects**: Scale transforms and shadow effects
- **Loading States**: Spinning animations during content generation
- **Mobile-First**: Responsive design that works on all screen sizes

## 🔧 Configuration

### Frontend Configuration (Vite)
- React plugin enabled
- Development server on port 5173
- Optimized for `lucide-react` package

### Frontend Styling (Tailwind CSS)
- Custom gradient configurations
- Responsive breakpoints
- Animation utilities

### Backend Configuration (Reddit API)

For live Reddit data, set up Reddit API credentials:

1. **Create Reddit App**
   - Go to [Reddit Apps](https://www.reddit.com/prefs/apps)
   - Click "Create App" or "Create Another App"
   - Choose **"script"** as the app type
   - Fill in the form:
     - Name: `Reddit Rant Roulette`
     - Description: `Poetry generator from internet rants`
     - Redirect URI: `http://localhost:8080`

2. **Configure Environment Variables**
   ```bash
   cd backend
   cp env_template.txt .env
   ```
   
   Edit `.env` file:
   ```env
   REDDIT_CLIENT_ID=your_14_character_client_id
   REDDIT_CLIENT_SECRET=your_27_character_secret
   REDDIT_USER_AGENT=RedditRantRoulette/1.0
   ```

3. **Backend Dependencies**
   - **Flask**: Web API framework (port 5001)
   - **PRAW**: Reddit API wrapper
   - **Flask-CORS**: Cross-origin resource sharing
   - **python-dotenv**: Environment variable management

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/rant` | GET | Get a single random rant |
| `/api/rants?count=3` | GET | Get multiple rants |
| `/api/health` | GET | Health check |
| `/api/setup-info` | GET | Configuration status |

## 🚀 Deployment

### Frontend Deployment

**Build for Production:**
```bash
npm run build
```
The build files will be generated in the `dist/` directory.

**Frontend Hosting Options:**
- **Vercel**: Zero-config deployment for React apps
- **Netlify**: Drag-and-drop deployment with continuous integration
- **GitHub Pages**: Free hosting for static sites
- **Cloudflare Pages**: Fast global CDN deployment

### Backend Deployment

**Backend Hosting Options:**
- **Heroku**: Easy Python app deployment
- **Railway**: Modern platform with Git integration
- **DigitalOcean App Platform**: Managed container hosting
- **AWS EC2**: Full control virtual private servers
- **Google Cloud Run**: Serverless container platform

**Environment Variables for Production:**
```bash
# Required for backend deployment
REDDIT_CLIENT_ID=your_production_client_id
REDDIT_CLIENT_SECRET=your_production_secret
REDDIT_USER_AGENT=RedditRantRoulette/1.0
FLASK_ENV=production
```

### Full Stack Deployment

For a complete deployment, you'll need:
1. **Backend API** deployed and accessible via HTTPS
2. **Frontend** configured to point to your backend API URL
3. **Environment variables** properly configured for production
4. **CORS** settings updated for your frontend domain

**Example Production Setup:**
- Backend: `https://your-api.herokuapp.com`
- Frontend: `https://your-app.vercel.app`
- Update frontend API calls to use production backend URL

## 🎭 Sample Content

The app features 8 entertaining rant/poem pairs covering topics like:
- 🚶 Slow walkers in hallways
- 🍕 Pineapple on pizza debates
- 🚗 Turn signal etiquette
- 🧽 Household chores
- 🎵 Loud music on public transport
- 🍽️ Dining manners
- 🎬 Movie theater behavior
- 🏧 ATM efficiency

## 🔧 Troubleshooting

### Frontend Issues
- **Port 5173 already in use**: Kill the process with `lsof -ti:5173 | xargs kill -9`
- **Module not found**: Run `npm install` to ensure all dependencies are installed
- **Build fails**: Check Node.js version (requires 16+)

### Backend Issues
- **"No rant found" errors**: 
  - Reddit API might be hitting rate limits
  - Try again in a few minutes
  - Verify Reddit API credentials in `.env` file
- **CORS errors**: 
  - Ensure Flask server is running on port 5001
  - Check if both frontend and backend servers are running
- **Import errors**: 
  - Install dependencies: `pip install -r requirements.txt`
  - Check Python version (3.7+ required)
- **Port 5001 already in use**: Find and kill the process using the port

### Integration Issues
- **API connection fails**: 
  - Backend server must be running before frontend
  - Check `http://localhost:5001/api/health` in browser
  - Verify no firewall is blocking the connection

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🎉 Fun Facts

- **Poetry Style**: Each poem follows a consistent AABB rhyme scheme
- **Rant Topics**: Carefully selected for maximum relatability
- **Color Psychology**: Red/orange for anger, green/teal for tranquility
- **Performance**: Optimized for smooth animations and quick loading

---

**Made with 💀 and ☕ for maximum internet chaos**

*Transform your daily frustrations into beautiful art - one rant at a time!* 🎭✨ 