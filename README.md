# Recommender System for Local Businesses

Imagine you're deciding where to eat, get your haircut, or spend a free afternoon—and instead of endlessly scrolling through Google reviews or sifting through star ratings, you have a trusted friend who knows your tastes and recommends exactly the places you'd love.

That's the idea behind my recommender system for local businesses: a personalized experience that goes beyond generic ratings. By understanding your preferences, behaviors, and past favorites, it suggests businesses you're likely to enjoy—just like a friend who really gets you.

No more guesswork. Just the right place, every time.

# Project Objective

My console application prompts you to enter a user_id and the number of recommendations you'd like to receive. You can then choose from three recommendation methods:

- User-based - suggests places liked by other users with similar tastes.
- Item-based - suggests places similar to ones you have rated highly.
- SVD-based - uses patterns in your past reviews to discover hidden preferences and suggest places that you might like.

Based on your selection, the application will generate and return the requested number of personalized business recommendations.

# Table of Contents

1. [About the data](#about-the-data)
2. [Collaborative filtering: user-based](#user-based-collaborative-filtering)
3. [Collaborative filtering: item-based](#item-based-collaborative-filtering)
4. [SVD (Singular Value Decomposition)](#singular-value-decomposition)
5. [Console application](#console-application)
6. [Next Steps](#next-steps)
7. [References](#references)

# About the Data 

### Original Dataset

For this project I used the Google Local Reviews Dataset (2021) developed by Jiacheng Li, Jingbo Shang and Julian McAuley at UC San Diego.
The dataset consists of user reviews for local businesses across the United States, sourced from Google Maps. Each review includes:

- A unique user ID
- A unique business ID (gmap ID)
- A star rating (1–5)
- A timestamp
- Review text (optional)

To ensure meaningful interaction data and reduce sparsity, the team at UCSD created subsets for each state with k-core filtering, which retains only users and businesses with at least 10 reviews each. This approach helps improve the quality and stability of collaborative filtering techniques, such as SVD.

For this project, I focused on reviews from the state of Utah, where I grew up. I was particularly interested in exploring what kinds of local business recommendations the system would generate for my home state.

The Utah original k-core subset has:
  - 4,858,771 reviews
  - 160,766 unique users
  - 34,689 unique businesses
No user has reviewed the same business more than once. 

### Data Subset

To improve computational efficiency, I reduced the dataset to a subset containing 10,001 users. This subset was constructed by randomly sampling 10,000 user IDs from the Utah subset and appending my own user ID (associated with my Google reviews), for a total of 10,001 users. All review records were then filtered to include only those associated with these 10,001 users.

The Utah 10,001 users subset has:
  - 305,262 reviews
  - 10,001 unique users
  - 29,040 unique businesses

# User-Based Collaborative Filtering

I implemented a user-based collaborative filtering algorithm using cosine similarity to measure how similar users are based on their past reviews. 

My recommender function will first check if the a exists in the dataset, since I am only able to find similar users if the user in question has made reviews in the past. If they have reviews in the dataset, then the following steps are taken:

  1. Identiy their top 50 most similar users, excluding themselves.
  2. For each similar user, the function retrieves their favorite businesses. Where favorite is defined as having rated those businesses a 4 or higher.
  3. Any businsses that the target user has already reviewed are filted out.
  4. The remaining favorites are combined together, where if multiple users rated the same business, their ratings are added together to represent aggregated popularity.
  5. The favorites are then sorted by the highest aggregate ratings.
  6. The function will return the top n_rec number of businesses as the final recommendations.

If the user is not found in the dataset, then the function falls back on a popularity-based list of recommendations. All businesses are ranking by a combination of their average rating and the number of reviews.



# Item-Based Collaborative Filtering


# Singular Value Decomposition


# Console Application


# Next Steps

# References
