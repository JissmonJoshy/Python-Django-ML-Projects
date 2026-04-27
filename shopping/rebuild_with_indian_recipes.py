import pandas as pd

csv_path = r'static\data\recipes_dataset.csv'

# Core recipes (original unique ones)
core_recipes = [
    {'name': 'Noodles', 'ingredients': 'noodles,vegetables,sauce'},
    {'name': 'Tea', 'ingredients': 'tea powder,milk,sugar'},
    {'name': 'Upma', 'ingredients': 'rava,vegetables,oil'},
    {'name': 'Milkshake', 'ingredients': 'milk,sugar,fruit'},
    {'name': 'Pizza', 'ingredients': 'base,cheese,sauce,vegetables'},
    {'name': 'Juice', 'ingredients': 'fruit,sugar,water'},
    {'name': 'Soup', 'ingredients': 'vegetables,salt,water'},
    {'name': 'Omelette', 'ingredients': 'egg,salt,oil,onion'},
    {'name': 'Salad', 'ingredients': 'vegetables,salt,lemon'},
    {'name': 'Fried Rice', 'ingredients': 'rice,vegetables,soy sauce,oil'},
    {'name': 'Biriyani', 'ingredients': 'rice,chicken,onion,masala,oil'},
    {'name': 'Coffee', 'ingredients': 'coffee powder,milk,sugar'},
    {'name': 'Sambar', 'ingredients': 'dal,vegetables,spices'},
    {'name': 'Idli', 'ingredients': 'rice batter'},
    {'name': 'Burger', 'ingredients': 'bun,patty,lettuce,sauce'},
    {'name': 'Paratha', 'ingredients': 'wheat flour,oil,salt'},
    {'name': 'Dosa', 'ingredients': 'rice batter,oil'},
    {'name': 'Pasta', 'ingredients': 'pasta,sauce,cheese,oil'},
    {'name': 'Cake', 'ingredients': 'flour,sugar,egg,butter'},
    {'name': 'Sandwich', 'ingredients': 'bread,butter,vegetables'},
]

# Kerala Specialties
kerala_recipes = [
    {'name': 'Appam', 'ingredients': 'rice flour,coconut milk,yeast,sugar,salt'},
    {'name': 'Stew Kerala', 'ingredients': 'potatoes,carrots,onions,coconut milk,spices'},
    {'name': 'Puttu', 'ingredients': 'rice flour,jaggery,coconut,salt,water'},
    {'name': 'Avial', 'ingredients': 'mixed vegetables,coconut paste,cumin,turmeric,oil'},
    {'name': 'Olan', 'ingredients': 'white pumpkin,cowpeas,coconut milk,green chili,turmeric'},
    {'name': 'Pachadi', 'ingredients': 'mango,jaggery,chili,salt,oil'},
    {'name': 'Pickle Kerala', 'ingredients': 'mango,chili,fenugreek,mustard,oil'},
    {'name': 'Thoran', 'ingredients': 'shredded vegetables,coconut,cumin,turmeric,oil'},
    {'name': 'Pulissery', 'ingredients': 'pumpkin,coconut paste,turmeric,green chili,yogurt'},
    {'name': 'Erissery', 'ingredients': 'pumpkin,beans,coconut paste,green chili,turmeric'},
    {'name': 'Kerala Fish Curry', 'ingredients': 'fish,coconut milk,turmeric,chili,onions,curry leaves'},
    {'name': 'Prawn Curry Kerala', 'ingredients': 'prawns,coconut milk,turmeric,chili,onions,curry leaves'},
    {'name': 'Kaalan', 'ingredients': 'yam,raw banana,chickpeas,coconut paste,turmeric,green chili'},
    {'name': 'Ishtew', 'ingredients': 'potatoes,carrots,onions,coconut milk,pepper,cardamom'},
    {'name': 'Malabar Paratha', 'ingredients': 'wheat flour,onions,green chili,oil,salt'},
    {'name': 'Banana Chips Kerala', 'ingredients': 'banana,turmeric,chili,oil,salt'},
    {'name': 'Tapioca Chips', 'ingredients': 'tapioca,cumin,chili,turmeric,oil,salt'},
    {'name': 'Kerala Biryani', 'ingredients': 'basmati rice,meat,coconut,spices,oil,onions'},
    {'name': 'Malabar Biryani', 'ingredients': 'basmati rice,meat,coconut,spices,ghee'},
    {'name': 'Beef Fry Kerala', 'ingredients': 'beef,onion,ginger,garlic,chili,coconut'},
]

