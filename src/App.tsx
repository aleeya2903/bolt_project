import  { useState } from 'react';
import { Shuffle, Copy, RotateCcw, Zap } from 'lucide-react';

// Add this new interface for Reddit API responses
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

// Update your existing RantData interface to include source
interface RantData {
  id: number;
  rant: string;
  poem: string;
  source?: string; // Add this line
}


const hardcodedRants: RantData[] = [
  {
    id: 1,
    rant: "WHY DO PEOPLE WALK SO SLOW IN HALLWAYS?! Like seriously, it's not a leisurely stroll through the park, it's a HALLWAY! Some of us have places to be! And don't even get me started on people who suddenly stop right in front of you to check their phone. MOVE TO THE SIDE! This is basic hallway etiquette people!!!",
    poem: "Oh wanderers of the narrow way,\nWhy must you dawdle, why delay?\nThe hallway calls for urgent stride,\nNot meandering side to side.\n\nYour phone can wait, dear friend so slow,\nStep aside and let us go!\nFor some of us have dreams to chase,\nNot snails to match in this small space."
  },
  {
    id: 2,
    rant: "I CANNOT be the only one who thinks pineapple on pizza is actually AMAZING and everyone who disagrees is just following the crowd! It's sweet, it's tangy, it balances the salt from the cheese perfectly! But nooooo, everyone acts like I committed a war crime when I order Hawaiian pizza. IT'S JUST FRUIT, PEOPLE!",
    poem: "Upon the dough of golden wheat,\nLies fruit both tangy and so sweet.\nThe crowd may scream, the masses roar,\nBut pineapple's what pizza's for!\n\nSweet rings of joy on melted cheese,\nA taste that puts my soul at ease.\nLet others judge and point with shame,\nI'll eat my Hawaiian just the same!"
  },
  {
    id: 3,
    rant: "Can we talk about people who don't use turn signals?! IT'S LITERALLY ONE FINGER MOVEMENT! Just flick the little stick! That's it! But apparently it's too much effort for some people. I'm not a mind reader! I don't know if you're turning left, right, or just really bad at staying in your lane!",
    poem: "One finger's flick, one simple motion,\nCould save us all from road commotion.\nBut drivers sail without a sign,\nLeaving chaos in their line.\n\nNo crystal ball have I to see,\nWhich way your car intends to flee.\nSo signal forth, dear road companion,\nAnd end this tragic driving canon!"
  },
  {
    id: 4,
    rant: "STOP LEAVING YOUR DISHES IN THE SINK! It's not a magical fairy kingdom where dishes clean themselves! You used it, you wash it! I'm not your personal dishwasher! And while we're at it, PUT THE TOILET SEAT DOWN! It's called basic human decency!",
    poem: "In kitchen sinks across the land,\nDirty dishes make their stand.\nNo fairy godmother will appear,\nTo make your mess just disappear.\n\nSo wash your plate and clean your cup,\nAnd put that toilet seat back up!\nFor courtesy costs nothing, friend,\nOn this we all can depend."
  },
  {
    id: 5,
    rant: "Why do people blast music on public transportation?! WE DON'T ALL WANT TO HEAR YOUR TERRIBLE PLAYLIST! Get some headphones! They cost like $5! But no, apparently everyone on the bus needs to experience your questionable music taste at maximum volume!",
    poem: "On buses, trains, and subway cars,\nYour music travels near and far.\nBut fellow travelers did not choose,\nTo hear your beats and rhythm blues.\n\nSo spare us from your sonic art,\nAnd keep your playlist close to heart.\nWith headphones snug upon your ears,\nYou'll save us all from musical tears."
  },
  {
    id: 6,
    rant: "PEOPLE WHO CHEW WITH THEIR MOUTH OPEN! It's like listening to a cow eating grass! CLOSE YOUR MOUTH! Were you raised by wolves?! The sound is absolutely disgusting and I can see your food! Nobody wants to witness your digestive process in action!",
    poem: "Oh masters of the open jaw,\nYour chewing breaks decorum's law.\nThe sounds you make while eating food,\nAre really quite incredibly rude.\n\nSo close your lips and chew with grace,\nAnd spare us from your dinner's face.\nFor dining should be seen, not heard,\nThis wisdom should be widely shared."
  },
  {
    id: 7,
    rant: "STOP TALKING DURING MOVIES! I paid $15 to watch this film, not to hear your running commentary! If you want to have a conversation, GO TO A COFFEE SHOP! The rest of us are trying to follow the plot! And PUT YOUR PHONE AWAY! The screen is brighter than the sun!",
    poem: "In theaters dark where stories play,\nSome folks forget the proper way.\nThey chat and text throughout the show,\nWhile others wish that they would go.\n\nSo silence phones and still your tongue,\nLet cinema songs be properly sung.\nFor movies are a sacred space,\nWhere stories unfold with quiet grace."
  },
  {
    id: 8,
    rant: "Why do people take FOREVER at ATMs?! It's not rocket science! Put in your card, enter your PIN, get your money, LEAVE! But no, some people treat it like they're filing their taxes! There's a line of people behind you! HURRY UP!",
    poem: "At ATMs across the nation,\nSome folks cause great frustration.\nThey ponder long at money machines,\nWhile others wait behind the scenes.\n\nSo know your PIN and make it quick,\nDon't make the waiting line feel sick.\nFor banking should be swift and neat,\nTo keep the flow of commerce sweet."
  }
];

