import requests
from mcp.server.fastmcp import FastMCP
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("CRYPTOPANIC_API_KEY")

mcp = FastMCP("crypto news")
        
@mcp.tool()
def get_crypto_news(kind: str = "news", num_pages: int = 1) -> str:
  news = fetch_crypto_news(kind, num_pages)
  readable = concatenate_news(news)
  return readable

@mcp.tool()
def get_filtered_news(
    kind: str = "news",
    num_pages: int = 1,
    currencies: str = None,
    filter: str = None,
    regions: str = None,
    public: bool = True
) -> str:
  all_news = []
  for page in range(1, num_pages + 1):
    news_items = fetch_filtered_news_page(kind, page, currencies, filter, regions, public)
    if not news_items:
      break
    all_news.extend(news_items)
  return concatenate_news(all_news)

def fetch_filtered_news_page(kind, page, currencies, filter, regions, public):
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
    return response.json().get("results", [])
  except:
    return []

@mcp.tool()
def get_post_details(post_id: str) -> dict:
  try:
    url = f"https://cryptopanic.com/api/v1/posts/{post_id}/"
    params = {"auth_token": API_KEY}
    response = requests.get(url, params=params)
    return response.json()
  except:
    return {}

@mcp.tool()
def vote_post(post_id: str, vote: str) -> dict:
  try:
    url = f"https://cryptopanic.com/api/v1/posts/{post_id}/vote/"
    params = {"auth_token": API_KEY}
    data = {"vote": vote}  # vote can be important, like, dislike, etc.
    response = requests.post(url, params=params, json=data)
    return response.json()
  except:
    return {}

@mcp.tool()
def add_to_portfolio(currency: str) -> dict:
  try:
    url = "https://cryptopanic.com/api/v1/portfolio/add/"
    params = {"auth_token": API_KEY}
    data = {"currency": currency}
    response = requests.post(url, params=params, json=data)
    return response.json()
  except:
    return {}

@mcp.tool()
def remove_from_portfolio(currency: str) -> dict:
  try:
    url = "https://cryptopanic.com/api/v1/portfolio/remove/"
    params = {"auth_token": API_KEY}
    data = {"currency": currency}
    response = requests.post(url, params=params, json=data)
    return response.json()
  except:
    return {}

@mcp.tool()
def get_portfolio_news(num_pages: int = 1) -> str:
  all_news = []
  for page in range(1, num_pages + 1):
    news_items = fetch_portfolio_news_page(page)
    if not news_items:
      break
    all_news.extend(news_items)
  return concatenate_news(all_news)

def fetch_portfolio_news_page(page):
  try:
    url = "https://cryptopanic.com/api/v1/portfolio/"
    params = {"auth_token": API_KEY, "page": page}
    response = requests.get(url, params=params)
    return response.json().get("results", [])
  except:
    return []

@mcp.tool()
def get_portfolio_summary() -> dict:
  try:
    url = "https://cryptopanic.com/api/v1/portfolio/summary/"
    params = {"auth_token": API_KEY}
    response = requests.get(url, params=params)
    return response.json()
  except:
    return {}

@mcp.tool()
def get_portfolio_history() -> dict:
  try:
    url = "https://cryptopanic.com/api/v1/portfolio/history/"
    params = {"auth_token": API_KEY}
    response = requests.get(url, params=params)
    return response.json()
  except:
    return {}

@mcp.tool()
def list_portfolio_alerts() -> dict:
  try:
    url = "https://cryptopanic.com/api/v1/portfolio/alerts/"
    params = {"auth_token": API_KEY}
    response = requests.get(url, params=params)
    return response.json()
  except:
    return {}

@mcp.tool()
def add_portfolio_alert(currency: str, price: float, direction: str) -> dict:
  try:
    url = "https://cryptopanic.com/api/v1/portfolio/alerts/add/"
    params = {"auth_token": API_KEY}
    data = {
      "currency": currency,
      "price": price,
      "direction": direction  # up or down
    }
    response = requests.post(url, params=params, json=data)
    return response.json()
  except:
    return {}

@mcp.tool()
def remove_portfolio_alert(alert_id: str) -> dict:
  try:
    url = "https://cryptopanic.com/api/v1/portfolio/alerts/remove/"
    params = {"auth_token": API_KEY}
    data = {"id": alert_id}
    response = requests.post(url, params=params, json=data)
    return response.json()
  except:
    return {}

def concatenate_news(news_items):
  concatenated_text = ""
  for idx, news in enumerate(news_items):  # 拼接全部新闻
    title = news.get("title", "No Title")
    concatenated_text += f"- {title}\n"
       
  return concatenated_text.strip()


if __name__ == "__main__":
  mcp.run(transport="stdio")
