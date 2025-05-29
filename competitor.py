import requests
from bs4 import BeautifulSoup
import urllib.parse

def get_competitors_from_google(ticker: str, max_competitors: int = 4):
    """
    Scrape Google search results for competitors of a company based on ticker,
    extracting competitor names from elements with class 'FZPZX q8U8x tNxQIb PZPZlf'.

    Args:
        ticker (str): Stock ticker or company name keyword, e.g. "AAPL", "WIPRO".
        max_competitors (int): Max number of competitor names to return.

    Returns:
        List[str]: List of competitor names extracted from Google search page.
    """
    query = f"{ticker} ltd competitors"
    encoded_query = urllib.parse.quote_plus(query)
    google_search_url = f"https://www.google.com/search?q={encoded_query}"

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/114.0.0.0 Safari/537.36"
        )
    }

    try:
        response = requests.get(google_search_url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Find competitor names by exact class
        competitor_elements = soup.find_all(class_="FZPZX q8U8x tNxQIb PZPZlf")

        competitors = []
        for elem in competitor_elements:
            text = elem.get_text(strip=True)
            if text and text.lower() != ticker.lower() and text not in competitors:
                competitors.append(text)
            if len(competitors) >= max_competitors:
                break

        return competitors

    except Exception as e:
        print(f"Error scraping Google competitors for '{ticker}': {e}")
        return []

# Example usage:
if __name__ == "__main__":
    ticker = "AAPL"  # Change ticker as needed
    competitors = get_competitors_from_google(ticker)
    print(f"Top competitors for {ticker}: {competitors}")
