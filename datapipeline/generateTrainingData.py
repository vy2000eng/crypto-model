

from src.utils.EnvVars import EnvVars
from src.Client.BinanaceClient import BinanceClient
from src.controller.PipelineController import PipelineController

if __name__ == "__main__":

    pipeline        = PipelineController()
    df = pipeline.generate_training_data()
    pipeline.convert_df_to_csv(df)
    print(df.tail(10))

