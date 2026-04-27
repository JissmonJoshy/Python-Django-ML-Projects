import pandas as pd

# Read the current CSV file
csv_path = r'static\data\recipes_dataset.csv'
df = pd.read_csv(csv_path)

print(f"Current dataset: {len(df)} recipes")

# Generate additional recipe variations to reach 500
recipes_to_add = []

# Spice variations
spices = ['cumin', 'coriander', 'turmeric', 'paprika', 'garam masala', 'ginger', 'garlic', 'black pepper']
bases = ['basmati rice', 'jasmine rice', 'white rice', 'brown rice', 'quinoa', 'couscous', 'pasta', 'noodles']
proteins = ['chicken', 'beef', 'pork', 'lamb', 'turkey', 'tofu', 'tempeh', 'seitan', 'chickpeas', 'lentils']
vegetables = ['broccoli', 'carrots', 'zucchini', 'bell peppers', 'mushrooms', 'spinach', 'kale', 'bok choy', 'green beans', 'peas']
sauces = ['garlic sauce', 'soy sauce', 'ginger sauce', 'peanut sauce', 'bbq sauce', 'teriyaki sauce', 'mushroom sauce', 'cream sauce']

# Generate curry variations
for protein in proteins[:5]:
    for spice in spices[:4]:
        recipes_to_add.append({
            'name': f'{protein.title()} {spice.title()} Curry',
            'ingredients': f'{protein},coconut milk,{spice},rice,onions'
        })

# Generate rice bowl variations
for protein in proteins[:6]:
    for vegetable in vegetables[:6]:
        recipes_to_add.append({
            'name': f'{vegetable.title()} and {protein.title()} Rice Bowl',
            'ingredients': f'rice,{protein},{vegetable},soy sauce,sesame oil'
        })

# Generate stir-fry variations
for protein in proteins[:5]:
    for vegetable in vegetables[:5]:
        recipes_to_add.append({
            'name': f'{protein.title()} and {vegetable.title()} Stir Fry',
            'ingredients': f'{protein},{vegetable},soy sauce,garlic,ginger,oil'
        })

# Generate pasta variations
pastas = ['spaghetti', 'penne', 'fettuccine', 'linguine', 'rigatoni', 'angel hair']
for pasta in pastas:
    for protein in proteins[:4]:
        recipes_to_add.append({
            'name': f'{pasta.title()} with {protein.title()}',
            'ingredients': f'{pasta},{protein},tomato sauce,garlic,olive oil,parmesan'
        })

# Generate soup variations
for base in ['chicken', 'beef', 'vegetable', 'bone']:
    for vegetable in vegetables[:6]:
        recipes_to_add.append({
            'name': f'{vegetable.title()} {base.title()} Soup',
            'ingredients': f'{base} broth,{vegetable},onions,garlic,salt,pepper'
        })

# Generate salad variations
for vegetable in vegetables[:8]:
    for protein in proteins[:4]:
        recipes_to_add.append({
            'name': f'{vegetable.title()} {protein.title()} Salad',
            'ingredients': f'{vegetable},{protein},dressing,olive oil,lime'
        })

# Generate grilled variations
for protein in ['chicken breast', 'salmon', 'steak', 'lamb chops', 'pork chops', 'shrimp']:
    recipes_to_add.append({
        'name': f'Grilled {protein.title()}',
        'ingredients': f'{protein},lemon,herbs,olive oil,garlic'
    })

# Generate baked variations
for item in ['salmon', 'chicken', 'vegetables', 'tofu', 'mushrooms']:
    recipes_to_add.append({
        'name': f'Baked {item.title()}',
        'ingredients': f'{item},olive oil,garlic,herbs,lemon,salt'
    })

# Generate steamed variations
for vegetable in vegetables[:6]:
    recipes_to_add.append({
        'name': f'Steamed {vegetable.title()}',
        'ingredients': f'{vegetable},water,salt,butter,garlic'
    })

# Generate roasted variations
for vegetable in vegetables[:8]:
    recipes_to_add.append({
        'name': f'Roasted {vegetable.title()}',
        'ingredients': f'{vegetable},olive oil,garlic,salt,pepper,herbs'
    })

# Generate pizza variations
toppings = ['pepperoni', 'mushroom', 'sausage', 'vegetables', 'seafood', 'hawaiian']
for topping in toppings:
    recipes_to_add.append({
        'name': f'{topping.title()} Pizza',
        'ingredients': f'pizza base,cheese,{topping},tomato sauce,olive oil'
    })

# Generate sandwich variations  
for filling in ['turkey', 'ham', 'roast beef', 'chicken salad', 'tuna salad', 'veggie']:
    recipes_to_add.append({
        'name': f'{filling.title()} Sandwich',
        'ingredients': f'bread,{filling},lettuce,tomato,mayo,mustard'
    })

# Generate wrap variations
for filling in ['chicken', 'beef', 'vegetables', 'falafel', 'tofu', 'tempeh']:
    recipes_to_add.append({
        'name': f'{filling.title()} Wrap',
        'ingredients': f'tortilla wrap,{filling},lettuce,tomato,sauce'
    })

# Generate smoothie variations
for fruit in ['strawberry', 'banana', 'mango', 'blueberry', 'papaya', 'pineapple']:
    recipes_to_add.append({
        'name': f'{fruit.title()} Smoothie',
        'ingredients': f'{fruit},yogurt,milk,honey,ice'
    })

# Generate juice variations
for fruit in ['orange', 'apple', 'grape', 'cranberry', 'pomegranate', 'watermelon']:
    recipes_to_add.append({
        'name': f'{fruit.title()} Juice',
        'ingredients': f'{fruit},water,sugar,lemon'
    })

# Generate tea variations
for flavor in ['green', 'black', 'herbal', 'chai', 'oolong', 'jasmine']:
    recipes_to_add.append({
        'name': f'{flavor.title()} Tea',
        'ingredients': f'{flavor} tea leaves,water,milk,honey,sugar'
    })

# Generate coffee variations
for style in ['espresso', 'americano', 'macchiato', 'flat white', 'cortado', 'lungo']:
    recipes_to_add.append({
        'name': f'{style.title()}',
        'ingredients': f'coffee beans,water,milk,cream'
    })

# Add the recipes
df_new = pd.concat([df, pd.DataFrame(recipes_to_add)], ignore_index=True)

# Remove duplicates
df_final = df_new.drop_duplicates(subset=['name', 'ingredients'], keep='first').reset_index(drop=True)

# Trim or pad to 500
current_count = len(df_final)
print(f"Total recipes before final adjustment: {current_count}")

if current_count > 500:
    df_final = df_final.iloc[:500]
    print(f"Trimmed to exactly 500 recipes")
elif current_count < 500:
    # Generate additional simple recipes
    additional = []
    for i in range(500 - current_count):
        base_protein = proteins[i % len(proteins)]
        base_veg = vegetables[i % len(vegetables)]
        additional.append({
            'name': f'Mixed {base_protein.title()} Dish #{i+1}',
            'ingredients': f'{base_protein},{base_veg},rice,sauce,oil'
        })
    
    df_additional = pd.DataFrame(additional)
    df_final = pd.concat([df_final, df_additional], ignore_index=True)
    df_final = df_final.drop_duplicates(subset=['name', 'ingredients'], keep='first').reset_index(drop=True)
    df_final = df_final.iloc[:500]

print(f"Final dataset: {len(df_final)} recipes")

# Save to CSV
df_final.to_csv(csv_path, index=False)
print(f"Updated CSV saved successfully with {len(df_final)} recipes!")