# More Indian cuisines
indian_recipes = [
    {'name': 'Panipuri', 'ingredients': 'semolina,potato,chickpeas,tamarind sauce,chili sauce,salt'},
    {'name': 'Gol Gappa', 'ingredients': 'puri,potato,chickpeas,tamarind sauce,yogurt,spices'},
    {'name': 'Samosa', 'ingredients': 'maida,potato,peas,spices,oil'},
    {'name': 'Kachori', 'ingredients': 'maida,lentil filling,spices,oil'},
    {'name': 'Dhokla', 'ingredients': 'rice flour,urad flour,ginger,green chili,salt,oil'},
    {'name': 'Fafda', 'ingredients': 'gram flour,salt,spices,oil'},
    {'name': 'Jalebi', 'ingredients': 'maida,yogurt,sugar syrup,cardamom,ghee'},
    {'name': 'Laddu', 'ingredients': 'gram flour,ghee,jaggery,cardamom,dry fruits'},
    {'name': 'Rasam', 'ingredients': 'tamarind,tomato,pepper,cumin,curry leaves,salt'},
    {'name': 'Curd Rice', 'ingredients': 'rice,curd,salt,curry leaves,mustard,oil'},
    {'name': 'Lemon Rice', 'ingredients': 'rice,lemon,turmeric,mustard,curry leaves,oil'},
    {'name': 'Coconut Rice', 'ingredients': 'rice,coconut,turmeric,mustard,curry leaves,oil'},
    {'name': 'Tamarind Rice', 'ingredients': 'rice,tamarind,jaggery,mustard,curry leaves,oil'},
    {'name': 'Poha', 'ingredients': 'flattened rice,potato,mustard,turmeric,curry leaves,oil'},
    {'name': 'Chole Bhature', 'ingredients': 'chickpeas,maida,yogurt,onion,tamarind,spices'},
    {'name': 'Tandoori Aloo', 'ingredients': 'potatoes,yogurt,tandoori spices,oil'},
    {'name': 'Paneer Tikka Masala', 'ingredients': 'paneer,tomato,cream,ginger,garlic,spices'},
    {'name': 'Laal Maas', 'ingredients': 'mutton,yogurt,red chili,ginger,garlic,onions'},
    {'name': 'Pav Bhaji', 'ingredients': 'vegetables,butter,pav bhaji masala,pav bread'},
    {'name': 'Misal Pav', 'ingredients': 'sprouts,beans,pav bread,spices,oil'},
    {'name': 'Hyderabadi Dum Biryani', 'ingredients': 'meat,basmati rice,yogurt,saffron,fried onions'},
    {'name': 'Haleem', 'ingredients': 'meat,wheat,lentils,spices,ghee'},
    {'name': 'Mirchi ka Salan', 'ingredients': 'green chili,peanuts,sesame,coconut,tamarind'},
    {'name': 'Nihari', 'ingredients': 'meat,yogurt,ginger,garlic,red chili,nihari masala'},
    {'name': 'Chettinad Chicken', 'ingredients': 'chicken,pepper,turmeric,chili,onion,oil'},
    {'name': 'Khichdi', 'ingredients': 'rice,lentils,vegetables,turmeric,oil'},
    {'name': 'Naan', 'ingredients': 'flour,yogurt,butter,salt'},
    {'name': 'Roti', 'ingredients': 'wheat flour,water,salt,oil'},
    {'name': 'Dal Makhani', 'ingredients': 'lentils,kidney beans,cream,butter,spices'},
    {'name': 'Butter Chicken', 'ingredients': 'chicken,tomato sauce,cream,butter,spices'},
]

