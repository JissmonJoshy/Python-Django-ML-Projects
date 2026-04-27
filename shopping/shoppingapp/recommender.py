import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from .models import Bookings, Products


def get_booking_df():
    qs = Bookings.objects.filter(
        status__in=["Booked", "Completed"]
    ).values('cust_id', 'Product_id', 'count')

    return pd.DataFrame(qs)


def build_user_item_matrix(df):
    return pd.pivot_table(
        df,
        index='cust_id',
        columns='Product_id',
        values='count',
        aggfunc='sum',
        fill_value=0
    )


def recommend_products(user_id, top_n=6):
    df = get_booking_df()

    # 🧊 Cold start
    if df.empty or user_id not in df['cust_id'].values:
        return Products.objects.order_by('-qty')[:top_n]

    user_item = build_user_item_matrix(df)

    similarity = cosine_similarity(user_item.T)
    sim_df = pd.DataFrame(
        similarity,
        index=user_item.columns,
        columns=user_item.columns
    )

    purchased = user_item.loc[user_id]
    purchased = purchased[purchased > 0].index.tolist()

    scores = pd.Series(dtype=float)

    # Category boost
    product_types = dict(
        Products.objects.values_list('id', 'type')
    )

    CATEGORY_WEIGHT = {
        "Vegetables": 1.6,
        "Fruits": 1.4,
        "Spices": 1.3,
        "Grocery": 1.2
    }

    for pid in purchased:
        weight = CATEGORY_WEIGHT.get(product_types.get(pid), 1)
        scores = scores.add(sim_df[pid] * weight, fill_value=0)

    scores = scores.drop(purchased, errors='ignore')
    scores = scores.sort_values(ascending=False)

    product_ids = scores.head(top_n).index.tolist()
    return Products.objects.filter(id__in=product_ids)