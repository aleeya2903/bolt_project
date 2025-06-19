import  { useState, useEffect } from 'react';
import { Shuffle, Copy, RotateCcw, Zap, Clock, TrendingUp } from 'lucide-react';

interface RantAndPoemResponse {
  success: boolean;
  rant: {
    title: string;
    content: string;
    subreddit: string; 
    score: number;
    url: string;
  };
  poem: string | null;
  poem_error?: string;
  error?: string;
  using_live_data: boolean;
  cached?: boolean;
  is_ai?: boolean;
  response_time_ms?: number;
  generated_at?: string;
}

// Cache stats interface
interface CacheStats {
  cache_size: number;
  cache_hits: number;
  cache_misses: number;
  hit_ratio_percent: number;
  total_requests: number;
  generation_successes: number;
  generation_failures: number;
  last_generated: string | null;
}

// Update your existing RantData interface to include source
interface RantData {
  id: number;
  rant: string;
  poem: string;
  source?: string;
  isAI?: boolean; // Add this to track if poem is AI-generated
  cached?: boolean; // Track if served from cache
  responseTime?: number; // Track response time
  generatedAt?: string; // When the content was generated
}

function App() {
  const [currentRant, setCurrentRant] = useState<RantData | null>(null);
  const [isSpinning, setIsSpinning] = useState(false);
  const [spinCount, setSpinCount] = useState(0);
  const [copiedText, setCopiedText] = useState<string>('');
  const [cacheStats, setCacheStats] = useState<CacheStats | null>(null);
  const [performanceMode, setPerformanceMode] = useState<'normal' | 'fast'>('normal');
  
  // Fetch cache stats on component mount and periodically
  useEffect(() => {
    const fetchCacheStats = async () => {
      try {
        const response = await fetch('http://localhost:5001/api/cache/stats');
        if (response.ok) {
          const data = await response.json();
          setCacheStats(data.cache_stats);
        }
      } catch (error) {
        console.log('Cache stats not available:', error);
      }
    };
    
    fetchCacheStats();
    const interval = setInterval(fetchCacheStats, 10000); // Update every 10 seconds
    
    return () => clearInterval(interval);
  }, []);
  
  // Fallback simple poem generator (only used if AI fails)
  const generateSimplePoem = (rantText: string): string => {
    const emotionWords = ['angry', 'frustrated', 'annoying', 'hate', 'love', 'beautiful'];
    const foundEmotions = emotionWords.filter(word => 
      rantText.toLowerCase().includes(word)
    );
    
    const poemTemplates = [
      `Oh world of frustration and endless dismay,
Where ${foundEmotions[0] || 'anger'} rules both night and day,
Let patience flow like a gentle stream,
And turn your ${foundEmotions[1] || 'frustration'} into a peaceful dream.`,
      
      `In the realm where complaints do dwell,
Your passionate words ring like a bell,
Though ${foundEmotions[0] || 'irritation'} may cloud your sight,
Beauty emerges when we shed some light.`,
      
      `From depths of ${foundEmotions[0] || 'annoyance'} comes this tale,
Where ordinary moments often fail,
But in your words, though fierce they may be,
Lies poetry for all the world to see.`
    ];
    
    return poemTemplates[Math.floor(Math.random() * poemTemplates.length)];
  };

  const spinRant = async () => {
    setIsSpinning(true);
    const startTime = performance.now();
    
    try {
      // Choose endpoint based on performance mode
      const endpoint = performanceMode === 'fast' 
        ? 'http://localhost:5001/api/rant-and-poem-fast'  // Ultra-fast, cache-only
        : 'http://localhost:5001/api/rant-and-poem';      // Fast with fallback
      
      const response = await fetch(endpoint);
      const data: RantAndPoemResponse = await response.json();
      
      if (data.success && data.rant) {
        const rant = data.rant;
        let poem = data.poem;
        let isAI = data.is_ai || false;
        
        // If AI poem generation failed, use our fallback
        if (!poem || data.poem_error) {
          console.warn('AI poem generation failed:', data.poem_error);
          poem = generateSimplePoem(rant.content);
          isAI = false;
        }
        
        const endTime = performance.now();
        const clientResponseTime = endTime - startTime;
        
        setCurrentRant({
          id: Date.now(),
          rant: `${rant.title}\n\n${rant.content}`,
          poem: poem,
          source: `r/${rant.subreddit} • ${rant.score} upvotes`,
          isAI: isAI,
          cached: data.cached || false,
          responseTime: data.response_time_ms || clientResponseTime,
          generatedAt: data.generated_at
        });
        
        // Update cache stats after successful request
        if (cacheStats) {
          setCacheStats(prev => prev ? {
            ...prev,
            cache_hits: data.cached ? prev.cache_hits + 1 : prev.cache_hits,
            cache_misses: !data.cached ? prev.cache_misses + 1 : prev.cache_misses,
            total_requests: prev.total_requests + 1
          } : null);
        }
        
      } else {
        throw new Error(data.error || 'API returned no rant data');
      }
    } catch (error) {
      console.error('API Error:', error);
      
      // Ultimate fallback to hardcoded rants
      const hardcodedRants: RantData[] = [
        {
          id: 1,
          rant: "WHY DO PEOPLE WALK SO SLOW IN HALLWAYS?! Like seriously, it's not a leisurely stroll through the park, it's a HALLWAY! Some of us have places to be! And don't even get me started on people who suddenly stop right in front of you to check their phone. MOVE TO THE SIDE! This is basic hallway etiquette people!!!",
          poem: "Oh wanderers of the narrow way,\nWhy must you dawdle, why delay?\nThe hallway calls for urgent stride,\nNot meandering side to side.\n\nYour phone can wait, dear friend so slow,\nStep aside and let us go!\nFor some of us have dreams to chase,\nNot snails to match in this small space.",
          isAI: false,
          cached: false
        }
      ];
      
      const randomIndex = Math.floor(Math.random() * hardcodedRants.length);
      const fallbackRant = hardcodedRants[randomIndex];
      setCurrentRant({
        ...fallbackRant,
        source: 'Sample Data (API Unavailable)',
        responseTime: performance.now() - startTime
      });
    }
    
    setSpinCount(prev => prev + 1);
    setIsSpinning(false);
  };

  const copyToClipboard = async (text: string, type: string) => {
    try {
      await navigator.clipboard.writeText(text);
      setCopiedText(type);
      setTimeout(() => setCopiedText(''), 2000);
    } catch (err) {
      console.error('Failed to copy text: ', err);
    }
  };

  const resetApp = () => {
    setCurrentRant(null);
    setSpinCount(0);
    setCopiedText('');
  };

  const togglePerformanceMode = () => {
    setPerformanceMode(prev => prev === 'normal' ? 'fast' : 'normal');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900 p-4">
      {/* Header */}
      <header className="text-center mb-8">
        <h1 className="text-6xl md:text-8xl font-black text-transparent bg-clip-text bg-gradient-to-r from-yellow-400 via-pink-500 to-cyan-400 mb-4 animate-pulse">
          REDDIT RANT ROULETTE
        </h1>
        <p className="text-xl md:text-2xl text-gray-300 font-bold">
          Turn Internet Rage into Poetry with AI! 🎭
        </p>
        
        {/* Spin counter and performance info */}
        <div className="flex justify-center items-center gap-4 mt-4">
          {spinCount > 0 && (
            <div className="text-lg text-yellow-400 font-bold">
              Spins: {spinCount} 🎰
            </div>
          )}
          {currentRant?.responseTime && (
            <div className="text-lg text-cyan-400 font-bold flex items-center gap-1">
              <Clock className="w-4 h-4" />
              {Math.round(currentRant.responseTime)}ms
              {currentRant.cached && <span className="text-green-400">⚡</span>}
            </div>
          )}
        </div>
      </header>

      {/* Performance Mode Toggle */}
      <div className="max-w-4xl mx-auto mb-6 text-center">
        <button
          onClick={togglePerformanceMode}
          className={`px-6 py-2 rounded-full font-bold transition-all duration-200 ${
            performanceMode === 'fast'
              ? 'bg-gradient-to-r from-green-500 to-emerald-500 text-white'
              : 'bg-gradient-to-r from-blue-500 to-purple-500 text-white'
          }`}
        >
          <TrendingUp className="w-4 h-4 inline mr-2" />
          {performanceMode === 'fast' ? '⚡ ULTRA-FAST MODE' : '🚀 NORMAL MODE'}
        </button>
        <p className="text-sm text-gray-400 mt-2">
          {performanceMode === 'fast' 
            ? 'Cache-only for guaranteed instant response' 
            : 'Fast with AI fallback if cache is empty'
          }
        </p>
      </div>

      {/* Main Controls */}
      <div className="max-w-4xl mx-auto mb-8">
        <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
          <button
            onClick={spinRant}
            disabled={isSpinning}
            className={`
              px-8 py-4 text-2xl md:text-3xl font-black rounded-full
              bg-gradient-to-r from-pink-500 to-yellow-500 text-white
              shadow-2xl transform transition-all duration-200
              hover:scale-110 hover:shadow-pink-500/50
              active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed
              ${isSpinning ? 'animate-spin' : 'hover:animate-bounce'}
            `}
          >
            {isSpinning ? (
              <Shuffle className="w-8 h-8 mx-4" />
            ) : (
              <>
                <Zap className="w-8 h-8 inline mr-2" />
                SPIN THE RANT!
                <Zap className="w-8 h-8 inline ml-2" />
              </>
            )}
          </button>
          
          {currentRant && (
            <button
              onClick={resetApp}
              className="px-6 py-3 text-lg font-bold rounded-full bg-gray-700 hover:bg-gray-600 text-white transition-colors duration-200 shadow-lg"
            >
              <RotateCcw className="w-5 h-5 inline mr-2" />
              Reset
            </button>
          )}
        </div>
      </div>

      {/* Content Area */}
      {currentRant && (
        <div className="max-w-6xl mx-auto grid md:grid-cols-2 gap-8">
          {/* Original Rant */}
          <div className="bg-gradient-to-br from-red-600 to-orange-600 rounded-3xl p-6 shadow-2xl transform hover:scale-105 transition-transform duration-300">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-3xl font-black text-white flex items-center">
                🤬 THE RANT
              </h2>
              <button
                onClick={() => copyToClipboard(currentRant.rant, 'rant')}
                className="p-2 bg-white/20 hover:bg-white/30 rounded-full transition-colors duration-200"
                title="Copy rant"
              >
                <Copy className="w-5 h-5 text-white" />
              </button>
            </div>
            <div className="bg-black/20 rounded-2xl p-4 backdrop-blur-sm">
              <p className="text-white text-lg leading-relaxed font-medium">
                {currentRant.rant}
              </p>
            </div>
            {currentRant.source && (
              <p className="text-yellow-300 text-sm mt-2 font-bold">
                📍 Source: {currentRant.source}
              </p>
            )}
            {/* Performance indicators */}
            <div className="flex gap-2 mt-2">
              {currentRant.cached && (
                <span className="text-green-300 text-xs font-bold bg-green-500/20 px-2 py-1 rounded">
                  ⚡ CACHED
                </span>
              )}
              {currentRant.responseTime && (
                <span className="text-cyan-300 text-xs font-bold bg-cyan-500/20 px-2 py-1 rounded">
                  🚀 {Math.round(currentRant.responseTime)}ms
                </span>
              )}
            </div>
            {copiedText === 'rant' && (
              <p className="text-yellow-300 text-sm mt-2 font-bold animate-pulse">
                ✨ Rant copied to clipboard!
              </p>
            )}
          </div>

          {/* AI Poem */}
          <div className="bg-gradient-to-br from-emerald-600 to-teal-600 rounded-3xl p-6 shadow-2xl transform hover:scale-105 transition-transform duration-300">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-3xl font-black text-white flex items-center">
                {currentRant.isAI ? '🤖 AI POEM' : '🎭 THE POEM'}
              </h2>
              <button
                onClick={() => copyToClipboard(currentRant.poem, 'poem')}
                className="p-2 bg-white/20 hover:bg-white/30 rounded-full transition-colors duration-200"
                title="Copy poem"
              >
                <Copy className="w-5 h-5 text-white" />
              </button>
            </div>
            <div className="bg-black/20 rounded-2xl p-4 backdrop-blur-sm">
              <p className="text-white text-lg leading-relaxed font-medium whitespace-pre-line italic">
                {currentRant.poem}
              </p>
            </div>
            {currentRant.isAI && (
              <p className="text-cyan-300 text-sm mt-2 font-bold">
                ✨ Generated by Mistral-7B AI
              </p>
            )}
            {!currentRant.isAI && (
              <p className="text-yellow-300 text-sm mt-2 font-bold">
                📝 Template-generated (AI unavailable)
              </p>
            )}
            {currentRant.generatedAt && (
              <p className="text-gray-300 text-xs mt-1">
                Generated: {new Date(currentRant.generatedAt).toLocaleTimeString()}
              </p>
            )}
            {copiedText === 'poem' && (
              <p className="text-yellow-300 text-sm mt-2 font-bold animate-pulse">
                ✨ Poem copied to clipboard!
              </p>
            )}
          </div>
        </div>
      )}

      {/* Loading State */}
      {isSpinning && (
        <div className="max-w-4xl mx-auto text-center">
          <div className="bg-gradient-to-r from-purple-600 to-blue-600 rounded-3xl p-8 shadow-2xl">
            <div className="animate-spin w-16 h-16 border-4 border-white border-t-transparent rounded-full mx-auto mb-4"></div>
            <p className="text-2xl font-black text-white">
              🎰 SPINNING THE WHEEL OF RAGE... 🎰
            </p>
            <p className="text-lg text-gray-200 mt-2">
              {performanceMode === 'fast' ? '⚡ Ultra-fast mode...' : '🤖 AI is crafting your poetry...'}
            </p>
          </div>
        </div>
      )}

      {/* Instructions */}
      {!currentRant && !isSpinning && (
        <div className="max-w-4xl mx-auto text-center">
          <div className="bg-gradient-to-r from-indigo-600 to-purple-600 rounded-3xl p-8 shadow-2xl">
            <h3 className="text-3xl font-black text-white mb-4">
              🎲 Ready to Transform Rage into Art? 🎲
            </h3>
            <p className="text-xl text-gray-200 font-medium mb-4">
              Click the button above to generate a random internet rant and watch AI transform it into beautiful poetry!
            </p>
            <p className="text-lg text-gray-300 font-medium">
              🤖 Powered by Mistral-7B AI • 📚 Live Reddit data • ⚡ High-performance caching
            </p>
          </div>
        </div>
      )}

      {/* Footer */}
      <footer className="text-center mt-12 text-gray-400">
        <p className="text-lg font-bold">
          Made with 💀, ☕, and 🤖 for maximum internet chaos
        </p>
      </footer>
    </div>
  );
}

export default App;