# International cuisines
international_recipes = [
    {'name': 'fruit salad', 'ingredients': 'fruit,sugar,lemon,apple,banana,orange'},
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
    {'name': 'Ramen', 'ingredients': 'noodles,broth,egg,pork,green onion'},
    {'name': 'Sushi', 'ingredients': 'rice,nori,fish,cucumber,avocado'},
    {'name': 'Miso Soup', 'ingredients': 'miso paste,dashi,tofu,seaweed'},
    {'name': 'Vietnamese Pho', 'ingredients': 'rice noodles,beef broth,beef,herbs'},
    {'name': 'Risotto', 'ingredients': 'arborio rice,broth,wine,butter,parmesan'},
    {'name': 'Beef Wellington', 'ingredients': 'beef,mushrooms,pate,pastry,sauce'},
    {'name': 'Ratatouille', 'ingredients': 'eggplant,tomato,zucchini,peppers,basil'},
    {'name': 'Feta Salad', 'ingredients': 'feta,tomatoes,olives,onion,oregano'},
    {'name': 'Shakshuka', 'ingredients': 'eggs,tomato sauce,peppers,spices'},
    {'name': 'Kebab', 'ingredients': 'meat,pita,lettuce,tomato,sauce'},
    {'name': 'Tom Yum', 'ingredients': 'broth,lemongrass,galangal,lime,chili,shrimp'},
    {'name': 'Larb', 'ingredients': 'meat,lime,fish sauce,chili,herbs'},
    {'name': 'Som Tam', 'ingredients': 'papaya,lime,fish sauce,chili,peanuts'},
    {'name': 'Red Curry', 'ingredients': 'red curry paste,coconut milk,meat,vegetables'},
    {'name': 'Kung Pao Chicken', 'ingredients': 'chicken,peanuts,soy sauce,garlic,chili'},
    {'name': 'Bibimbap', 'ingredients': 'rice,vegetables,egg,gochujang,sesame'},
    {'name': 'Bulgogi', 'ingredients': 'beef,soy sauce,garlic,ginger,sesame'},
    {'name': 'Pancakes', 'ingredients': 'flour,egg,milk,butter,baking powder'},
    {'name': 'Waffles', 'ingredients': 'flour,egg,milk,butter,baking powder'},
    {'name': 'French Toast', 'ingredients': 'bread,egg,milk,butter,cinnamon'},
    {'name': 'Brownie', 'ingredients': 'chocolate,flour,butter,egg,sugar'},
    {'name': 'Cheesecake', 'ingredients': 'cream cheese,graham cracker,egg,sugar'},
    {'name': 'Tiramisu', 'ingredients': 'mascarpone,coffee,ladyfinger,cocoa'},
    {'name': 'Smoothie', 'ingredients': 'fruit,yogurt,milk,honey'},
    {'name': 'Latte', 'ingredients': 'espresso,milk,foam'},
    {'name': 'Cappuccino', 'ingredients': 'espresso,milk,foam,chocolate'},
]

# Combine all recipes
all_recipes = core_recipes + kerala_recipes + indian_recipes + international_recipes

# Create dataframe and remove duplicates
df = pd.DataFrame(all_recipes)
df_unique = df.drop_duplicates(subset=['name', 'ingredients'], keep='first').reset_index(drop=True)

# Trim to 500 if needed
if len(df_unique) > 500:
    df_unique = df_unique.iloc[:500]

print(f"Total unique recipes: {len(df_unique)}")
print(f"- Core recipes: {len(core_recipes)}")
print(f"- Kerala recipes: {len(kerala_recipes)}")
print(f"- Indian recipes: {len(indian_recipes)}")
print(f"- International recipes: {len(international_recipes)}")

# Save to CSV
df_unique.to_csv(csv_path, index=False)
print(f"\nCSV updated successfully with {len(df_unique)} recipes!")

# Verify some recipes
print("\nSample recipes in file:")
print(df_unique[df_unique['name'].str.contains('Appam|Rasam|Hyderabadi|Chettinad', na=False)][['name', 'ingredients']].to_string())
