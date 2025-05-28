import yfinance as yf
import pandas as pd
import os

def fetch_financial_reports(ticker: str, save_path: str = "reports", period: str = "max", interval: str = "1d"):
    """
    Fetches financial reports and historical stock data for the given ticker and saves them as CSV files.
    
    Args:
        ticker (str): Stock ticker (e.g., "AAPL", "RELIANCE.NS").
        save_path (str): Root directory to save reports.
        period (str): Historical data period, e.g. '1mo', '1y', '5y', 'max' (default 'max').
        interval (str): Data interval, e.g. '1d', '1wk', '1mo' (default '1d').
    """
    try:
        stock = yf.Ticker(ticker)

        # Prepare directory
        company_dir = os.path.join(save_path, ticker)
        os.makedirs(company_dir, exist_ok=True)

        # Fetch and save balance sheet
        bs = stock.balance_sheet
        if not bs.empty:
            bs.T.to_csv(os.path.join(company_dir, "balance_sheet.csv"))

        # Fetch and save income statement
        is_ = stock.financials
        if not is_.empty:
            is_.T.to_csv(os.path.join(company_dir, "income_statement.csv"))

        # Fetch and save cash flow
        cf = stock.cashflow
        if not cf.empty:
            cf.T.to_csv(os.path.join(company_dir, "cash_flow.csv"))


        # ESG Scores (if available)
        sustainability = stock.sustainability
        if sustainability is not None and not sustainability.empty:
            sustainability.to_csv(os.path.join(company_dir, "esg_scores.csv"))

        # Fetch and save historical market data
        hist = stock.history(period=period, interval=interval)
        if not hist.empty:
            hist.to_csv(os.path.join(company_dir, "historical_data.csv"))

        print(f"[✓] Reports and historical data for {ticker} saved to {company_dir}")

    except Exception as e:
        print(f"[✗] Failed to fetch data for {ticker}: {e}")

# ------------------------
# 💡 Example usage
# ------------------------
if __name__ == "__main__":
    tickers = ["AAPL", "RELIANCE.NS"]
    for t in tickers:
        fetch_financial_reports(t)
