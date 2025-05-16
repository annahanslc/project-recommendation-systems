
import pandas as pd
import json
import gzip

# define file paths

path_meta = '../original_data/meta-Utah.json.gz'
path_pivot_subset = '../data/subset.parquet'
path_reviews_subset = '../data/subset_reviews.parquet'
path_user_sim = '../data/subset_user_sim.parquet'
path_item_sim = '../data/subset_item_sim.parquet'

# define a function for reading the data using a generator

def parse_json(path):
  """
  Parses a gzipped JSON file line by line.

  Accepts a path of a gzipped JSON file, assuming that the file is .json.gz file type,
  and yields each line as a parsed JSON object.

  Args:
    path (str): Path to the gzipped JSON file.

  Yields:
    dict: Python dictionary representing one JSON object per line
  """

  g = gzip.open(path, 'r')
  for l in g:
    yield json.loads(l)

# define a function to get all the reviews for a user, sorted by rating in descending order

def get_user_rated_sorted(user_id, df):
    """
    Retrieves and sorts reviews submitted by a specific user.

    Filters a DataFrame by user_id to extract all reviews with the given user ID,
    then returns a new DataFrame containing gmap_id and rating in pairs, sorted by the rating in descending order.

    Args:
      user_id (str): Google User Id for the reviewer
      df (pd.DataFrame): DataFrame with all reviews for all users in the dataset

    Returns:
      pd.DataFrame: DataFrame containing all the reviews for a user with columns ['gmap_id', 'rating'], sorted by rating in descending order.
    """

    user_reviews = df[df['user_id'] == user_id]
    user_rated = dict(zip(user_reviews['gmap_id'], user_reviews['rating']))
    user_rated = pd.DataFrame(list(user_rated.items()), columns=['gmap_id', 'rating'])
    user_rated.sort_values(by='rating', ascending=False, inplace=True)
    return user_rated

# define a function to get a user's favorite places, favorites defined as being rated 4 or higher

def get_favorites(user_id, df):
  """
  Retrieves a user's favorites places (rated 4 stars or higher).

  Calls the external function get_user_rated_sorted() to retrieve all the reviews of given user.
  Filters this data to include only places that the user rated with 4 stars or more, assuming
  these represent teh user's "favorites".

  Args:
    user_id (str): User's Google Map Reviewer ID
    df (pd.DataFrame): DataFrame that contains all reviews in the dataset.

  Returns:
    pd.DataFrame: DataFrame with the columns ['gmap_id', 'rating'] of all places that the given user has rated with 4 stars or more,
    sorted by rating in descending order.
  """

  user_rated_sorted = get_user_rated_sorted(user_id, df)
  favorites = user_rated_sorted[user_rated_sorted['rating'] >= 4]
  return favorites

# define a function to get n most popular businesses, popular determined as 1) the most # of reviews and 2) highest average review

def get_popular(n, df):
  """
  Retrieves the top n most popular places from a dataset of reviews.

  Groups the input DataFrame by place ('gmap_id') and aggregates by:
    1) Number of reviews (count)
    2) Average rating (mean)

  Popularity is determined by first sorting places by the number of reviews, then by the average rating, in descending order.
  Returns the top n places based on this ranking.

  Args:
    n (int): The number of popular places desired.
    df (pd.DataFrame): A DataFrame containing all the reviews in the dataset.

  Returns:
    pd.Dataframe: DataFrame containing n number of the most popular places.
  """

  popular = df.groupby('gmap_id')['rating'].agg(['count','mean']).sort_values(by=['count','mean'], ascending=False)
  return popular.head(n)

# create a function to return the business name using the gmap_id

def get_business_name(gmap_id):
  """
  Searches for a business's name in the metadata using 'gmap_id'.

  Defines a generator that parses the meta data from filepath, then uses the generator to search
  for a given 'gmap_id' to return the 'name' of the place.

  Args:
    gmap_id (str): Google maps place id for the business.

  Returns:
    str: The name of the business.
  """

  meta_generator = parse(path_meta)
  for place in meta_generator:
    if place.get('gmap_id') == gmap_id:
      name = place['name']
      break
  return name

# create a function to return the business rating using the gmap_id

def get_business_rating(gmap_id):
  """
  Retrieves a place's rating from metadata using its gmap_id.

  Defines a generator to access the metadata row by row. Then uses the generator to search
  by 'gmap_id' and returns the 'avg_rating' of the place.

  Args:
    gmap_id (str): Google maps place id for the business.

  Returns:
    int: The average rating of the business.
  """

  meta_generator = parse(path_meta)
  for place in meta_generator:
    if place.get('gmap_id') == gmap_id:
      avg_rating = place['avg_rating']
      break
  return avg_rating
