from flask import Flask, render_template
from data_access import get_teams, get_portfolio
from database import engine, Base
from models import * # Import models to ensure they are registered with Base

app = Flask(__name__)

# Create database tables if they don't exist
# In a production environment, you might use Alembic for migrations
Base.metadata.create_all(bind=engine)


# Placeholder for the current user's ID.
# In a real app, this would come from a login/session system.
CURRENT_USER_ID = 1

@app.route('/')
def league():
    """Displays the league standings by fetching data from the database."""
    teams = get_teams()
    # Sort teams by points for the league table
    league_teams = sorted(teams, key=lambda x: x['points'], reverse=True)
    return render_template('index.html', active_tab='league', teams=league_teams)

@app.route('/portfolio')
def portfolio_view():
    """Displays the current user's portfolio from the database."""
    portfolio_data = get_portfolio(CURRENT_USER_ID)
    return render_template('index.html', active_tab='portfolio', portfolio=portfolio_data)

@app.route('/market')
def market():
    """Displays the stock market with all teams from the database."""
    teams = get_teams()
    return render_template('index.html', active_tab='market', teams=teams)

if __name__ == '__main__':
    # In a real application, you would configure host and port,
    # and turn off debug mode in production.
    app.run(debug=True)