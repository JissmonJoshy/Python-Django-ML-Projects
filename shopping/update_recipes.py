import pandas as pd

# Read the CSV file
csv_path = r'static\data\recipes_dataset.csv'
df = pd.read_csv(csv_path)

print(f"Original dataset: {len(df)} recipes")

# Remove duplicates
df_unique = df.drop_duplicates(subset=['name', 'ingredients'], keep='first').reset_index(drop=True)
print(f"After removing duplicates: {len(df_unique)} recipes")

# Add more recipes
new_recipes = [
    {'name': 'Garlic Bread', 'ingredients': 'bread,butter,garlic,parsley'},
    {'name': 'Tacos', 'ingredients': 'tortilla,meat,cheese,lettuce,tomato,sauce'},
    {'name': 'Quesadilla', 'ingredients': 'tortilla,cheese,chicken,peppers,onions'},
    {'name': 'Grilled Cheese', 'ingredients': 'bread,butter,cheese'},
    {'name': 'Mac and Cheese', 'ingredients': 'pasta,cheese,butter,milk'},
    {'name': 'Spaghetti', 'ingredients': 'pasta,tomato sauce,garlic,olive oil'},
    {'name': 'Lasagna', 'ingredients': 'pasta sheets,meat,tomato sauce,cheese,bechamel'},
    {'name': 'Chicken Stir Fry', 'ingredients': 'chicken,vegetables,soy sauce,garlic,ginger'},
    {'name': 'Beef Tacos', 'ingredients': 'beef,tortilla,cheese,salsa,sour cream'},
    {'name': 'Vegetable Curry', 'ingredients': 'vegetables,coconut milk,curry paste,rice'},
    {'name': 'Mushroom Risotto', 'ingredients': 'rice,mushrooms,butter,parmesan,onion,wine'},
    {'name': 'Fish Tacos', 'ingredients': 'fish,tortilla,cabbage,lime,sauce'},
    {'name': 'Chicken Curry', 'ingredients': 'chicken,curry paste,coconut milk,onion,garlic'},
    {'name': 'Spring Rolls', 'ingredients': 'rice paper,vegetables,shrimp,peanut sauce'},
    {'name': 'Pad Thai', 'ingredients': 'rice noodles,shrimp,egg,vegetables,peanuts,lime'},
    {'name': 'Chicken Alfredo', 'ingredients': 'pasta,chicken,cream,parmesan,garlic,butter'},
    {'name': 'Beef Stew', 'ingredients': 'beef,potatoes,carrots,onions,broth'},
    {'name': 'Chow Mein', 'ingredients': 'noodles,chicken,vegetables,soy sauce,garlic'},
    {'name': 'Enchiladas', 'ingredients': 'tortillas,chicken,cheese,red sauce,sour cream'},
    {'name': 'Falafel', 'ingredients': 'chickpeas,garlic,spices,flour,oil'},
    {'name': 'Hummus', 'ingredients': 'chickpeas,tahini,lemon,garlic,olive oil'},
    {'name': 'Greek Salad', 'ingredients': 'tomatoes,cucumber,feta,olives,olive oil,lemon'},
    {'name': 'Caesar Salad', 'ingredients': 'lettuce,croutons,parmesan,caesar dressing'},
    {'name': 'Caprese Salad', 'ingredients': 'tomatoes,mozzarella,basil,olive oil,balsamic'},
    {'name': 'Thai Green Curry', 'ingredients': 'chicken,green curry paste,coconut milk,vegetables'},
    {'name': 'Meatballs', 'ingredients': 'ground meat,breadcrumbs,egg,garlic,spices'},
    {'name': 'Chicken Nuggets', 'ingredients': 'chicken,breadcrumbs,egg,oil'},
    {'name': 'Fish and Chips', 'ingredients': 'fish,potatoes,flour,oil,salt'},
    {'name': 'Shrimp Scampi', 'ingredients': 'shrimp,garlic,butter,lemon,pasta'},
    {'name': 'BBQ Chicken', 'ingredients': 'chicken,BBQ sauce,spices'},
    {'name': 'Teriyaki Chicken', 'ingredients': 'chicken,teriyaki sauce,garlic,ginger'},
    {'name': 'Beef Stroganoff', 'ingredients': 'beef,mushrooms,sour cream,onions,pasta'},
    {'name': 'Chicken Parmesan', 'ingredients': 'chicken,tomato sauce,cheese,pasta'},
    {'name': 'Vegetable Stir Fry', 'ingredients': 'vegetables,soy sauce,garlic,ginger,oil'},
    {'name': 'Tofu Stir Fry', 'ingredients': 'tofu,vegetables,soy sauce,garlic,sesame oil'},
    {'name': 'Vegetable Fried Rice', 'ingredients': 'rice,vegetables,egg,soy sauce,oil'},
    {'name': 'Prawn Curry', 'ingredients': 'prawns,curry paste,coconut milk,vegetables'},
    {'name': 'Crab Cakes', 'ingredients': 'crab,breadcrumbs,egg,mayo,spices'},
    {'name': 'Clam Chowder', 'ingredients': 'clams,potatoes,onions,cream,broth'},
    {'name': 'Seafood Paella', 'ingredients': 'seafood,rice,saffron,vegetables,broth'},
]

# Add new recipes to the dataframe
df_new = pd.concat([df_unique, pd.DataFrame(new_recipes)], ignore_index=True)

# Remove any duplicates that might have been added
df_final = df_new.drop_duplicates(subset=['name', 'ingredients'], keep='first').reset_index(drop=True)

print(f"After adding new recipes: {len(df_final)} recipes")

# Save to CSV
df_final.to_csv(csv_path, index=False)
print(f"\nUpdated CSV saved successfully!")
print(f"Total unique recipes: {len(df_final)}")
