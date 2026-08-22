import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

GNEWS_API_KEY = os.getenv("GNEWS_API_KEY")
BASE_URL = "https://gnews.io/api/v4/search"


def search_news(keyword):
    """
    Fetch the latest 5 news articles from GNews.

    Returns:
    [
        {
            "title": "...",
            "source": "...",
            "published": "...",
            "description": "...",
            "link": "..."
        }
    ]
    """

    if not keyword.strip():
        return []

    if not GNEWS_API_KEY:
        print("GNEWS_API_KEY not found.")
        return []

    params = {
        "q": keyword,
        "lang": "en",
        "max": 5,
        "apikey": GNEWS_API_KEY
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=15)
        response.raise_for_status()

        data = response.json()

        articles = []

        for article in data.get("articles", []):
            articles.append({
                "title": article.get("title", ""),
                "source": article.get("source", {}).get("name", ""),
                "published": article.get("publishedAt", ""),
                "description": article.get("description", ""),
                "link": article.get("url", "")
            })

        return articles

    except requests.exceptions.RequestException as e:
        print(f"GNews API Error: {e}")
        return []

    except Exception as e:
        print(f"Unexpected Error: {e}")
        return []