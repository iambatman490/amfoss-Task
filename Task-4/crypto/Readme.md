1.The Structure (index.html)
    Built the basic layout of the webpage.
    Added a top bar with a search box and a dark/light mode button.
    Added a chart area at the top using an HTML canvas for the price graph.
    Added buttons to change the time range (24H, 7D, 1M, 1Y).
    Added tabs to switch between "All Coins" and "Watchlist".
    Added an empty table where the live coin data will appear.
2. The Design (style.css)
    Used CSS variables for colors so the app can easily switch between Dark and Light mode.
    Styled the layout with modern cards, rounded corners, and clean fonts.
    Made the design responsive so it looks good on both mobile screens and laptops.
    Set green colors for positive price changes and red for negative price changes.
3. The Logic and Live Data (app.js)
    Fetched Live Prices: Used JavaScript fetch() to call the free CoinGecko API and pull the latest 50 cryptocurrencies.
    Built the Table: Looped through the data and added each coin's name, price, 24-hour change, and market cap into the table.
    Added Search: Made the search bar filter the list instantly as the user types.
    Interactive Charts: Integrated Chart.js to draw price trends. When a user clicks a coin or changes the time range, the app fetches historical price data and redraws the graph.
    Watchlist (Favorites): Allowed users to star/favorite coins. Saved these choices in the browser's localStorage so the favorites stay saved even after refreshing the page.
    Theme Switcher: Added a click event on the theme button to toggle data-theme between "dark" and "light".
