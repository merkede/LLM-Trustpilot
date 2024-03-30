import streamlit as st
import pandas as pd

data = pd.read_csv("import pandas as pd

data_url = "https://raw.githubusercontent.com/merkede/LLM-Trustpilot/main/Trustpilot_LLM.csv"
data = pd.read_csv(data_url)/Trustpilot_LLM.csv")


# Define regular expressions
topic_category_regex = r"Topic Category: (.*?)\n"
themes_regex = r"Themes: (.*?)\n"
pain_point_regex = r"Pain Point: (.*?)\n"
detailed_topic_regex = r"Detailed Topic: (.*?)\n"
main_emotion_regex = r"Main Emotion: (.*?)\n"
emotion_explanation_regex = r"Emotion Explanation: (.*)"

# Extract data from the "summary" column using regular expressions
data["Topic Category"] = data["summary"].str.extract(topic_category_regex, expand=False).str.strip()
data["Themes"] = data["summary"].str.extract(themes_regex, expand=False).str.strip()
data["Pain point"] = data["summary"].str.extract(pain_point_regex, expand=False).str.strip()
data["Detailed Topic"] = data["summary"].str.extract(detailed_topic_regex, expand=False).str.strip()
data["Main Emotion"] = data["summary"].str.extract(main_emotion_regex, expand=False).str.strip()
data["Emotion Explanation"] = data["summary"].str.extract(emotion_explanation_regex, expand=False).str.strip()


# Streamlit app
def main():
    st.title("Customer Feedback Dashboard")
    
    # Sidebar filters
    topic_categories = st.sidebar.multiselect("Topic Category", data["Topic Category"].unique())
    emotions = st.sidebar.multiselect("Main Emotion", data["Main Emotion"].unique())
    
    # Filter data based on sidebar selections
    filtered_data = data[data["Topic Category"].isin(topic_categories)]
    filtered_data = filtered_data[filtered_data["Main Emotion"].isin(emotions)]
    
    # Display key metrics
    st.subheader("Key Metrics")
    total_reviews = len(filtered_data)
    avg_rating = filtered_data["Rating"].mean()
    st.write(f"Total Reviews: {total_reviews}")
    st.write(f"Average Rating: {avg_rating:.2f}")
    
    # Display topic distribution
    st.subheader("Topic Distribution")
    topic_counts = filtered_data["Topic Category"].value_counts()
    st.bar_chart(topic_counts)
    
    # Display emotion distribution
    st.subheader("Emotion Distribution")
    emotion_counts = filtered_data["Main Emotion"].value_counts()
    st.bar_chart(emotion_counts)
    
    # Display top pain points
    st.subheader("Top Pain Points")
    pain_points = filtered_data["Pain point"].value_counts().head(5)
    st.write(pain_points)
    
    # Display detailed analysis
    st.subheader("Detailed Analysis")
    selected_topic = st.selectbox("Select Topic Category", filtered_data["Topic Category"].unique())
    topic_data = filtered_data[filtered_data["Topic Category"] == selected_topic]
    
    if not topic_data.empty:
        st.write("Detailed Topic:")
        st.write(topic_data["Detailed Topic"].iloc[0])
        
        st.write("Main Emotion:")
        st.write(topic_data["Main Emotion"].iloc[0])
        
        st.write("Emotion Explanation:")
        st.write(topic_data["Emotion Explanation"].iloc[0])
    else:
        st.write("No data available for the selected topic.")
    
    # Display actionable insights
    st.subheader("Actionable Insights")
    if "Frustration" in emotion_counts.index:
        st.write("- Address the main sources of frustration identified in the reviews.")
    if "Customer Service" in topic_counts.index:
        st.write("- Improve customer service quality and responsiveness.")
    if filtered_data["Themes"].str.contains("Communication", na=False).any():
        st.write("- Enhance communication channels and provide timely updates to customers.")
    if "Pricing" in topic_counts.index:
        st.write("- Review pricing strategies and consider offering competitive rates.")
    if "Website/App" in topic_counts.index:
        st.write("- Optimize the website/app for better user experience and functionality.")

if __name__ == "__main__":
    main()
