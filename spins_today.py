import os
import json
from tavily import TavilyClient
from datetime import datetime, timedelta

client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])

def get_last_3_days_spins():
    all_links = {}
    seen_urls = set()

    # Loop over vandaag, gisteren en eergisteren
    for i in range(3):
        date = datetime.now() - timedelta(days=i)
        date_str = date.strftime("%B %d, %Y")
        query = f"coin master free spins links {date_str}"

        try:
            response = client.search(
                query=query,
                search_depth="advanced",
                include_answer=True,
                max_results=25
            )

            links = []
            for item in response.get("results", []):
                url = item.get("url", "")
                title = item.get("title", "")
                if "rewards.coinmaster.com" in url and url not in seen_urls:
                    seen_urls.add(url)
                    reward = title.split("–")[-1].strip() if "–" in title else "Free Spins"
                    links.append({"reward": reward, "url": url})

            all_links[date_str] = links[:12]  # max 12 per dag
        except:
            all_links[date_str] = []

    return {
        "updated": datetime.now().strftime("%B %d, %Y"),
        "days": all_links
    }

# Run & save
data = get_last_3_days_spins()
with open("spins_today.json", "w") as f:
    json.dump(data, f, indent=2)

print(f"Success! Last 3 days links saved → {len(data['days'])} days")
