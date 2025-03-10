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

def fetch_crypto_news_page(kind: str = "news", page: int = 1): 
  try:
    url = "https://cryptopanic.com/api/v1/posts/"
    params = {
      "auth_token": API_KEY,
      "kind": "news",  # news, analysis, videos
      "regions": "en",  
      "page": page      
    }
    response = requests.get(url, params=params)
    return response.json().get("results", [])
  except:
    return []
        
def fetch_crypto_news(kind: str = "news", num_pages: int = 10):
  all_news = []
  for page in range(1, num_pages + 1):
    print(f"Fetching page {page}...")
    news_items = fetch_crypto_news_page(kind, page)
    if not news_items:
      print(f"No more news found on page {page}. Stopping.")
      break
    all_news.extend(news_items)
  return all_news        

def concatenate_news(news_items):
  concatenated_text = ""
  for idx, news in enumerate(news_items):  # 拼接全部新闻
    title = news.get("title", "No Title")
    concatenated_text += f"- {title}\n"
       
  return concatenated_text.strip()


if __name__ == "__main__":
  mcp.run(transport="stdio")