function App() {
  const [currentRant, setCurrentRant] = useState<RantData | null>(null);
  const [isSpinning, setIsSpinning] = useState(false);
  const [spinCount, setSpinCount] = useState(0);
  const [copiedText, setCopiedText] = useState<string>('');
  const generatePoem = async (rantText: string): Promise<string> => {
    try {
      return generateSimplePoem(rantText);
    } catch (error) {
      console.error('Poem generation error:', error);
      return generateSimplePoem(rantText);
    }
  };
  
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
    
    try {
      // Fetch real Reddit rant from your API
      const response = await fetch('http://localhost:5001/api/rant');
      const data: RedditRantResponse = await response.json();
      
      if (data.success && data.rant) {
        const rant = data.rant;
        
        // Create a poem using AI
        const poem = await generatePoem(rant.content);
        
        setCurrentRant({
          id: Date.now(),
          rant: `${rant.title}\n\n${rant.content}`,
          poem: poem,
          source: `r/${rant.subreddit} • ${rant.score} upvotes`
        });
      } else {
        throw new Error('API returned no rant data');
      }
    } catch (error) {
      console.error('API Error:', error);
      // Fallback to hardcoded rants
      const randomIndex = Math.floor(Math.random() * hardcodedRants.length);
      const fallbackRant = hardcodedRants[randomIndex];
      setCurrentRant({
        ...fallbackRant,
        source: 'Sample Data'
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

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900 p-4">
      {/* Header */}
      <header className="text-center mb-8">
        <h1 className="text-6xl md:text-8xl font-black text-transparent bg-clip-text bg-gradient-to-r from-yellow-400 via-pink-500 to-cyan-400 mb-4 animate-pulse">
          REDDIT RANT ROULETTE
        </h1>
        <p className="text-xl md:text-2xl text-gray-300 font-bold">
          Turn Internet Rage into Poetry! 🎭
        </p>
        
        {/* Spin counter */}
        {spinCount > 0 && (
          <div className="text-lg text-yellow-400 font-bold mt-4">
            Spins: {spinCount} 🎰
          </div>
        )}
      </header>

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
                🎭 THE POEM
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
              Click the button above to generate a random internet rant and watch it transform into beautiful poetry!
            </p>
            <p className="text-lg text-gray-300 font-medium">
              📚 Featuring curated rants about life's most annoying moments
            </p>
          </div>
        </div>
      )}

      {/* Footer */}
      <footer className="text-center mt-12 text-gray-400">
        <p className="text-lg font-bold">
          Made with 💀 and ☕ for maximum internet chaos
        </p>
      </footer>
    </div>
  );
}

export default App;