import http.client
import json
import urllib.parse

def get_reddit_hot(subreddit, limit=10):
    conn = http.client.HTTPSConnection("old.reddit.com")
    headers = {"User-Agent": "neta-trend-collector/1.0 (trend analysis tool)"}
    path = f"/r/{subreddit}/hot.json?t=day&limit={limit}"
    
    try:
        conn.request("GET", path, headers=headers)
        res = conn.getresponse()
        data = json.loads(res.read().decode("utf-8"))
        
        results = []
        for child in data.get('data', {}).get('children', []):
            item = child.get('data', {})
            results.append({
                "title": item.get('title'),
                "ups": item.get('ups'),
                "num_comments": item.get('num_comments'),
                "url": f"https://www.reddit.com{item.get('permalink')}",
                "subreddit": subreddit
            })
        return results
    except Exception as e:
        return [{"error": str(e), "subreddit": subreddit}]
    finally:
        conn.close()

subreddits = [
    "netsec", "cybersecurity",
    "OpenAI", "LocalLLaMA", "ClaudeCode",
    "programming", "technology",
    "opensource", "indiehackers", "webdev", "javascript",
    "cscareerquestions", "productivity"
]

all_results = {}
for sub in subreddits:
    with open("reddit_results.json", "w", encoding="utf-8") as f:
    json.dump(all_results, f, ensure_ascii=False, indent=2)
print("SUCCESS: Results saved to reddit_results.json")
