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

            week -- list of shape (n,)
            day_of_week -- list of shape (n,)
            backup_start_time -- list of shape (n,)
            workflow_id -- list of shape (n,)
            file_name -- list of shape (n,)
            size_of_backup -- list of shape (n,)
            backup_time -- list of shape (n,)
        """

        # n = number of examples, d = dimensionality
        self.week = None
        self.day_of_week = None
        self.backup_start_time = None
        self.workflow_id = None
        self.file_name = None
        self.size_of_backup = None
        self.backup_time = None

    def load(self, filename):
        """Load csv file into userId, movieId, ratings."""

        # determine filename
        dataset= pd.read_csv(filename)
        self.week = dataset['Week #'].tolist()
        self.day_of_week = dataset['Day of Week'].tolist()
        self.backup_start_time = dataset['Backup Start Time - Hour of Day'].tolist()
        self.workflow_id = dataset['Work-Flow-ID'].tolist()
        self.file_name = dataset['File Name'].tolist()
        self.size_of_backup = dataset['Size of Backup (GB)'].tolist()
        self.backup_time = dataset['Backup Time (hour)'].tolist()

# helper functions
def load_data_network(filename):
    """Load csv file into Data_ratings class."""
    data = Data()
    data.load(filename)
    return data