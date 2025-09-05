from sqlalchemy.orm import Session
from sqlalchemy import func
from models import Dim_stocks, Fak_stocks, Portfolio_items
from database import SessionLocal
from datetime import date

def get_teams():
    """
    Fetches all teams (stocks) and their current prices from the database.
    This now joins Dim_stocks with Fak_stocks to get the current price.
    """
    db: Session = SessionLocal()
    try:
        today = date.today()
        # Join Dim_stocks and Fak_stocks to get the current price
        # Assuming one team has one stock for now.
        # A real implementation might need more details in Dim_stocks (like team name).
        teams_with_price = db.query(
            Dim_stocks.stock_id,
            Fak_stocks.price
        ).join(
            Fak_stocks,
            Dim_stocks.stock_id == Fak_stocks.stock_id
        ).filter(
            Fak_stocks.valid_from <= today,
            Fak_stocks.valid_to >= today
        ).all()

        # This is a simplified representation. We'd need a team name in Dim_stocks.
        # For now, I'll use the stock_id as the name.
        return [
            {
                'id': stock_id,
                'name': f"Team {stock_id}", # Placeholder name
                'played': 0, 'won': 0, 'drawn': 0, 'lost': 0, 'points': 0, # No performance data in new model
                'price': price
            } for stock_id, price in teams_with_price
        ]
    finally:
        db.close()

def get_portfolio(user_id: int):
    """
    Fetches the portfolio for a given user using the new dimensional model.
    """
    db: Session = SessionLocal()
    try:
        today = date.today()
        
        # Get user's portfolio items
        portfolio_items = db.query(Portfolio_items).filter(Portfolio_items.user_id == user_id).all()

        if not portfolio_items:
            return {'cash': 0.0, 'holdings': [], 'total_value': 0.0} # Assuming no cash info in new model

        holdings_data = []
        total_holdings_value = 0

        for item in portfolio_items:
            # Get the current price for each stock in the portfolio
            current_stock_price = db.query(Fak_stocks.price).filter(
                Fak_stocks.stock_id == item.stock_id,
                Fak_stocks.valid_from <= today,
                Fak_stocks.valid_to >= today
            ).scalar()

            if current_stock_price:
                # Assuming 'shares' is missing, so defaulting to 1
                shares = 1 # Placeholder, as Portfolio_items doesn't have a quantity
                value = shares * current_stock_price
                total_holdings_value += value
                holdings_data.append({
                    'name': f"Team {item.stock_id}", # Placeholder name
                    'shares': shares,
                    'price': current_stock_price,
                    'value': value
                })
        
        # The new model doesn't have a cash table, so cash is assumed to be 0
        cash = 0.0
        return {
            'cash': cash,
            'holdings': holdings_data,
            'total_value': cash + total_holdings_value
        }
    finally:
        db.close()