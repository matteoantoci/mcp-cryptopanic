
import requests
from mcp.server.fastmcp import FastMCP
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("CRYPTOPANIC_API_KEY")

mcp = FastMCP("cryptopanic-api")

@mcp.tool()
def get_crypto_news(
    kind: str = "news",
    num_pages: int = 1,
) -> str:
    """Fetches crypto posts (news or media) from CryptoPanic. Returns a concatenated string of post titles.

    Args:
        kind: Filter posts by type. Available values: 'news' or 'media'. Default: 'news'.
        num_pages: Number of pages to fetch. Each page contains multiple posts.

    Returns:
        A concatenated string of post titles.
    """
    news = fetch_crypto_news(kind, num_pages)  # Note: fetch_crypto_news is not defined in the provided code, assuming it exists elsewhere or needs implementation.
    readable = concatenate_news(news)
    return readable


@mcp.tool()
def get_filtered_news(
    kind: str = "news",
    num_pages: int = 1,
    currencies: str = None,
    filter: str = None,
    regions: str = None,
    public: bool = True,
) -> str:
    """Fetches crypto posts from CryptoPanic with various filtering options. Returns a concatenated string of post titles.

    Args:
        kind: Filter posts by type. Available values: 'news' or 'media'. Default: 'news'.
        num_pages: Number of pages to fetch. Each page contains multiple posts.
        currencies: Filter by currency. Comma-separated currency codes (e.g., 'BTC,ETH'). Max 50.
        filter: Apply UI filters. Available values: 'rising', 'hot', 'bullish', 'bearish', 'important', 'saved', 'lol'.
        regions: Filter by region. Comma-separated region codes (e.g., 'en,de'). Default: 'en'. Available: en, de, nl, es, fr, it, pt, ru, tr, ar, cn, jp, ko.
        public: Set to 'true' for public API access (generic posts), 'false' for private access (uses user settings).

    Returns:
        A concatenated string of post titles matching the filters.
    """
    all_news = []
    for page in range(1, num_pages + 1):
        news_items = fetch_filtered_news_page(kind, page, currencies, filter, regions, public)
        if not news_items:
            break
        all_news.extend(news_items)
    return concatenate_news(all_news)


