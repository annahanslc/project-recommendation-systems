
import pandas as pd
from recommenders import *

pd.set_option('display.max_columns', None)

def main():
  print("Welcome to the Google Local Business Recommender!")

  user_id = str(input("What is the user id?"))
  print(f'Hello, user number {user_id}')

  n_recs = int(input("How many recommendations would you like?"))
  print(f'Great, I will give you {n_recs} recommendations')

  print('Now compiling your recommendations, please wait a few minutes...')

  print(get_svd_recommendations(user_id, n_recs))

  print('Done')

if __name__ == "__main__":
  main()
