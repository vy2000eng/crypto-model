



from src.controller.DataVisualizerController import DataVisualizerController


if __name__ == "__main__":

    data_visualizer_controller = DataVisualizerController()
    df = data_visualizer_controller.loadCsv()
   # data_visualizer_controller.generate_full_report(df)

    

    data_visualizer_controller.feature_correlation(df)
    # data_visualizer_controller.visualizeData(df)
    # data_visualizer_controller.visualizeFeatureSignal(df)
    # data_visualizer_controller.price_momentum_vs_returns(df)
    #data_visualizer_controller.funding_regimes(df)

    # data_visualizer_controller.feature_vs_future_return(df, "rsi")
    # data_visualizer_controller.feature_vs_future_return(df, "funding_rate")
    # data_visualizer_controller.feature_vs_future_return(df, "price_momentum")
    # data_visualizer_controller.feature_vs_future_return(df, "bb_percent")


    #data_visualizer_controller.feature_bucket_returns(df, "funding_rate")
