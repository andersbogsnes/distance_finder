from distances import Distances
import pandas as pd

client = Distances('sqlite:///test.db')
df = pd.DataFrame({"from_address": ["Midtermolen 7, 2100",
                                    "Bogholder Allé 29A, 2720",
                                    "Rådhuspladsen 2-4, 1550"],
                   "to_address": ["Halmtorvet 29C, 1700",
                                  "Linnésgade 16D, 1361",
                                  "Borgergade 93, 1300"]})

client.import_data_from_df(df, from_column='from_address', to_column='to_address')
