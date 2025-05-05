# cryptopanic-mcp-server

[![Discord](https://img.shields.io/discord/1353556181251133481?cacheSeconds=3600)](https://discord.gg/aRnuu2eJ)
![GitHub License](https://img.shields.io/github/license/kukapay/blockbeats-mcp)

Provide the latest cryptocurrency news to AI agents, powered by [CryptoPanic](https://cryptopanic.com/).

## Tools

The server implements the following tools:

```python
get_crypto_news(kind: str = "news", num_pages: int = 1) -> str
```
- `kind`: Content type (news, analysis, videos)
- `num_pages`: Number of pages to fetch (default: 1, max: 10)

```python
get_filtered_news(
    kind: str = "news",
    num_pages: int = 1,
    currencies: str = None,
    filter: str = None,
    regions: str = None,
    public: bool = True
) -> str
```
- Fetch news with advanced filters.
- `currencies`: Comma-separated list of currency symbols (e.g., BTC,ETH).
- `filter`: Filter type (hot, rising, bullish, bearish, important, saved).
- `regions`: Comma-separated list of regions (e.g., en, us).
- `public`: Whether to fetch only public news (default: True).

```python
get_post_details(post_id: str) -> dict
```
- Get detailed information for a specific post by ID.

```python
vote_post(post_id: str, vote: str) -> dict
```
- Vote on a post.
- `vote`: Type of vote (important, like, dislike, etc.).

```python
add_to_portfolio(currency: str) -> dict
```
- Add a currency to the user's portfolio.

```python
remove_from_portfolio(currency: str) -> dict
```
- Remove a currency from the user's portfolio.

```python
get_portfolio_news(num_pages: int = 1) -> str
```
- Get news related to the user's portfolio.

```python
get_portfolio_summary() -> dict
```
- Get a summary of the user's portfolio.

```python
get_portfolio_history() -> dict
```
- Get historical data of the user's portfolio.

```python
list_portfolio_alerts() -> dict
```
- List all price alerts set on the portfolio.

```python
add_portfolio_alert(currency: str, price: float, direction: str) -> dict
```
- Add a price alert.
- `direction`: "up" or "down".

```python
remove_portfolio_alert(alert_id: str) -> dict
```
- Remove a price alert by its ID.

Example Output for `get_crypto_news`:

```
- Bitcoin Breaks $60k Resistance Amid ETF Optimism
- Ethereum Layer 2 Solutions Gain Traction
- New Crypto Regulations Proposed in EU
- ...
```

## Configuration

- CryptoPanic API key: get one [here](https://cryptopanic.com/developers/api/)
- Add a server entry to your configuration file:

```
"mcpServers": { 
  "mcp-cryptopanic": { 
    "command": "uv", 
    "args": [ 
      "--directory", "/your/path/to/mcp-cryptopanic"", 
      "run", 
      "main.py" 
    ], 
    "env": { 
      "CRYPTOPANIC_API_KEY": "" 
    } 
  } 
}
```

## License

MIT License - see `LICENSE` file
