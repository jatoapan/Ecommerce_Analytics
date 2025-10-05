import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re

def completeness_barplot(df, columns, df_name=None):
    completeness_df = df[columns].isna().agg(["sum"]).transpose()
    completeness_df["Complete Values"] = len(df) - completeness_df["sum"]
    completeness_df["Complete Data"] = round(completeness_df["Complete Values"]/len(df), 2)
    completeness_df.rename(columns={"sum": "Missing Values"}, inplace=True)
    completeness_df["Missing Data"] = round(completeness_df["Missing Values"]/len(df), 2)
    completeness_df.reset_index(inplace=True)
    completeness_df.rename(columns={"index": "Column"}, inplace=True)
    order_columns = ["Column", "Complete Values", "Complete Data", "Missing Values", "Missing Data"]
    completeness_df = completeness_df[order_columns]
    print(completeness_df.to_string(index=False))
    completeness_df = completeness_df.melt(
        id_vars="Column", 
        value_vars=["Missing Data", "Complete Data"],
        var_name="Data Type",
        value_name="Proportion"
    )
    completeness_df["Column"] = completeness_df["Column"].str.replace(r"[,.:;_\-]", " ", regex=True).str.title()
    sns.catplot(
        data=completeness_df,
        kind="bar",
        x="Proportion",
        y="Column",
        hue="Data Type",
        hue_order=["Complete Data", "Missing Data"],
        palette = {"Complete Data": '#1f77b4',"Missing Data": '#d62728'},
        edgecolor="black"
    )
    plt.title(f"Barplot for {df_name} DataFrame Completeness" if df_name else "Barplot")
    plt.show()

def uniqueness_barplot(df, columns, df_name=None):
    description_df = df[columns].agg(["nunique"]).transpose()
    description_df.rename(columns={"nunique": "Unique Values"}, inplace=True)
    description_df.reset_index(inplace=True)
    description_df.rename(columns={"index": "Column"}, inplace=True)
    print(description_df.to_string(index=False))
    description_df["Column"] = description_df["Column"].str.replace(r"[,.:;_\-]", " ", regex=True).str.title()
    description_df.sort_values(["Unique Values"],ascending=False, inplace=True)
    sns.catplot(
        data=description_df,
        kind="bar",
        x="Unique Values",
        y="Column",
        hue="Column",
        edgecolor="black"
    )
    plt.title(f"Barplot for {df_name} DataFrame Unique Values" if df_name else "Barplot")
    plt.show()

def activity_summary_plot(df, subject_column, transaction_column, subject_name=None):
    total_subjects = df[subject_column].nunique()
    transactions_per_subject = df.groupby(subject_column, observed=False)[transaction_column].nunique()
    subjects_with_transactions = transactions_per_subject > 0
    total_active_subjects = subjects_with_transactions.sum()
    subjects_without_transactions = transactions_per_subject == 0
    total_inactive_subjects = subjects_without_transactions.sum()
    summary_data = {
        "Status": ["Active", "Inactive", "Total"],
        "Quantity": [total_active_subjects, total_inactive_subjects, total_subjects]
    }
    summary_df = pd.DataFrame(summary_data)
    summary_df["Proportion"] = round(summary_df["Quantity"] / total_subjects, 2)
    summary_df.sort_values(["Quantity"], ascending=False, inplace=True)
    print(summary_df.to_string(index=False))
    sns.catplot(
        data=summary_df,
        kind="bar",
        x="Proportion",
        y="Status",
        edgecolor="black",
        hue="Status",
        palette={"Active": '#1f77b4', "Inactive": '#d62728', "Total": '#2ca02c'}
    )
    plt.title(f"Transactional Activity Summary for {subject_name}" if subject_name else "Transactional Activity Summary")
    plt.show()

def category_totals_plot(df, category_column, metric_column, limit=None):
    total_metric = df[metric_column].sum()
    summary_df = df.groupby(category_column, observed=False).agg(Total=(metric_column, 'sum'))
    summary_df.reset_index(inplace=True)
    summary_df["Proportion"] = round(summary_df["Total"] / total_metric, 2)
    y_column_name = re.sub(r"[,.:;_\-]", " ", category_column).title()
    summary_df.rename(columns={category_column: y_column_name}, inplace=True)
    summary_df.sort_values("Total", ascending=False, inplace=True)
    print(summary_df.to_string(index=False))
    if limit: 
        summary_df = summary_df.head(n=limit)
    sorted_categories = summary_df[y_column_name].tolist()
    sns.catplot(
        data=summary_df,
        kind="bar",
        x="Proportion",
        y=y_column_name,
        edgecolor="black",
        hue=y_column_name,
        order=sorted_categories,
        hue_order=sorted_categories
    )
    plt.title(f"Proportional Totals by {y_column_name}")
    plt.show()

def custom_line_plot(df, x_column, y_column, title=None):
    chart = sns.relplot(data=df, x=x_column, y=y_column, kind="line")
    x_label_name = re.sub(r"[,.:;_\-]", " ", x_column).title()
    y_label_name = re.sub(r"[,.:;_\-]", " ", y_column).title()
    chart.set_axis_labels(x_var=x_label_name, y_var=y_label_name)
    plt.title(title if title else f"{x_label_name} vs. {y_label_name} Line Plot")
    plt.xticks(rotation=45)
    plt.show()

def custom_box_plot(df, x_column, title=None):
    chart = sns.catplot(data=df, x=x_column, kind="box")
    x_label_name = re.sub(r"[,.:;_\-]", " ", x_column).title()
    chart.set_axis_labels(x_var=x_label_name)
    plt.title(title if title else f"Boxplot for {x_label_name}")
    plt.show()

def custom_bar_plot(df, x_column, y_column, hue_column=None, title=None):
    chart = sns.catplot(data=df, x=x_column, y=y_column, hue=hue_column, kind="bar")
    x_label_name = re.sub(r"[,.:;_\-]", " ", x_column).title()
    y_label_name = re.sub(r"[,.:;_\-]", " ", y_column).title()
    chart.set_axis_labels(x_var=x_label_name, y_var=y_label_name)
    plt.title(title if title else f"{x_label_name} vs. {y_label_name} Barplot")
    plt.xticks(rotation=45)
    plt.show()