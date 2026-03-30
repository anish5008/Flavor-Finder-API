# 🍳 Flavor Finder API (Terminal Edition)

**Flavor Finder** is a text-based (CLI) culinary assistant built entirely in **Python**. It connects to the Spoonacular API to provide real-time recipe data, nutritional information, and kitchen management tools directly in your terminal.

## 💻 Technical Environment
- **Language:** Python 3.x
- **Interface:** Command Line Interface (CLI)
- **Dependencies:** `requests`, `python-dotenv`

## ✨ Features
- **Smart Search:** Find recipes by name or by the ingredients currently in your fridge.
- **Dietary Filtering:** Support for Vegan, Vegetarian, and Keto restrictions.
- **Nutritional Lookup:** Check macros like Calories, Protein, and Fat.
- **Data Persistence:** Automatically generates and updates `shopping_cart.txt`, `favorites.txt`, and `recipes.txt` locally.

## 🚀 How to Run
### Option A: Run from Source (Recommended for Devs)
1. Ensure you have **Python 3** installed.
2. Clone this repository and navigate to the folder.
3. Install requirements: `pip install requests python-dotenv`.
4. Create a `.env` file and add your `SPOONACULAR_API_KEY`.
5. Run the application:
   ```bash
   python main.py
