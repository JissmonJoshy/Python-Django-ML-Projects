import pandas as pd

# Read the current CSV file
csv_path = r'static\data\recipes_dataset.csv'
df = pd.read_csv(csv_path)

print(f"Current dataset: {len(df)} recipes")

# Indian and Kerala recipes to add
indian_kerala_recipes = [
    # Kerala Specialties
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
    {'name': 'Injera Kerala', 'ingredients': 'rice,cucumber,chili,salt,turmeric'},
    {'name': 'Appam Stew', 'ingredients': 'appam,chicken,potatoes,onions,coconut milk,spices'},
    {'name': 'Kerala Fish Curry', 'ingredients': 'fish,coconut milk,turmeric,chili,onions,curry leaves'},
    {'name': 'Prawn Curry Kerala', 'ingredients': 'prawns,coconut milk,turmeric,chili,onions,curry leaves'},
    {'name': 'Kaalan', 'ingredients': 'yam,raw banana,chickpeas,coconut paste,turmeric,green chili'},
    {'name': 'Ishtew', 'ingredients': 'potatoes,carrots,onions,coconut milk,pepper,cardamom'},
    {'name': 'Malabar Paratha', 'ingredients': 'wheat flour,onions,green chili,oil,salt'},
    {'name': 'Banana Chips Kerala', 'ingredients': 'banana,turmeric,chili,oil,salt'},
    {'name': 'Tapioca Chips', 'ingredients': 'tapioca,cumin,chili,turmeric,oil,salt'},
    {'name': 'Kerala Biryani', 'ingredients': 'basmati rice,meat,coconut,spices,oil,onions'},
    
    # North Indian curries
    {'name': 'Panipuri', 'ingredients': 'semolina,potato,chickpeas,tamarind sauce,chili sauce,salt'},
    {'name': 'Gol Gappa', 'ingredients': 'puri,potato,chickpeas,tamarind sauce,yogurt,spices'},
    {'name': 'Samosa', 'ingredients': 'maida,potato,peas,spices,oil'},
    {'name': 'Kachori', 'ingredients': 'maida,lentil filling,spices,oil'},
    {'name': 'Dhokla', 'ingredients': 'rice flour,urad flour,ginger,green chili,salt,oil'},
    {'name': 'Fafda', 'ingredients': 'gram flour,salt,spices,oil'},
    {'name': 'Jalebi', 'ingredients': 'maida,yogurt,sugar syrup,cardamom,ghee'},
    {'name': 'Laddu', 'ingredients': 'gram flour,ghee,jaggery,cardamom,dry fruits'},
    {'name': 'Barfi', 'ingredients': 'condensed milk,ghee,cardamom,dry fruits'},
    {'name': 'Khoya Barfi', 'ingredients': 'khoya,sugar,ghee,cardamom'},
    
    # Bengali curries
    {'name': 'Fish Curry Bengali', 'ingredients': 'fish,potato,onion,turmeric,ginger,garlic,oil'},
    {'name': 'Prawn Malai Curry', 'ingredients': 'prawns,coconut,cream,ginger,garlic,green chili'},
    {'name': 'Egg Curry Bengali', 'ingredients': 'eggs,onion,turmeric,ginger,garlic,coconut,oil'},
    {'name': 'Luchi', 'ingredients': 'maida,oil,salt,sugar'},
    {'name': 'Puri', 'ingredients': 'wheat flour,salt,oil,water'},
    {'name': 'Alur Dum', 'ingredients': 'potatoes,onion,ginger,garlic,yogurt,spices'},
    {'name': 'Begun Bhaja', 'ingredients': 'eggplant,turmeric,chili,salt,oil'},
    {'name': 'Aloo Roast', 'ingredients': 'potatoes,onion,green chili,ginger,garlic'},
    {'name': 'Macher Palaw', 'ingredients': 'fish,rice,potato,onion,spices,ghee'},
    {'name': 'Mutton Biryani', 'ingredients': 'mutton,basmati rice,yogurt,ginger,garlic,spices'},
    
    # South Indian specialties
    {'name': 'Rasam', 'ingredients': 'tamarind,tomato,pepper,cumin,curry leaves,salt'},
    {'name': 'Sambar', 'ingredients': 'dal,vegetables,tamarind,sambar powder,oil'},
    {'name': 'Curd Rice', 'ingredients': 'rice,curd,salt,curry leaves,mustard,oil'},
    {'name': 'Lemon Rice', 'ingredients': 'rice,lemon,turmeric,mustard,curry leaves,oil'},
    {'name': 'Coconut Rice', 'ingredients': 'rice,coconut,turmeric,mustard,curry leaves,oil'},
    {'name': 'Tamarind Rice', 'ingredients': 'rice,tamarind,jaggery,mustard,curry leaves,oil'},
    {'name': 'Poha', 'ingredients': 'flattened rice,potato,mustard,turmeric,curry leaves,oil'},
    {'name': 'Uttapam', 'ingredients': 'rice batter,vegetables,onion,chili'},
    {'name': 'Medhu Vada', 'ingredients': 'urad flour,cumin,salt,black pepper,oil'},
    {'name': 'Medu Vada', 'ingredients': 'urad dal,salt,cumin,black pepper,oil'},
    
    # Punjabi curries
    {'name': 'Chole Bhature', 'ingredients': 'chickpeas,maida,yogurt,onion,tamarind,spices'},
    {'name': 'Amritsari Kulcha', 'ingredients': 'maida,yogurt,salt,paneer,onion'},
    {'name': 'Tandoori Aloo', 'ingredients': 'potatoes,yogurt,tandoori spices,oil'},
    {'name': 'Paneer Tikka Masala', 'ingredients': 'paneer,tomato,cream,ginger,garlic,spices'},
    {'name': 'Shahi Tukda', 'ingredients': 'bread,condensed milk,dry fruits,cardamom,ghee'},
    {'name': 'Lassi', 'ingredients': 'yogurt,water,sugar,cardamom,mango'},
    {'name': 'Dahi Bhalle', 'ingredients': 'urad flour,yogurt,sugar syrup,cardamom'},
    {'name': 'Makki di Roti', 'ingredients': 'cornmeal,salt,ghee,water'},
    {'name': 'Sarson da Saag', 'ingredients': 'mustard greens,spinach,butter,salt,cream'},
    {'name': 'Chikhalwali', 'ingredients': 'wheat flour,jaggery,ghee,nuts'},
    
    # Awadhi/Lucknowi curries
    {'name': 'Dum Pukht Biryani', 'ingredients': 'meat,basmati rice,yogurt,saffron,ghee'},
    {'name': 'Tundey Ke Kabab', 'ingredients': 'meat,spices,ginger,garlic,green chili'},
    {'name': 'Shami Kabab', 'ingredients': 'meat,lentils,ginger,garlic,spices,egg'},
    {'name': 'Galauti Kabab', 'ingredients': 'meat,spices,ginger,garlic,yogurt'},
    {'name': 'Haleem', 'ingredients': 'meat,lentils,wheat,spices,ghee'},
    {'name': 'Nihari', 'ingredients': 'meat,yogurt,ginger,garlic,red chili,nihari masala'},
    {'name': 'Korma Awadhi', 'ingredients': 'meat,yogurt,cream,nuts,spices'},
    {'name': 'Kakori Kabab', 'ingredients': 'meat,lentils,spices,ginger,garlic,egg'},
    {'name': 'Paya', 'ingredients': 'meat trotters,ginger,garlic,spices,oil'},
    {'name': 'Dum Aloo Awadhi', 'ingredients': 'potatoes,yogurt,cream,spices'},
    
    # Rajasthani curries
    {'name': 'Laal Maas', 'ingredients': 'mutton,yogurt,red chili,ginger,garlic,onions'},
    {'name': 'Panchmel Ki Sabzi', 'ingredients': 'mixed vegetables,turmeric,green chili,oil'},
    {'name': 'Churma Laddoo', 'ingredients': 'wheat flour,ghee,jaggery,cardamom,nuts'},
    {'name': 'Khichdi Rajasthan', 'ingredients': 'rice,moong dal,vegetables,cumin,turmeric,ghee'},
    {'name': 'Bajra Roti', 'ingredients': 'millet flour,salt,ghee,water'},
    {'name': 'Bajra Halwa', 'ingredients': 'millet flour,ghee,jaggery,nuts,cardamom'},
    {'name': 'Ker Sangri', 'ingredients': 'dried desert bean,turmeric,ginger,onion,oil'},
    {'name': 'Pyaaz ka Aaloo', 'ingredients': 'potatoes,onions,turmeric,green chili,salt'},
    {'name': 'Mirch Paste', 'ingredients': 'green chili,garlic,coconut,lemon,salt'},
    {'name': 'Rajasthani Khichri', 'ingredients': 'rice,lentils,vegetables,ghee,spices'},
    
    # Maharashtrian curries
    {'name': 'Vada Pav', 'ingredients': 'potato,gram flour,turmeric,chili,oil'},
    {'name': 'Pav Bhaji', 'ingredients': 'vegetables,butter,pav bhaji masala,pav bread'},
    {'name': 'Batata Vada', 'ingredients': 'potato,gram flour,oil,chili,turmeric'},
    {'name': 'Misal Pav', 'ingredients': 'sprouts,beans,pav bread,spices,oil'},
    {'name': 'Upma', 'ingredients': 'semolina,vegetables,oil,cumin,turmeric'},
    {'name': 'Sheera', 'ingredients': 'semolina,ghee,sugar,cardamom,nuts'},
    {'name': 'Kharichi Kheer', 'ingredients': 'rice,milk,jaggery,cardamom,nuts'},
    {'name': 'Surali Chakli', 'ingredients': 'gram flour,rice flour,turmeric,chili,oil'},
    {'name': 'Aanarsa', 'ingredients': 'rice,jaggery,sesame,poppy seeds'},
    {'name': 'Chikhalwali', 'ingredients': 'wheat flour,jaggery,ghee,nuts'},
    
    # Gujarati curries
    {'name': 'Khichiyu', 'ingredients': 'rice,lentils,vegetables,turmeric,oil'},
    {'name': 'Khichdi Gujarati', 'ingredients': 'rice,moong dal,vegetables,ghee,cumin'},
    {'name': 'Fafda Jalebi', 'ingredients': 'gram flour,maida,sugar syrup,ghee'},
    {'name': 'Undhyu', 'ingredients': 'vegetables,chickpeas,potatoes,peanuts,spices'},
    {'name': 'Dhokla Gujarati', 'ingredients': 'rice flour,urad flour,ginger,salt,oil'},
    {'name': 'Khandvi', 'ingredients': 'gram flour,yogurt,turmeric,green chili,mustard oil'},
    {'name': 'Jalebi', 'ingredients': 'maida,yogurt,sugar syrup,cardamom,ghee'},
    {'name': 'Basundi', 'ingredients': 'milk,cardamom,nutmeg,dry fruits,sugar'},
    {'name': 'Makhane Ki Kheer', 'ingredients': 'fox nuts,milk,sugar,cardamom,dry fruits'},
    {'name': 'Sukhdi', 'ingredients': 'wheat flour,ghee,jaggery,dry fruits'},
    
    # Goan curries
    {'name': 'Goan Fish Curry', 'ingredients': 'fish,coconut,turmeric,red chili,onion,vinegar'},
    {'name': 'Goan Prawn Curry', 'ingredients': 'prawns,coconut milk,turmeric,chili,onion,vinegar'},
    {'name': 'Sorpotel', 'ingredients': 'pork,red chili, vinegar, ginger, garlic, cumin'},
    {'name': 'Vindaloo Goan', 'ingredients': 'pork,potatoes,red chili,vinegar,spices'},
    {'name': 'Crab Recheado', 'ingredients': 'crab,green chili,ginger,garlic,coconut,oil'},
    {'name': 'Xacuti', 'ingredients': 'meat,coconut,spices,mustard seeds,turmeric'},
    {'name': 'Ambotik', 'ingredients': 'meat,potatoes,tamarind,turmeric,chili,onion'},
    {'name': 'Pork Assado', 'ingredients': 'pork,vinegar,potatoes,onion,spices'},
    {'name': 'Sangas', 'ingredients': 'fish,coconut milk,turmeric,chili,ginger,garlic'},
    {'name': 'Tisrya Koliwada', 'ingredients': 'clams,coconut,chili,ginger,garlic,oil'},
    
    # Hyderabadi curries  
    {'name': 'Hyderabadi Dum Biryani', 'ingredients': 'meat,basmati rice,yogurt,saffron,fried onions'},
    {'name': 'Hyderabadi Haleem', 'ingredients': 'meat,wheat,lentils,spices,ghee'},
    {'name': 'Nihari Hyderabadi', 'ingredients': 'meat,yogurt,spices,ginger,garlic,oil'},
    {'name': 'Kheema Hyderabadi', 'ingredients': 'ground meat,peas,ginger,garlic,onion'},
    {'name': 'Mirchi ka Salan', 'ingredients': 'green chili,peanuts,sesame,coconut,tamarind'},
    {'name': 'Khubani ka Meetha', 'ingredients': 'apricots,cream,cardamom,nuts,sugar'},
    {'name': 'Hyderabadi Paya', 'ingredients': 'trotters,turmeric,chili,ginger,garlic,oil'},
    {'name': 'Keema Dil', 'ingredients': 'ground meat,heart,liver,ginger,garlic,spices'},
    {'name': 'Dum ka Murgh', 'ingredients': 'chicken,yogurt,spices,saffron,ghee'},
    {'name': 'Bagaara Baigan', 'ingredients': 'eggplant,peanuts,sesame,coconut,tamarind'},
    
    # Chettinad curries
    {'name': 'Chettinad Chicken', 'ingredients': 'chicken,pepper,turmeric,chili,onion,oil'},
    {'name': 'Chettinad Lamb', 'ingredients': 'lamb,pepper,turmeric,chili,garlic,ginger'},
    {'name': 'Chettinad Fish', 'ingredients': 'fish,pepper,turmeric,chili,curry leaves,oil'},
    {'name': 'Chettinad Beef', 'ingredients': 'beef,pepper,turmeric,chili,onion,oil'},
    {'name': 'Vada Chettinad', 'ingredients': 'urad flour,cumin,pepper,salt,oil'},
    {'name': 'Idli Chettinad', 'ingredients': 'rice batter,dal,salt'},
    {'name': 'Dosa Chettinad', 'ingredients': 'rice batter,oil,salt'},
    {'name': 'Puttu Chettinad', 'ingredients': 'rice flour,coconut,salt,jaggery'},
    {'name': 'Payasam Chettinad', 'ingredients': 'rice jaggery,coconut,cardamom,nuts'},
    {'name': 'Urundai Sidhan', 'ingredients': 'tapioca,jaggery,sesame,coconut'},
    
    # Mangalorean curries
    {'name': 'Mangalorean Fish Curry', 'ingredients': 'fish,coconut,turmeric,chili,onion'},
    {'name': 'Neer Dosa', 'ingredients': 'rice batter,oil,salt'},
    {'name': 'Mangalorean Biryani', 'ingredients': 'rice,meat,coconut,spices,oil'},
    {'name': 'Ghee Rice', 'ingredients': 'rice,ghee,spices,nuts'},
    {'name': 'Chikhalwali Mangalorean', 'ingredients': 'wheat flour,jaggery,ghee,dry fruits'},
    {'name': 'Mandiges', 'ingredients': 'urad flour,cumin,oil,salt'},
    {'name': 'Chakli Mangalorean', 'ingredients': 'gram flour,rice flour,turmeric,oil'},
    {'name': 'Payasam Mangalorean', 'ingredients': 'milk,jaggery,cardamom,dry fruits'},
    {'name': 'Coconut Chikhalwali', 'ingredients': 'flour,coconut,jaggery,ghee'},
    {'name': 'Rice Puttu', 'ingredients': 'rice flour,coconut,jaggery,salt'},
    
    # Assamese curries
    {'name': 'Assamese Fish Curry', 'ingredients': 'fish,turmeric,chili,ginger,garlic,oil'},
    {'name': 'Assamese Duck Curry', 'ingredients': 'duck,turmeric,chili,ginger,garlic,oil'},
    {'name': 'Aloo Pitika', 'ingredients': 'potatoes,roasted fish,ginger,green chili,oil'},
    {'name': 'Masor Tenga', 'ingredients': 'fish,turmeric,chili,ginger,garlic,tomato'},
    {'name': 'Bhaat', 'ingredients': 'rice,lentils,oil,salt,turmeric'},
    {'name': 'Chutney Assamese', 'ingredients': 'spices,ginger,garlic,green chili,oil'},
    {'name': 'Pitha', 'ingredients': 'rice flour,jaggery,coconut,salt'},
    {'name': 'Luchi Assamese', 'ingredients': 'maida,oil,salt,water'},
    {'name': 'Payesh', 'ingredients': 'rice,milk,jaggery,cardamom,dry fruits'},
    {'name': 'Khichuri', 'ingredients': 'rice,lentils,turmeric,salt,oil'},
    
    # Additional Kerala dishes
    {'name': 'Malabar Biryani', 'ingredients': 'basmati rice,meat,coconut,spices,ghee'},
    {'name': 'Kolapuri Roti', 'ingredients': 'wheat flour,salt,sesame,cumin,oil'},
    {'name': 'Puttu Kudam', 'ingredients': 'rice flour,jaggery,coconut,salt'},
    {'name': 'Paya Curry Kerala', 'ingredients': 'trotters,coconut milk,spices,turmeric'},
    {'name': 'Beef Fry Kerala', 'ingredients': 'beef,onion,ginger,garlic,chili,coconut'},
    {'name': 'Chicken Roast Kerala', 'ingredients': 'chicken,coconut,turmeric,chili,onion'},
    {'name': 'Duck Curry Kerala', 'ingredients': 'duck,coconut milk,spices,turmeric,oil'},
    {'name': 'Squid Curry Kerala', 'ingredients': 'squid,coconut milk,turmeric,chili,onion'},
    {'name': 'Crab Curry Kerala', 'ingredients': 'crab,coconut milk,turmeric,chili,onion'},
    {'name': 'Pearl Onion Curry', 'ingredients': 'pearl onion,coconut milk,turmeric,chili'},
]

# Add all new recipes to the dataframe
df_new = pd.concat([df, pd.DataFrame(indian_kerala_recipes)], ignore_index=True)

# Remove any duplicates
df_final = df_new.drop_duplicates(subset=['name', 'ingredients'], keep='first').reset_index(drop=True)

# Trim to 500 if we exceed it
if len(df_final) > 500:
    df_final = df_final.iloc[:500]

print(f"Added {len(indian_kerala_recipes)} Indian/Kerala recipes")
print(f"Final dataset: {len(df_final)} recipes")

# Save to CSV
df_final.to_csv(csv_path, index=False)
print(f"Updated CSV saved successfully!")
print(f"\nRecipes added from these regions:")
print("- Kerala Specialties")
print("- North Indian")
print("- Bengali")
print("- South Indian")
print("- Punjabi")
print("- Awadhi/Lucknowi")
print("- Rajasthani")
print("- Maharashtrian")
print("- Gujarati")
print("- Goan")
print("- Hyderabadi")
print("- Chettinad")
print("- Mangalorean")
print("- Assamese")
