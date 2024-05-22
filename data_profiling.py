from ydata_profiling import ProfileReport
import pandas as pd


df = pd.read_csv("updated_data_total.csv", sep="\t", encoding="iso-8859-1")

df.replace('WAHR', 1, inplace=True)
df.replace('FALSCH', 0, inplace=True)

profile = ProfileReport(df, title="Profiling Report")
profile.to_file(output_file="sgv-profile.html")