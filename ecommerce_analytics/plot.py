import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plot_completeness_barplot(df, column, df_name=None):
    completeness_df = df[column]
    completeness_df = completeness_df.isna().agg(["sum","count"]).transpose()
    completeness_df["Total Data"] = len(df)
    completeness_df = round(completeness_df/len(df), 2)
    completeness_df.reset_index(inplace=True)
    completeness_df.rename(columns={"index":"Column","sum":"Missing Data","count":"Complete Data"},inplace=True)
    completeness_df = completeness_df.melt(
        id_vars="Column", 
        value_vars=["Missing Data", "Complete Data", "Total Data"],
        var_name="Data Type",
        value_name="Proportion"
    )
    completeness_df["Column"] = completeness_df["Column"].str.replace(r"[,.:;_\-]"," ", regex=True).str.title()
    sns.catplot(
        data=completeness_df,
        kind="bar",
        x="Proportion",
        y="Column",
        hue="Data Type",
        hue_order=["Total Data","Complete Data","Missing Data"],
        palette = {"Complete Data": '#1f77b4', "Missing Data": '#d62728', "Total Data":"#2ca02c"},
        edgecolor='black'
    )
    plt.title(f"Barplot for {df_name} DataFrame Completeness" if df_name else "Barplot")
    plt.show()

def plot_uniqueness_barplot(df, column, df_name=None):
    description_df = df[column]
    description_df = description_df.agg(["nunique"]).transpose()
    description_df.reset_index(inplace=True)
    description_df.rename(columns={"index":"Column","nunique":"Unique Values"},inplace=True)
    description_df["Column"] = description_df["Column"].str.replace(r"[,.:;_\-]"," ", regex=True).str.title()
    description_df.sort_values(["Unique Values"],ascending=False,inplace=True)
    sns.catplot(
        data=description_df,
        kind="bar",
        x="Unique Values",
        y="Column",
        hue="Column",
        edgecolor='black'
    )
    plt.title(f"Barplot for {df_name} DataFrame Unique Values" if df_name else "Barplot")
    plt.show()