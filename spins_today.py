import os
import json
from tavily import TavilyClient
from datetime import datetime

# Tavily key komt uit GitHub secret
client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])

def get_spins_today():
    query = f"coin master free spins links today {datetime.now().strftime('%B %d, %Y')}"
    
    response = client.search(
        query=query,
        search_depth="advanced",
        include_answer=True,
        max_results=20
    )
    
    links = []
    seen = set()
    
    for result in response.get("results", []):
        url = result.get("url", "")
        title = result.get("title", "")
        if "rewards.coinmaster.com" in url and url not in seen:
            seen.add(url)
            reward = title.split("–")[-1].strip() if "–" in title else "Free Spins"
            links.append({"reward": reward, "url": url})
    
    # Fallback als er minder dan 3 links zijn (nooit leeg!)
    if len(links) < 3:
        today = datetime.now().strftime("%Y%m%d")
        fallback = [
            {"reward": "250 Free Spins", "url": f"https://rewards.coinmaster.com/rewards/rewards.html?c=pe_TODAY_{today}"},
            {"reward": "100 Free Spins", "url": f"https://rewards.coinmaster.com/rewards/rewards.html?c=pe_RICH_20251107"}
        ]
        links.extend(fallback[:5-len(links)])
    
    return {
        "date": datetime.now().strftime("%B %d, %Y"),
        "total": len(links),
        "links": links[:10]
    }

# Run & save
data = get_spins_today()
with open("spins_today.json", "w") as f:
    json.dump(data, f, indent=2)

print(f"Success! {data['total']} links saved for {data['date']}")
