"""
Author      : Fangyao Liu
Description : ML utilties
"""


import pandas as pd



######################################################################
# classes
######################################################################

class Data:

    def __init__(self):
        """
        Data_ratings class.

        Attributes
        --------------------
            userId -- list of shape (n,)
            movieId -- list of shape (n,)
            ratings -- list of shape (n,)
        """

        # n = number of examples, d = dimensionality
        self.userID = None
        self.movieID = None
        self.ratings = None
        self.titles = None
        self.genres = None


    def load_ratings(self, filename):
        """Load csv file into userId, movieId, ratings."""

        # determine filename
        dataset= pd.read_csv(filename)
        self.userID = dataset['userId'].tolist()
        self.movieID = dataset['movieId'].tolist()
        self.ratings = dataset['rating'].tolist()

    def load_movies(self, filename):
        """Load csv file into userId, movieId, ratings."""

        # determine filename
        dataset= pd.read_csv(filename)
        self.movieID = dataset['movieId'].tolist()
        self.titles = dataset['title'].tolist()
        self.genres = dataset['genres'].tolist()



# helper functions
def load_data_ratings(filename):
    """Load csv file into Data_ratings class."""
    data_ratings = Data()
    data_ratings.load_ratings(filename)
    return data_ratings

def load_data_movies(filename):
    """Load csv file into Data_ratings class."""
    data_movies = Data()
    data_movies.load_movies(filename)
    return data_movies