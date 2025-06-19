#!/usr/bin/env python3
"""
Performance Testing Script for Reddit Rant Roulette Cache System
Tests and compares performance between cached and non-cached endpoints
"""
import requests
import time
import statistics
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "http://localhost:5001"

class PerformanceTester:
    def __init__(self):
        self.results = {
            'cached_endpoint': [],
            'normal_endpoint': [],
            'non_cached_generation': []
        }
    
    def test_endpoint_performance(self, endpoint, num_requests=10, max_workers=5):
        """Test an endpoint with multiple concurrent requests"""
        print(f"\n🧪 Testing {endpoint} with {num_requests} requests...")
        
        def make_request():
            start_time = time.time()
            try:
                response = requests.get(f"{BASE_URL}{endpoint}", timeout=30)
                end_time = time.time()
                
                response_time = (end_time - start_time) * 1000  # Convert to ms
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('success'):
                        return {
                            'response_time': response_time,
                            'cached': data.get('cached', False),
                            'is_ai': data.get('is_ai', False),
                            'backend_time': data.get('response_time_ms', 0),
                            'success': True
                        }
                
                return {
                    'response_time': response_time,
                    'success': False,
                    'error': response.text[:100] if response.text else 'Unknown error'
                }
                
            except Exception as e:
                end_time = time.time()
                return {
                    'response_time': (end_time - start_time) * 1000,
                    'success': False,
                    'error': str(e)
                }
        
        # Execute requests concurrently
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(make_request) for _ in range(num_requests)]
            results = [future.result() for future in as_completed(futures)]
        
        return results
    
    def test_cache_warming(self, count=5):
        """Test manual cache warming"""
        print(f"\n🔥 Testing cache warming with {count} items...")
        
        start_time = time.time()
        try:
            response = requests.post(f"{BASE_URL}/api/cache/warm", 
                                   json={"count": count}, 
                                   timeout=60)
            end_time = time.time()
            
            if response.status_code == 200:
                data = response.json()
                warming_time = (end_time - start_time) * 1000
                
                print(f"✅ Cache warming completed in {warming_time:.2f}ms")
                print(f"   Generated: {data.get('generated', 0)}/{data.get('requested', 0)} items")
                return True
            else:
                print(f"❌ Cache warming failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Cache warming error: {e}")
            return False
    
    def get_cache_stats(self):
        """Get current cache statistics"""
        try:
            response = requests.get(f"{BASE_URL}/api/cache/stats", timeout=10)
            if response.status_code == 200:
                return response.json().get('cache_stats', {})
            return None
        except Exception as e:
            print(f"❌ Error getting cache stats: {e}")
            return None
    
    def run_comprehensive_test(self):
        """Run a comprehensive performance test suite"""
        print("🚀 Starting Comprehensive Performance Test Suite")
        print("=" * 60)
        
        # Check if server is running
        try:
            response = requests.get(f"{BASE_URL}/api/health", timeout=5)
            if response.status_code != 200:
                print("❌ Server not responding. Please start the Flask app first.")
                return
        except:
            print("❌ Cannot connect to server. Please start the Flask app on port 5001.")
            return
        
        # Get initial cache stats
        initial_stats = self.get_cache_stats()
        if initial_stats:
            print(f"📊 Initial cache size: {initial_stats.get('cache_size', 0)}")
        
        # Test 1: Warm the cache first
        print("\n" + "=" * 60)
        print("🔥 TEST 1: Cache Warming")
        self.test_cache_warming(10)
        
        # Wait for cache to populate
        print("⏳ Waiting 5 seconds for cache to populate...")
        time.sleep(5)
        
        # Test 2: Ultra-fast cached endpoint
        print("\n" + "=" * 60)
        print("⚡ TEST 2: Ultra-Fast Cached Endpoint")
        cached_results = self.test_endpoint_performance('/api/rant-and-poem-fast', 20, 10)
        
        # Test 3: Normal endpoint with fallback
        print("\n" + "=" * 60)
        print("🚀 TEST 3: Normal Endpoint (with fallback)")
        normal_results = self.test_endpoint_performance('/api/rant-and-poem', 15, 5)
        
        # Test 4: Individual poem generation (slowest)
        print("\n" + "=" * 60)
        print("🐌 TEST 4: Individual Poem Generation (non-cached)")
        poem_results = self.test_individual_poem_generation(5)
        
        # Analyze results
        print("\n" + "=" * 60)
        print("📊 PERFORMANCE ANALYSIS")
        self.analyze_results(cached_results, normal_results, poem_results)
        
        # Final cache stats
        final_stats = self.get_cache_stats()
        if final_stats:
            print(f"\n📈 Final Cache Statistics:")
            for key, value in final_stats.items():
                print(f"   {key}: {value}")
    
    def test_individual_poem_generation(self, num_requests=5):
        """Test individual poem generation for comparison"""
        print(f"\n🧪 Testing individual poem generation with {num_requests} requests...")
        
        test_rants = [
            "I hate waiting in line at the grocery store! It takes forever!",
            "Why do people drive so slowly in the fast lane?!",
            "My neighbors are SO LOUD! It's 3 AM, stop playing music!",
            "I can't believe how expensive coffee is these days!",
            "People who don't return their shopping carts are the worst!"
        ]
        
        results = []
        for i in range(num_requests):
            rant_text = test_rants[i % len(test_rants)]
            
            start_time = time.time()
            try:
                response = requests.post(f"{BASE_URL}/api/poem", 
                                       json={"rant_text": rant_text}, 
                                       timeout=60)
                end_time = time.time()
                
                response_time = (end_time - start_time) * 1000
                
                if response.status_code == 200:
                    data = response.json()
                    results.append({
                        'response_time': response_time,
                        'success': data.get('success', False),
                        'cached': False,
                        'is_ai': True if data.get('success') else False
                    })
                else:
                    results.append({
                        'response_time': response_time,
                        'success': False,
                        'cached': False
                    })
                    
            except Exception as e:
                end_time = time.time()
                results.append({
                    'response_time': (end_time - start_time) * 1000,
                    'success': False,
                    'error': str(e),
                    'cached': False
                })
            
            print(f"   Request {i+1}/{num_requests}: {results[-1]['response_time']:.2f}ms")
        
        return results
    
    def analyze_results(self, cached_results, normal_results, poem_results):
        """Analyze and display performance comparison"""
        
        def analyze_dataset(results, name):
            if not results:
                return None
            
            successful_results = [r for r in results if r.get('success', False)]
            if not successful_results:
                print(f"❌ {name}: No successful requests")
                return None
            
            response_times = [r['response_time'] for r in successful_results]
            cached_count = sum(1 for r in successful_results if r.get('cached', False))
            ai_count = sum(1 for r in successful_results if r.get('is_ai', False))
            
            analysis = {
                'total_requests': len(results),
                'successful_requests': len(successful_results),
                'success_rate': len(successful_results) / len(results) * 100,
                'avg_response_time': statistics.mean(response_times),
                'median_response_time': statistics.median(response_times),
                'min_response_time': min(response_times),
                'max_response_time': max(response_times),
                'cached_responses': cached_count,
                'ai_responses': ai_count,
                'cache_hit_rate': cached_count / len(successful_results) * 100 if successful_results else 0
            }
            
            print(f"\n📊 {name} Results:")
            print(f"   Total Requests: {analysis['total_requests']}")
            print(f"   Success Rate: {analysis['success_rate']:.1f}%")
            print(f"   Average Response Time: {analysis['avg_response_time']:.2f}ms")
            print(f"   Median Response Time: {analysis['median_response_time']:.2f}ms")
            print(f"   Min/Max Response Time: {analysis['min_response_time']:.2f}ms / {analysis['max_response_time']:.2f}ms")
            if cached_count > 0:
                print(f"   Cache Hit Rate: {analysis['cache_hit_rate']:.1f}%")
            if ai_count > 0:
                print(f"   AI-Generated Responses: {ai_count}/{len(successful_results)}")
            
            return analysis
        
        # Analyze each dataset
        cached_analysis = analyze_dataset(cached_results, "⚡ Ultra-Fast Cached Endpoint")
        normal_analysis = analyze_dataset(normal_results, "🚀 Normal Endpoint")
        poem_analysis = analyze_dataset(poem_results, "🐌 Individual Poem Generation")
        
        # Performance comparison
        print(f"\n🏆 PERFORMANCE COMPARISON:")
        print("=" * 40)
        
        if cached_analysis and normal_analysis:
            speedup_vs_normal = normal_analysis['avg_response_time'] / cached_analysis['avg_response_time']
            print(f"⚡ Cached vs Normal: {speedup_vs_normal:.1f}x faster")
        
        if cached_analysis and poem_analysis:
            speedup_vs_poem = poem_analysis['avg_response_time'] / cached_analysis['avg_response_time']
            print(f"⚡ Cached vs Individual Generation: {speedup_vs_poem:.1f}x faster")
        
        if normal_analysis and poem_analysis:
            speedup_normal_vs_poem = poem_analysis['avg_response_time'] / normal_analysis['avg_response_time']
            print(f"🚀 Normal vs Individual Generation: {speedup_normal_vs_poem:.1f}x faster")
        
        # Performance categories
        def categorize_performance(avg_time):
            if avg_time < 100:
                return "🚀 EXCELLENT (< 100ms)"
            elif avg_time < 500:
                return "✅ GOOD (< 500ms)"
            elif avg_time < 2000:
                return "⚠️ ACCEPTABLE (< 2s)"
            else:
                return "❌ SLOW (> 2s)"
        
        print(f"\n🎯 PERFORMANCE CATEGORIES:")
        if cached_analysis:
            print(f"   Ultra-Fast Cached: {categorize_performance(cached_analysis['avg_response_time'])}")
        if normal_analysis:
            print(f"   Normal Endpoint: {categorize_performance(normal_analysis['avg_response_time'])}")
        if poem_analysis:
            print(f"   Individual Generation: {categorize_performance(poem_analysis['avg_response_time'])}")
        
        print(f"\n💡 RECOMMENDATIONS:")
        if cached_analysis and cached_analysis['avg_response_time'] < 200:
            print("   ✅ Cache system is performing excellently!")
            print("   ✅ Users will experience near-instant responses")
        
        if normal_analysis and normal_analysis['cache_hit_rate'] > 80:
            print("   ✅ High cache hit rate - system is well-optimized")
        elif normal_analysis and normal_analysis['cache_hit_rate'] < 50:
            print("   ⚠️ Low cache hit rate - consider increasing cache size")
        
        if poem_analysis and poem_analysis['avg_response_time'] > 5000:
            print("   ⚠️ Individual poem generation is slow - cache is essential")
        
        print(f"\n🎯 CONCLUSION:")
        if cached_analysis and cached_analysis['avg_response_time'] < 100:
            print("   🏆 Cache system provides EXCELLENT performance improvement!")
            print("   🚀 Users will experience lightning-fast responses")
        else:
            print("   📈 Cache system provides measurable performance improvement")

def main():
    print("🎭 Reddit Rant Roulette - Performance Testing Suite")
    print("=" * 60)
    
    # Check environment
    if not os.getenv('HF_TOKEN'):
        print("⚠️ Warning: HF_TOKEN not found - AI generation may fail")
    
    tester = PerformanceTester()
    tester.run_comprehensive_test()
    
    print(f"\n🎉 Performance testing complete!")
    print("💡 Use this data to optimize your cache settings and server deployment.")

if __name__ == "__main__":
    main() 