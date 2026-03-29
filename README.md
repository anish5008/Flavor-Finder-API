# 🍳 Flavor Finder API

Flavor Finder is a terminal-based tool that helps users discover new meals and manage their grocery needs using real-time data from the Spoonacular API.

## ✨ Features
- **Search by Dish:** Find recipes by name with optional dietary filters (Vegan, Keto, etc.).
- **Search by Ingredients:** Input what you have in your fridge to see what you can cook.
- **Randomizer:** Get a surprise recipe when you don't know what to eat.
- **Nutritional Data:** View macros like Calories, Protein, and Fat for any dish.
- **Local Persistence:** Save your favorite recipes and shopping lists to local `.txt` files.

## 🛠️ Technical Improvements
- **Security:** Uses `python-dotenv` to keep API keys private and out of the source code.
- **Robust Logic:** Features updated error handling for user inputs and API response validation.
- **Data Parsing:** Extracts complex nested JSON data to display clean, step-by-step instructions.
