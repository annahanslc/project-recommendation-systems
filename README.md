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

To ensure meaningful interaction data and reduce sparsity, the team at UCSD created subsets for each state with k-core filtering, which retains only users and businesses with at least 10 reviews each. This helps to alleviate the problem of the long-tail, which is when many users leave only one or two reviews, and many businesses are reviewed only a handful of times. This create a very sparse user-item matrics, making it harder for collaborative filtering models to learn reliable patterns.

For this project, I focused on reviews from the state of Utah, where I grew up. I was particularly interested in exploring what kinds of local business recommendations the system would generate for my home state.

The Utah original k-core subset has:
  - 4,858,771 reviews
  - 160,766 unique users
  - 34,689 unique businesses
No user has reviewed the same business more than once. 

### Data Subset

To improve computational efficiency, I reduced the dataset to a subset containing 10,001 users. This subset was constructed by randomly sampling 10,000 user IDs from the Utah subset and appending my own user ID (associated with my Google reviews), for a total of 10,001 users. All review records were then filtered to include only those associated with these 10,001 users.

The Utah 10,001 users subset consists of:
  - 305,262 reviews
  - 10,001 unique users
  - 29,040 unique businesses

# User-Based Collaborative Filtering

For the user-based recommender function, I implemented a user-based collaborative filtering algorithm using cosine similarity to measure how similar users are based on their past reviews. 

My recommender function will first check if the a exists in the dataset, since I am only able to find similar users if the user in question has made reviews in the past. If they have reviews in the dataset, then the following steps are taken:

  1. Identiy their top 50 most similar users, excluding themselves.
  2. For each similar user, retrieve their favorite businesses, where favorite is defined as having rated those businesses a 4 or higher.
  3. Any businsses that the target user has already reviewed are not added to the list of favorites.
  4. The list of favorties are combined together, where if multiple users rated the same business, their ratings are added together to represent aggregated popularity.
  5. The favorites are then sorted by the highest aggregate ratings.
  6. The function will return the top n_rec number of businesses as the final recommendations.

In the case of a cold-start, where the user is not found in the dataset, then the function falls back on a popularity-based list of recommendations. All businesses are ranking by a combination of their average rating and the number of reviews.


# Item-Based Collaborative Filtering

For the item-based recommender function, I found the cosine similarity between businesses' ratings to find places that are similar to the ones that a user has rated highly.

Here is a breakdown of how the function works:

  1. Idenfity the user's favorite places, which are those rated a 4 or higher.
  2. For each one of the user's favorite places, the function retrieves similar businesses using the item-to-item cosine similarity matrix.
  3. If the user has not already rated them, then the businesses are added to a list of recommendations.
  4. The recommendations are then sorted by total similarity score and their average rating
  5. Businesses with an average star rating of 3.5 are removed from the list.
  6. The top n_recs recommendations are taken from the top of the list.

To handle the cold-start issue, if the user has no prior reviews, no favorite places (under 4 stars), or there are not enough qualifying recommendations using the above method, then the results are supplemented with a fallback list of popular businesses. Again, the popular businesses are determined by the number of reviews and their average rating. These popular businesses are added to the end of the list of recommendations to ensure that the user always receives the number of suggestions that they asked for. 

# Singular Value Decomposition

My SVD (Singular Value Decomposition)–based recommender identifies hidden patterns in user-business rating data by leveraging latent factors derived from the user-item matrix. These latent features help predict how a user might rate businesses they haven't interacted with yet.

The function uses predictions generated by my best-performing SVD model, which was tuned by testing various values of k—where k represents the number of latent factors used to capture underlying user and business traits. The best performing k was 150. 

My function takes the following steps to make recommendations:

  1. For the given user, the matrix of predicted ratings is filtered by said user, then sorted by rating in descending order.
  2. Businesses that the user has already reviewed are removed from the list.
  3. The top n_rec number of businesses are then returned as recommendations.

If the user has no review history, a cold-start issue, then it falls back to recommending the most popular businesses. This ensures that even new users receive meaningful recommendations.

The recommendation returns the following information for the user's reference:

  1. 'gmap_id': the unique business identifier
  2. 'pred_rating': the user's predicted ratings for the businesses
  3. 'name': the business name for easy lookup
  4. 'avg_rating': the average community rating


# Console Application

To make the recommender system easy to interact with, I built a simple console application that allows the user to request personalized recommendations directly from the command line. It also allows the user to choose which recommender method to use.

The program welcomes the user and prompts the user to input a "user_id". 

It then asks for the desired number of recommendations "n_recs".

Next, the user is asked to choose from the following 3 different types of recommenders:

  1. User-based - suggests places liked by other users with similar tastes.
  2. Item-based - suggests places similar to ones you have rated highly.
  3. SVD-based - uses patterns in your past reviews to discover hidden preferences and suggest places that you might like.

It will then proceed to compile n_recs recommendations for user# user_id using the selected method. 
After 1-2 minutes, the programs outputs a list of recommendations.

Below are screenshot from the application:

### Example 1) Using option 1: user-based

![Screenshot 2025-04-13 at 5 14 40 PM](https://github.com/user-attachments/assets/1efdcd98-5102-444d-bfb2-c9ca7d567086)

### Example 2) Using option 2: item-based

![Screenshot 2025-04-13 at 5 15 50 PM](https://github.com/user-attachments/assets/9dc7c627-ec81-488e-9edc-1b1361ea9959)

### Example 3) Using option 3: SVD-based

![Screenshot 2025-04-13 at 5 17 02 PM](https://github.com/user-attachments/assets/cae902be-d65c-4ac3-98be-2a699fa4d427)


# Next Steps

# References