def fetch_filtered_news_page(kind, page, currencies, filter, regions, public):
    """Helper function to fetch a single page of filtered news."""
    try:
        url = "https://cryptopanic.com/api/v1/posts/"
        params = {
            "auth_token": API_KEY,
            "kind": kind,
            "page": page,
            "public": "true" if public else "false"
        }
        if currencies:
            params["currencies"] = currencies
        if filter:
            params["filter"] = filter
        if regions:
            params["regions"] = regions
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        return response.json().get("results", [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching filtered news page {page}: {e}")  # Log error
        return []
    except Exception as e:
        print(f"An unexpected error occurred in fetch_filtered_news_page: {e}")  # Log unexpected errors
        return []


@mcp.tool()
def get_post_details(
    post_id: str  # The unique identifier of the post to retrieve.
) -> dict:
    """Retrieves details for a specific CryptoPanic post by its ID."""
    try:
        url = f"https://cryptopanic.com/api/v1/posts/{post_id}/"
        params = {"auth_token": API_KEY}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching post details for {post_id}: {e}")
        return {}
    except Exception as e:
        print(f"An unexpected error occurred in get_post_details: {e}")
        return {}


@mcp.tool()
def vote_post(
    post_id: str,  # The unique identifier of the post to vote on.
    vote: str  # The type of vote to cast (e.g., 'important', 'like', 'dislike', 'lol', 'saved', 'toxic').
) -> dict:
    """Submits a vote for a specific CryptoPanic post."""
    try:
        url = f"https://cryptopanic.com/api/v1/posts/{post_id}/vote/"
        params = {"auth_token": API_KEY}
        # Ensure vote is one of the allowed values if known, otherwise pass through
        data = {"vote": vote}
        response = requests.post(url, params=params, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error voting on post {post_id}: {e}")
        return {}
    except Exception as e:
        print(f"An unexpected error occurred in vote_post: {e}")
        return {}


@mcp.tool()
def add_to_portfolio(
    currency: str  # The currency code (e.g., 'BTC', 'ETH') to add to the portfolio.
) -> dict:
    """Adds a specified currency to the user's CryptoPanic portfolio."""
    try:
        url = "https://cryptopanic.com/api/v1/portfolio/add/"
        params = {"auth_token": API_KEY}
        data = {"currency": currency}
        response = requests.post(url, params=params, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error adding {currency} to portfolio: {e}")
        return {}
    except Exception as e:
        print(f"An unexpected error occurred in add_to_portfolio: {e}")
        return {}


@mcp.tool()
def remove_from_portfolio(
    currency: str  # The currency code (e.g., 'BTC', 'ETH') to remove from the portfolio.
) -> dict:
    """Removes a specified currency from the user's CryptoPanic portfolio."""
    try:
        url = "https://cryptopanic.com/api/v1/portfolio/remove/"
        params = {"auth_token": API_KEY}
        data = {"currency": currency}
        response = requests.post(url, params=params, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error removing {currency} from portfolio: {e}")
        return {}
    except Exception as e:
        print(f"An unexpected error occurred in remove_from_portfolio: {e}")
        return {}


@mcp.tool()
def get_portfolio_news(
    num_pages: int = 1  # Number of pages to fetch. Each page contains multiple posts.
) -> str:
    """Fetches news posts related to the currencies in the user's CryptoPanic portfolio. Returns a concatenated string of post titles."""
    all_news = []
    for page in range(1, num_pages + 1):
        news_items = fetch_portfolio_news_page(page)
        if not news_items:
            break
        all_news.extend(news_items)
    return concatenate_news(all_news)


def fetch_portfolio_news_page(page):
    """Helper function to fetch a single page of portfolio news."""
    try:
        url = "https://cryptopanic.com/api/v1/portfolio/"
        params = {"auth_token": API_KEY, "page": page}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json().get("results", [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching portfolio news page {page}: {e}")
        return []
    except Exception as e:
        print(f"An unexpected error occurred in fetch_portfolio_news_page: {e}")
        return []


@mcp.tool()
def get_portfolio_summary() -> dict:
    """Retrieves a summary of the user's CryptoPanic portfolio."""
    try:
        url = "https://cryptopanic.com/api/v1/portfolio/summary/"
        params = {"auth_token": API_KEY}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching portfolio summary: {e}")
        return {}
    except Exception as e:
        print(f"An unexpected error occurred in get_portfolio_summary: {e}")
        return {}


@mcp.tool()
def get_portfolio_history() -> dict:
    """Retrieves the historical data for the user's CryptoPanic portfolio."""
    try:
        url = "https://cryptopanic.com/api/v1/portfolio/history/"
        params = {"auth_token": API_KEY}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching portfolio history: {e}")
        return {}
    except Exception as e:
        print(f"An unexpected error occurred in get_portfolio_history: {e}")
        return {}


@mcp.tool()
def list_portfolio_alerts() -> dict:
    """Lists all active price alerts set for the user's CryptoPanic portfolio."""
    try:
        url = "https://cryptopanic.com/api/v1/portfolio/alerts/"
        params = {"auth_token": API_KEY}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error listing portfolio alerts: {e}")
        return {}
    except Exception as e:
        print(f"An unexpected error occurred in list_portfolio_alerts: {e}")
        return {}


@mcp.tool()
def add_portfolio_alert(
    currency: str,  # The currency code (e.g., 'BTC', 'ETH') for the alert.
    price: float,  # The target price for the alert.
    direction: str  # The direction for the alert trigger. Must be 'up' or 'down'.
) -> dict:
    """Adds a new price alert for a specific currency in the user's CryptoPanic portfolio."""
    try:
        url = "https://cryptopanic.com/api/v1/portfolio/alerts/add/"
        params = {"auth_token": API_KEY}
        if direction not in ['up', 'down']:
            raise ValueError("Direction must be 'up' or 'down'")
        data = {
            "currency": currency,
            "price": price,
            "direction": direction
        }
        response = requests.post(url, params=params, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error adding portfolio alert for {currency}: {e}")
        return {}
    except ValueError as e:
        print(f"Invalid input for add_portfolio_alert: {e}")
        return {"error": str(e)}
    except Exception as e:
        print(f"An unexpected error occurred in add_portfolio_alert: {e}")
        return {}


@mcp.tool()
def remove_portfolio_alert(
    alert_id: str  # The unique identifier of the alert to remove.
) -> dict:
    """Removes a specific price alert from the user's CryptoPanic portfolio."""
    try:
        url = "https://cryptopanic.com/api/v1/portfolio/alerts/remove/"
        params = {"auth_token": API_KEY}
        data = {"id": alert_id}  # API expects 'id' based on trial and error, not 'alert_id'
        response = requests.post(url, params=params, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error removing portfolio alert {alert_id}: {e}")
        return {}
    except Exception as e:
        print(f"An unexpected error occurred in remove_portfolio_alert: {e}")
        return {}


def concatenate_news(news_items):
    """Helper function to format a list of news items into a readable string."""
    concatenated_text = ""
    if not news_items:
        return "No news items found."
    for idx, news in enumerate(news_items):
        title = news.get("title", "No Title")
        concatenated_text += f"- {title}\n"

    return concatenated_text.strip()


if __name__ == "__main__":
    mcp.run(transport="stdio")
