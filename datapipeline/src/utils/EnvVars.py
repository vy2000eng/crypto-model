
import os
from dotenv import load_dotenv
load_dotenv("datapipeline/.env", override=True)


class EnvVars:

    def __init__(self):
        self.B_API_KEY = os.getenv("B_API_KEY")
        self.B_SECRET_KEY=os.getenv("B_SECRET_KEY")
        self.TRAINING_DATA_PATH = os.getenv("TRAINING_DATA_PATH")
        self.TRAINING_DATA_PATH_MARK_STRUCT = os.getenv("TRAINING_DATA_PATH_MARK_STRUCT")
        self.START_DATE=os.getenv("START_DATE")





