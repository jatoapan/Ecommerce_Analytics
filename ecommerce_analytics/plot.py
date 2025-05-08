import pandas as pd
import matplotlib.pyplot as plt

def plot_completeness_barplot(df, title=None):
    missing = df.isna().sum()
    complete = df.count()
    completeness_df = pd.DataFrame({
        "complete": complete,
        "missing": missing,
        "total": complete + missing
    })
    completeness_df = completeness_df[["missing", "complete", "total"]]
    completeness_df.index = completeness_df.index.str.replace("_|-", " ", regex=True)
    completeness_df.index = completeness_df.index.str.title()
    completeness_df.plot(kind="barh", color=["#d62728", "#1f77b4", "#2ca02c"], figsize=(6, 3.5))
    plt.title(title)
    plt.legend(["Missing", "Complete", "Total"],loc="upper right")
    plt.show()

def plot_uniqueness_barplot(df, title=None):
    description_df = df.nunique().transpose()
    description_df.index = description_df.index.str.replace("_|-", " ", regex=True)
    description_df.index = description_df.index.str.title()
    description_df.plot(kind="barh", figsize=(6, 3.5))
    plt.title(title)
    plt.show()