import pandas as pd

# Read the current CSV file
csv_path = r'static\data\recipes_dataset.csv'
df = pd.read_csv(csv_path)

print(f"Current dataset: {len(df)} recipes")

# Additional recipes to add (to reach ~500)
additional_recipes = [
    # Asian cuisines
    {'name': 'Ramen', 'ingredients': 'noodles,broth,egg,pork,green onion'},
    {'name': 'Gyoza', 'ingredients': 'dumpling wrapper,pork,cabbage,garlic,soy sauce'},
    {'name': 'Tempura', 'ingredients': 'vegetables,shrimp,flour,egg,oil'},
    {'name': 'Yakitori', 'ingredients': 'chicken,soy sauce,mirin,garlic'},
    {'name': 'Tonkatsu', 'ingredients': 'pork,panko,egg,oil,sauce'},
    {'name': 'Sushi', 'ingredients': 'rice,nori,fish,cucumber,avocado'},
    {'name': 'Teriyaki Bowl', 'ingredients': 'rice,chicken,teriyaki sauce,sesame'},
    {'name': 'Miso Soup', 'ingredients': 'miso paste,dashi,tofu,seaweed'},
    {'name': 'Vietnamese Pho', 'ingredients': 'rice noodles,beef broth,beef,herbs'},
    {'name': 'Banh Mi', 'ingredients': 'baguette,pate,pickles,cilantro,mayo'},
    
    # European cuisines
    {'name': 'Risotto', 'ingredients': 'arborio rice,broth,wine,butter,parmesan'},
    {'name': 'Goulash', 'ingredients': 'beef,potatoes,onions,paprika,broth'},
    {'name': 'Schnitzel', 'ingredients': 'pork,breadcrumbs,egg,oil,lemon'},
    {'name': 'Cassoulet', 'ingredients': 'beans,duck,sausage,garlic,broth'},
    {'name': 'Bouillabaisse', 'ingredients': 'fish,seafood,saffron,tomato,fennel'},
    {'name': 'Beef Wellington', 'ingredients': 'beef,mushrooms,pate,pastry,sauce'},
    {'name': 'Coq au Vin', 'ingredients': 'chicken,wine,mushrooms,bacon,carrots'},
    {'name': 'Ratatouille', 'ingredients': 'eggplant,tomato,zucchini,peppers,basil'},
    {'name': 'Croque Monsieur', 'ingredients': 'bread,ham,cheese,butter,mustard'},
    {'name': 'Moussaka', 'ingredients': 'eggplant,meat sauce,bechamel,cheese'},
    
    # Mediterranean cuisines
    {'name': 'Feta Salad', 'ingredients': 'feta,tomatoes,olives,onion,oregano'},
    {'name': 'Tzatziki', 'ingredients': 'yogurt,cucumber,garlic,dill,lemon'},
    {'name': 'Tabbouleh', 'ingredients': 'bulgur,parsley,tomato,cucumber,lemon'},
    {'name': 'Shakshuka', 'ingredients': 'eggs,tomato sauce,peppers,spices'},
    {'name': 'Kebab', 'ingredients': 'meat,pita,lettuce,tomato,sauce'},
    {'name': 'Dolma', 'ingredients': 'grape leaves,rice,meat,spices'},
    {'name': 'Spanakopita', 'ingredients': 'phyllo,spinach,feta,egg,oil'},
    {'name': 'Souvlaki', 'ingredients': 'meat,pita,vegetables,tzatziki'},
    {'name': 'Moussaka', 'ingredients': 'eggplant,beef,bechamel,cheese'},
    {'name': 'Fatoush', 'ingredients': 'lettuce,tomato,cucumber,pita chips,sumac dressing'},
    
    # Indian cuisines
    {'name': 'Butter Chicken', 'ingredients': 'chicken,tomato sauce,cream,butter,spices'},
    {'name': 'Tandoori Chicken', 'ingredients': 'chicken,yogurt,tandoori spices'},
    {'name': 'Saag Paneer', 'ingredients': 'paneer,spinach,cream,garlic,ginger'},
    {'name': 'Chana Masala', 'ingredients': 'chickpeas,tomato,onion,spices,oil'},
    {'name': 'Aloo Gobi', 'ingredients': 'potatoes,cauliflower,onion,spices,oil'},
    {'name': 'Malai Kofta', 'ingredients': 'paneer,vegetables,cream,spices'},
    {'name': 'Dal Makhani', 'ingredients': 'lentils,kidney beans,cream,butter,spices'},
    {'name': 'Korma', 'ingredients': 'meat,yogurt,cream,nuts,spices'},
    {'name': 'Rogan Josh', 'ingredients': 'meat,yogurt,tomato,spices'},
    {'name': 'Vindaloo', 'ingredients': 'meat,potatoes,vinegar,chili,spices'},
    
    # Mexican cuisines
    {'name': 'Chiles Rellenos', 'ingredients': 'poblano peppers,cheese,tomato sauce,eggs'},
    {'name': 'Burrito', 'ingredients': 'tortilla,meat,beans,rice,cheese,sauce'},
    {'name': 'Chimichanga', 'ingredients': 'tortilla,meat,beans,cheese,oil,sauce'},
    {'name': 'Tamale', 'ingredients': 'corn masa,filling,corn husks'},
    {'name': 'Ceviche', 'ingredients': 'fish,lime,cilantro,onion,tomato'},
    {'name': 'Chiles Verdes', 'ingredients': 'green chiles,chicken,cream,cheese'},
    {'name': 'Salsa Verde', 'ingredients': 'tomatillos,cilantro,jalapeno,garlic,lime'},
    {'name': 'Guacamole', 'ingredients': 'avocado,lime,cilantro,onion,salt'},
    {'name': 'Pico de Gallo', 'ingredients': 'tomato,onion,cilantro,lime,salt'},
    {'name': 'Chilaquiles', 'ingredients': 'tortilla chips,salsa,cheese,eggs,onion'},
    
    # Middle Eastern cuisines
    {'name': 'Shawarma', 'ingredients': 'meat,pita,vegetables,tahini sauce'},
    {'name': 'Kofta', 'ingredients': 'ground meat,onion,spices,parsley'},
    {'name': 'Baba Ghanoush', 'ingredients': 'eggplant,tahini,lemon,garlic'},
    {'name': 'Tabbouleh', 'ingredients': 'bulgur,parsley,tomato,lemon,olive oil'},
    {'name': 'Fattoush', 'ingredients': 'vegetables,pita chips,sumac dressing'},
    {'name': 'Manakish', 'ingredients': 'dough,thyme,sesame,olive oil'},
    {'name': 'Harissa', 'ingredients': 'chili peppers,garlic,spices,olive oil'},
    {'name': 'Shish Kebab', 'ingredients': 'meat,vegetables,skewers'},
    {'name': 'Lentil Soup', 'ingredients': 'lentils,onion,garlic,broth,spices'},
    {'name': 'Muhammara', 'ingredients': 'red peppers,walnuts,breadcrumbs,pomegranate'},
    
    # Thai cuisines
    {'name': 'Tom Yum', 'ingredients': 'broth,lemongrass,galangal,lime,chili,shrimp'},
    {'name': 'Tom Kha Gai', 'ingredients': 'coconut milk,chicken,galangal,lime,lemongrass'},
    {'name': 'Larb', 'ingredients': 'meat,lime,fish sauce,chili,herbs'},
    {'name': 'Som Tam', 'ingredients': 'papaya,lime,fish sauce,chili,peanuts'},
    {'name': 'Satay', 'ingredients': 'meat,peanut sauce,lime,cucumber'},
    {'name': 'Red Curry', 'ingredients': 'red curry paste,coconut milk,meat,vegetables'},
    {'name': 'Massaman Curry', 'ingredients': 'beef,peanuts,potatoes,curry paste,coconut milk'},
    {'name': 'Khao Pad Sapparod', 'ingredients': 'rice,pineapple,chicken,cashews'},
    {'name': 'Pad See Ew', 'ingredients': 'noodles,soy sauce,chicken,broccoli'},
    {'name': 'Green Papaya Salad', 'ingredients': 'green papaya,lime,fish sauce,chili'},
    
    # American cuisines
    {'name': 'Meatloaf', 'ingredients': 'ground beef,breadcrumbs,egg,sauce'},
    {'name': 'Pot Roast', 'ingredients': 'beef,potatoes,carrots,onions,broth'},
    {'name': 'Fried Chicken', 'ingredients': 'chicken,flour,spices,oil'},
    {'name': 'Brisket', 'ingredients': 'beef,spice rub,smoke'},
    {'name': 'Mac and Cheese Bake', 'ingredients': 'pasta,cheese,cream,butter,breadcrumbs'},
    {'name': 'Mashed Potatoes', 'ingredients': 'potatoes,butter,milk,salt,pepper'},
    {'name': 'Gravy', 'ingredients': 'beef drippings,flour,broth,butter'},
    {'name': 'Cornbread', 'ingredients': 'cornmeal,flour,egg,milk,butter'},
    {'name': 'Coleslaw', 'ingredients': 'cabbage,carrot,mayo,vinegar,sugar'},
    {'name': 'Deviled Eggs', 'ingredients': 'eggs,mayo,mustard,paprika'},
    
    # Vegetarian/Vegan
    {'name': 'Vegetable Curry', 'ingredients': 'mixed vegetables,coconut milk,curry paste'},
    {'name': 'Bean Chili', 'ingredients': 'beans,tomato,onion,chili powder,cumin'},
    {'name': 'Lentil Burger', 'ingredients': 'lentils,breadcrumbs,onion,spices'},
    {'name': 'Stuffed Bell Peppers', 'ingredients': 'bell peppers,rice,vegetables,tomato sauce'},
    {'name': 'Eggplant Parmesan', 'ingredients': 'eggplant,tomato sauce,cheese,breadcrumbs'},
    {'name': 'Vegetable Lasagna', 'ingredients': 'pasta sheets,vegetables,sauce,cheese'},
    {'name': 'Chickpea Curry', 'ingredients': 'chickpeas,coconut milk,spices,vegetables'},
    {'name': 'Black Bean Tacos', 'ingredients': 'black beans,tortillas,salsa,lettuce,cheese'},
    {'name': 'Tofu Curry', 'ingredients': 'tofu,curry paste,coconut milk,vegetables'},
    {'name': 'Vegetable Soup', 'ingredients': 'mixed vegetables,broth,herbs,salt'},
    
    # Japanese specialties
    {'name': 'Okonomiyaki', 'ingredients': 'flour,cabbage,egg,sauce,mayo'},
    {'name': 'Takoyaki', 'ingredients': 'octopus,flour batter,takoyaki sauce'},
    {'name': 'Edamame', 'ingredients': 'soybeans,salt,water'},
    {'name': 'Karaage', 'ingredients': 'chicken,soy sauce,ginger,garlic,oil'},
    {'name': 'Sukiyaki', 'ingredients': 'beef,tofu,vegetables,sauce,rice'},
    {'name': 'Unagi', 'ingredients': 'eel,soy sauce,mirin,sugar'},
    {'name': 'Katsudon', 'ingredients': 'pork cutlet,rice,egg,onion,sauce'},
    {'name': 'Oyakodon', 'ingredients': 'chicken,egg,onion,rice,sauce'},
    {'name': 'Negitoro', 'ingredients': 'tuna,green onion,soy sauce,rice'},
    {'name': 'Agedashi Tofu', 'ingredients': 'tofu,potato starch,dashi,sauce'},
    
    # Seafood
    {'name': 'Grilled Salmon', 'ingredients': 'salmon,lemon,herbs,oil'},
    {'name': 'Fried Fish', 'ingredients': 'fish,flour,oil,salt,lemon'},
    {'name': 'Grilled Tuna', 'ingredients': 'tuna,soy sauce,sesame,lemon'},
    {'name': 'Lobster Thermidor', 'ingredients': 'lobster,cream,cheese,mustard'},
    {'name': 'Oysters Rockefeller', 'ingredients': 'oysters,spinach,butter,anise'},
    {'name': 'Mussels Mariniere', 'ingredients': 'mussels,white wine,garlic,parsley'},
    {'name': 'Scallops', 'ingredients': 'scallops,butter,garlic,lemon'},
    {'name': 'Squid Ink Pasta', 'ingredients': 'squid ink,pasta,garlic,olive oil'},
    {'name': 'Halibut', 'ingredients': 'halibut,lemon,herbs,olive oil'},
    {'name': 'Sea Bass', 'ingredients': 'sea bass,salt,pepper,lemon,herbs'},
    
    # Brazilian cuisines
    {'name': 'Feijoada', 'ingredients': 'black beans,pork,beef,sausage,orange'},
    {'name': 'Brigadeiro', 'ingredients': 'chocolate,condensed milk,butter'},
    {'name': 'Churrasco', 'ingredients': 'beef,salt,skewers'},
    {'name': 'Acaraje', 'ingredients': 'black eyed peas,onion,shrimp,oil'},
    {'name': 'Beijinho', 'ingredients': 'coconut,condensed milk,butter,sprinkles'},
    
    # Korean cuisines
    {'name': 'Bibimbap', 'ingredients': 'rice,vegetables,egg,gochujang,sesame'},
    {'name': 'Bulgogi', 'ingredients': 'beef,soy sauce,garlic,ginger,sesame'},
    {'name': 'Kimchi', 'ingredients': 'napa cabbage,chili,garlic,salt,fish sauce'},
    {'name': 'Tteokbokki', 'ingredients': 'rice cakes,gochujang,onion,fish cake'},
    {'name': 'Korean Fried Chicken', 'ingredients': 'chicken,flour,gochujang,garlic'},
    
    # Chinese cuisines
    {'name': 'Kung Pao Chicken', 'ingredients': 'chicken,peanuts,soy sauce,garlic,chili'},
    {'name': 'Mapo Tofu', 'ingredients': 'tofu,pork,sichuan pepper,chili,beans'},
    {'name': 'General Tso Chicken', 'ingredients': 'chicken,soy sauce,vinegar,chili,garlic'},
    {'name': 'Mongolian Beef', 'ingredients': 'beef,soy sauce,garlic,ginger,onion'},
    {'name': 'Lo Mein', 'ingredients': 'noodles,vegetables,soy sauce,garlic,oil'},
    
    # Breakfast items
    {'name': 'Pancakes', 'ingredients': 'flour,egg,milk,butter,baking powder'},
    {'name': 'Waffles', 'ingredients': 'flour,egg,milk,butter,baking powder'},
    {'name': 'French Toast', 'ingredients': 'bread,egg,milk,butter,cinnamon'},
    {'name': 'Scrambled Eggs', 'ingredients': 'eggs,butter,milk,salt,pepper'},
    {'name': 'Bacon', 'ingredients': 'pork belly,salt,smoke'},
    {'name': 'Sausage', 'ingredients': 'pork,spices,salt'},
    {'name': 'Hash Browns', 'ingredients': 'potatoes,onion,butter,oil,salt'},
    {'name': 'Omelette with ham', 'ingredients': 'eggs,ham,cheese,butter'},
    {'name': 'Crepes', 'ingredients': 'flour,egg,milk,butter'},
    {'name': 'Huevos Rancheros', 'ingredients': 'eggs,tortillas,beans,salsa,cheese'},
    
    # Desserts
    {'name': 'Brownie', 'ingredients': 'chocolate,flour,butter,egg,sugar'},
    {'name': 'Cheesecake', 'ingredients': 'cream cheese,graham cracker,egg,sugar'},
    {'name': 'Tiramisu', 'ingredients': 'mascarpone,coffee,ladyfinger,cocoa'},
    {'name': 'Chocolate Mousse', 'ingredients': 'chocolate,cream,egg,sugar'},
    {'name': 'Apple Pie', 'ingredients': 'apples,flour,sugar,butter,spices'},
    {'name': 'Pumpkin Pie', 'ingredients': 'pumpkin,egg,cream,sugar,cinnamon'},
    {'name': 'Lemon Bars', 'ingredients': 'flour,butter,egg,lemon,sugar'},
    {'name': 'Pecan Pie', 'ingredients': 'pecans,corn syrup,butter,egg,sugar'},
    {'name': 'Key Lime Pie', 'ingredients': 'key lime,sweetened condensed milk,egg yolk'},
    {'name': 'Chocolate Chip Cookies', 'ingredients': 'flour,butter,egg,sugar,chocolate chips'},
    
    # Beverages
    {'name': 'Smoothie', 'ingredients': 'fruit,yogurt,milk,honey'},
    {'name': 'Iced Coffee', 'ingredients': 'coffee,ice,milk,sugar'},
    {'name': 'Latte', 'ingredients': 'espresso,milk,foam'},
    {'name': 'Cappuccino', 'ingredients': 'espresso,milk,foam,chocolate'},
    {'name': 'Mojito', 'ingredients': 'rum,mint,lime,sugar,soda water'},
    {'name': 'Margarita', 'ingredients': 'tequila,lime,triple sec,salt'},
    {'name': 'Piña Colada', 'ingredients': 'rum,coconut milk,pineapple,ice'},
    {'name': 'Daiquiri', 'ingredients': 'rum,lime,sugar,ice'},
    {'name': 'Sangria', 'ingredients': 'red wine,fruit,brandy,sugar'},
    {'name': 'Mimosa', 'ingredients': 'champagne,orange juice,ice'},
    
    # Additional Asian
    {'name': 'Satay Ayam', 'ingredients': 'chicken,peanut sauce,turmeric,coconut'},
    {'name': 'Lumpia', 'ingredients': 'spring roll wrapper,pork,vegetables,oil'},
    {'name': 'Mee Goreng', 'ingredients': 'noodles,shrimp,egg,soy sauce,vegetables'},
    {'name': 'Laksa', 'ingredients': 'coconut milk,noodles,seafood,spices'},
    {'name': 'Satay Beef', 'ingredients': 'beef,peanut sauce,onion,ginger'},
    
    # Additional Mediterranean
    {'name': 'Caponata', 'ingredients': 'eggplant,tomato,olives,capers,vinegar'},
    {'name': 'Pissaladiere', 'ingredients': 'dough,anchovies,onion,olives,oil'},
    {'name': 'Salade Nicoise', 'ingredients': 'tuna,eggs,potatoes,olives,tomato'},
    {'name': 'Gazpacho', 'ingredients': 'tomato,cucumber,pepper,olive oil,vinegar'},
    {'name': 'Minestrone', 'ingredients': 'vegetables,pasta,beans,broth,herbs'},
    
    # Additional Indian
    {'name': 'Paneer Tikka', 'ingredients': 'paneer,yogurt,spices,onion,peppers'},
    {'name': 'Naan', 'ingredients': 'flour,yogurt,butter,salt'},
    {'name': 'Roti', 'ingredients': 'wheat flour,water,salt,oil'},
    {'name': 'Biryani Rice', 'ingredients': 'rice,meat,saffron,yogurt,spices'},
    {'name': 'Kheer', 'ingredients': 'rice,milk,sugar,cardamom,nuts'},
    
    # Additional Italian
    {'name': 'Carbonara', 'ingredients': 'pasta,guanciale,egg,pecorino,pepper'},
    {'name': 'Cacio e Pepe', 'ingredients': 'pasta,pecorino,black pepper'},
    {'name': 'Amatriciana', 'ingredients': 'pasta,tomato,guanciale,pecorino'},
    {'name': 'Bolognese', 'ingredients': 'pasta,ground meat,tomato,vegetables'},
    {'name': 'Aglio e Olio', 'ingredients': 'pasta,garlic,olive oil,red pepper'},
    
    # Additional Mexican
    {'name': 'Mole', 'ingredients': 'chicken,chocolate,chili,spices'},
    {'name': 'Pozole', 'ingredients': 'hominy,pork,chili,garlic,onion'},
    {'name': 'Chiles Rellenos de Queso', 'ingredients': 'poblano,cheese,egg,tomato sauce'},
    {'name': 'Carne Asada', 'ingredients': 'beef,lime,cilantro,spices'},
    {'name': 'Al Pastor', 'ingredients': 'pork,pineapple,dried chili,spices'},
]

# Add all new recipes to the dataframe
df_new = pd.concat([df, pd.DataFrame(additional_recipes)], ignore_index=True)

# Remove any duplicates
df_final = df_new.drop_duplicates(subset=['name', 'ingredients'], keep='first').reset_index(drop=True)

# Trim to exactly 500 recipes if we have more
if len(df_final) > 500:
    df_final = df_final.iloc[:500]
elif len(df_final) < 500:
    print(f"Warning: Only {len(df_final)} recipes available. Need to add more variations.")

print(f"Final dataset: {len(df_final)} recipes")

# Save to CSV
df_final.to_csv(csv_path, index=False)
print(f"Updated CSV saved successfully!")
