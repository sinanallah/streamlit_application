import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def get_dataset_statistics(data):
    num_rows = len(data)
    num_cols = len(data.columns)
    data_types = data.dtypes.value_counts()
    num_categorical = len(data.select_dtypes(include=['object']))
    num_numerical = len(data.select_dtypes(include=['int64', 'float64']))
    num_boolean = len(data.select_dtypes(include=['bool']))
    
    statistics = {
        "Number of rows": num_rows,
        "Number of columns": num_cols,
        "Data types": data_types.to_dict(),
        "Number of categorical variables": num_categorical,
        "Number of numerical variables": num_numerical,
        "Number of boolean variables": num_boolean
    }
    
    return statistics

def get_five_number_summary(column_data):
    min_val = np.min(column_data)
    q1 = np.percentile(column_data, 25)
    median = np.median(column_data)
    q3 = np.percentile(column_data, 75)
    max_val = np.max(column_data)

    summary = {
        "Minimum": min_val,
        "Q1": q1,
        "Median": median,
        "Q3": q3,
        "Maximum": max_val
    }

    return summary
  
def get_value_counts(column_data):
    value_counts = column_data.value_counts()
    return value_counts

web_apps = st.sidebar.selectbox("Select Web Apps",
                                ("Exploratory Data Analysis", "Distributions, Correlation Analysis"))
if web_apps == "Exploratory Data Analysis":

  uploaded_file = st.sidebar.file_uploader("Choose a file")

  if uploaded_file is not None:
    # Can be used wherever a "file-like" object is accepted
    df = pd.read_csv(uploaded_file)
    show_df = st.checkbox("Show Data Frame", key="disabled")

    if show_df:
      st.write(df)
      
    statistics = get_dataset_statistics(df)
            
    st.write("Dataset Statistics:")
    for stat, value in statistics.items():
        st.write(f"- {stat}: {value}")

    column_type = st.sidebar.selectbox('Select Data Type',
                                       ("Numerical", "Categorical"))

    if column_type == "Numerical":
      numerical_columns = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
      selected_column = st.sidebar.selectbox('Select a Column', numerical_columns)
      st.write(f"Selected Column: {selected_column}")
      column_data = df[selected_column]
      summary = get_five_number_summary(column_data)
      
      st.write("Five-Number Summary:")
      summary_table = pd.DataFrame(summary, index=["Values"])
      st.table(summary_table)

      # Distribution plot
      num_bins = st.slider('Number of Bins', min_value=5, max_value=100, value=30)
      opacity = st.slider('Opacity', min_value=0.0, max_value=1.0, step=0.1, value=1.0)
      hist_color_key = f"hist_color_{selected_column}"
      choose_color = st.color_picker('Pick a Color', "#69b3a2", key=hist_color_key)

      plt.figure(figsize=(8, 6))
      sns.histplot(column_data, kde=True, color=choose_color, bins=num_bins, alpha=opacity)
      plt.title(f"Distribution of {selected_column}")
      plt.xlabel(selected_column)
      plt.ylabel('Density')
      st.pyplot(plt)
      
      # Heat Map
      plt.figure(figsize=(10, 8))
      corr = df.select_dtypes(include=['int64', 'float64']).corr()
      sns.heatmap(corr, annot=True, cmap='coolwarm')
      plt.title("Correlation Heatmap")
      st.pyplot(plt.gcf())
      
      
    elif column_type == "Categorical":
      categorical_columns = df.select_dtypes(include=['object']).columns.tolist()
      selected_column = st.sidebar.selectbox('Select a Column', categorical_columns)
      st.write(f"Selected Column: {selected_column}")
      column_data = df[selected_column]
      
      column_data = column_data.dropna().astype(str)
      
      st.write("Value Counts:")
      value_counts = get_value_counts(column_data)
      value_counts_table = pd.DataFrame({'Category': value_counts.index, 'Count': value_counts.values})
      st.table(value_counts_table)

      # Customized bar plot
      bar_color_key = f"bar_color_{selected_column}"
      choose_color = st.color_picker('Pick a Color', "#69b3a2", key=bar_color_key)

      plt.figure(figsize=(10, 6))
      sns.barplot(x=value_counts_table['Category'], y=value_counts_table['Count'], color=choose_color)
      plt.title(f"Value Counts of {selected_column}")
      plt.xlabel(selected_column)
      plt.ylabel('Count')
      plt.xticks(rotation=45)
      st.pyplot(plt)
