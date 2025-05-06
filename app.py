import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt  
import seaborn as sns
import numpy as np
import pandas as pd
import streamlit as st

#Load the data
data = pd.read_csv("C:/Users/deadw/OneDrive/Coding Temple Assignments/Streamlit/Starbucks-EDA2/data/cleaned_starbucks.csv")
# Add Nav Bar
col1, col2 = st.columns([3, 1])
with col2:
      page = st.selectbox("Select a page:", ["Home", "Page 2"])


# Home Page
if page == "Home":
     st.title("Starbucks Exploratory Analysis")

    # Add image
     col1, col2, col3 = st.columns([1, 2, 1])
     with col2:
      image_path = "starbucks-caramel-frappuccino-starbucks-cup-frappuccino-11562887510r3t2fh4oho.png"
      st.image(image_path)
       # Add description and greeting
     st.markdown("<span style= 'font-size: 24px; '> Welcome to the Starbucks EDA app! Take a moment to explore!!</span>", unsafe_allow_html=True)

    # Overview
     st.subheader("Overview of the Dataset")
     st.write(f"The shape of the data is: {data.shape}")
     st.write(data.describe())
     container = st.container()
     container.write("These are key statistics from the dataset. This information gives a quick summary of the nutrition metrics associated with Starbucks beverages.")

     st.markdown("<h2 style='font-size: 16px;'><strong>Initial Glimpse of the Data:</strong></h2>",
            unsafe_allow_html=True)
     st.write(data.head())

    # Add a container
     container = st.container()
     container.write("The data gives the nutritional facts for some of Starbuck's most popular menu items.")

# Page 2
elif page == "Page 2":        
    st.title("Exploratory Data Analysis")      
    st.markdown("<h2 style='font-size: 28px; color: green'><strong>Now let's dive into the data...🔎</h2>",
            unsafe_allow_html=True)
    
#Tabs
    tab1,tab2, tab3, tab4, tab5, tab6 = st.tabs(["Beverage Counts", "Calories Distribution", "Correlation Heatmap", "Average Nutrition", "Caffeine Content", "Health Ratings"])

#Calculate the counts
    with tab1:    
      category_counts=data["Beverage_category"].value_counts()    
      st.markdown("<br>", unsafe_allow_html=True)
      st.markdown("<br>", unsafe_allow_html=True)

#Barchart for Beverage Counts
      fig, ax = plt.subplots()
      sns.countplot(y='Beverage_category', data=data, order=category_counts.index, ax=ax, color="#01547a")
      ax.set_title('Count of Beverages by Category', fontsize=20, fontweight='bold')
      ax.set_xlabel('Beverage Count', fontsize=16, fontweight='bold')
      ax.set_ylabel('Beverage Category', fontsize=16, fontweight='bold')
      st.pyplot(fig)
    
      container = st.container()
      container.write("There is a total of 240 drinks included in our dataset")
    
      st.markdown("<br>", unsafe_allow_html=True)

#Calories
    with tab2:
      fig, ax = plt.subplots()
      sns.histplot(data['Calories'], bins=20, kde=True, ax=ax, color="darkgreen")
      ax.set_title('Distribution of Calories in Beverages', fontsize=14, fontweight='bold')
      plt.xlabel('Calories',fontsize=12, fontweight='bold')
      plt.ylabel('Frequency',  fontsize=12, fontweight='bold')
      st.pyplot(fig)

      container = st.container()
      container.write("Most drinks on the Starbucks ☕ menu have about 200 calories.")

# Heatmap
    with tab3:
      numeric_data = data.select_dtypes(include=['float64', 'int64'])
      correlation_matrix = numeric_data.corr()
      mask=np.triu(np.ones_like(correlation_matrix, dtype=bool))
    
      plt.figure(figsize=(12,12))
      sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap="ocean", mask=mask, square=True, vmin=-1, vmax=1)
      plt.title("Correlation Heatmap", fontsize=20, fontweight='bold')
      st.pyplot(plt)

      container = st.container()
      container.write("Here, we see that higher fat 🧈, sodium, and sugar 🧁 tends to correlate with higher calories.")

# Average Nutrition
    with tab4:
      avg_nutrition = data.groupby('Beverage_category')[['Calories', 'Sugars (g)', 'Total Fat (g)']].mean().reset_index()
      avg_nutrition_melted = avg_nutrition.melt(id_vars='Beverage_category', var_name='Nutrition', value_name='Average')

      plt.figure(figsize=(10, 6))
      sns.barplot(data=avg_nutrition_melted, x='Beverage_category', y='Average', hue='Nutrition', palette='ocean')
      plt.title('Average Nutritional Content by Beverage Category',fontsize=18, fontweight='bold' )
      plt.xlabel('Beverage Category',fontsize=14, fontweight='bold')
      plt.ylabel('Average',  fontsize=14, fontweight='bold')
      plt.xticks(rotation=45)
      plt.tight_layout()
      st.pyplot(plt)
      
      container = st.container()
      container.write("Frappuccino Blended Coffees have the highest average of Total Fat, Sugar, and Calories.")

# Caffeine
    with tab5:
      plt.figure(figsize=(12, 6))
      sns.boxplot(x='Beverage_category', y='Caffeine (mg)', data=data)
      plt.title('Caffeine Content by Beverage Category', fontsize=18, fontweight='bold')
      plt.xticks(rotation=45)
      plt.xlabel('Beverage Category',fontsize=14, fontweight='bold')
      plt.ylabel('Caffeine (mg)', fontsize=14, fontweight='bold')
      st.pyplot(plt)

      container = st.container()
      container.write("Coffee has the highest caffeine content, followed by Classic Expresso drinks.")

 # Health Ratings
    with tab6:
      def calculate_health_rating(row):   
         if row['Calories'] <= 100 and row['Sugars (g)'] <= 10:        
            return 'Healthier'   
         elif row['Calories'] <= 200 and row['Sugars (g)'] <= 30:        
            return 'Moderate'    
         else:        
             return 'Indulgent'   
 # Rating column        
      data["Health Rating"] = data.apply(calculate_health_rating, axis=1)    

      st.write(data[["Beverage_category", "Beverage", "Beverage_prep", "Health Rating"]])

# Filters
      health_ratings=data["Health Rating"].unique()
      selected_ratings=st.multiselect("Select Health Ratings", options=health_ratings)

      if selected_ratings:
        filtered_data=data[data["Health Rating"].isin(selected_ratings)]

        st.write(filtered_data[["Beverage_category","Beverage", "Beverage_prep", "Calories", "Sugars (g)", "Total Fat (g)", "Health Rating"]])

# FilteredBar Plot
        plt.figure(figsize=(10,6))
        sns.barplot(data=filtered_data, x="Beverage_category", y="Calories", hue="Health Rating", palette="ocean")
        plt.title("Health Ratings", fontsize=18, fontweight="bold")
        plt.xlabel("Calories",fontsize=14, fontweight="bold")
        plt.ylabel("Beverage Category", fontsize=14, fontweight="bold")
        plt.xticks(rotation=45)
        st.pyplot(plt)
       
      else:    
        st.write("Please select at least one health rating to filter the beverages.")             

# YOUR APP HERE!