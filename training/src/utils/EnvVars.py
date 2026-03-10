import os
from dotenv import load_dotenv

load_dotenv("training/.env", override=True)

class EnvVars():
    def __init__(self):
        self.ModelOutPut= os.getenv("MODEL_OUTPUT")
        self.FEAUTURES=os.getenv("FEATURES")
        self.TRAINING_DATA_PATH_MARK_STRUCT= os.getenv("TRAINING_DATA_PATH_MARK_STRUCT")
        self.N_ESTIM=os.getenv("N_ESTIM")
        self.MAX_DEPTH=os.getenv("MAX_DEPTH")
        self.LEARNING_RATE=os.getenv("LEARNING_RATE")
        self.SUBSMPLE=os.getenv("SUBSMPLE")
        self.COLSMPL_BY_TREE=os.getenv("COLSMPL_BY_TREE")
        self.RANDOM_ST=os.getenv("RANDOM_ST")
        self.MODEL_OUTPUT=os.getenv("MODEL_OUTPUT")
        self.FEATURES_OUTPUT=os.getenv("FEATURES_OUTPUT") 





# if __name__ == "__main__":
#     envVars=EnvVars()
#     list_of_features=list(envVars.FEAUTURES.split(','))
#     print(list_of_features)
