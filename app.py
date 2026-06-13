import streamlit as st
import requests

# Set up page configuration
st.set_page_config(
    page_title="Advanced News Aggregator",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API Configuration
API_URL = "https://newsapi.org/v2/top-headlines"
API_KEY = "54a6a817b1df4b64a349a698a888fc54"

# Available options for filtering
COUNTRIES = {
    "United States": "us",
    "India": "in",
    "United Kingdom": "gb",
    "Australia": "au",
    "Canada": "ca",
    "Germany": "de",
    "Japan": "jp"
}

CATEGORIES = [
    "general",
    "business",
    "entertainment",
    "health",
    "science",
    "sports",
    "technology"
]

# Title and Description
st.title("📰 Advanced Real-Time News Aggregator")
st.markdown("Stay updated with top headlines from around the world. Filter by country, topic, or search via keywords.")
st.write("---")

# Sidebar for Filters
st.sidebar.header("Filter & Search Controls")

# 1. Location Filter
country_label = st.sidebar.selectbox("Select Country/Location", list(COUNTRIES.keys()), index=0)
country_code = COUNTRIES[country_label]

# 2. Topic/Category Filter
category = st.sidebar.selectbox("Select Topic/Category", CATEGORIES, index=0)

# 3. Keyword Search
keyword = st.sidebar.text_input("Search Keyword (Optional)", placeholder="e.g., AI, Stocks, Football")

# 4. Number of Articles
page_size = st.sidebar.slider("Number of Articles", min_value=5, max_value=50, value=20, step=5)

# Fetch Data Button
if st.sidebar.button("Fetch Headlines", type="primary"):
    
    # Construct query parameters
    # Note: NewsAPI top-headlines endpoint allows either country/category OR q, 
    # but combining them works as an intersection. If q is too specific, results might be limited.
    params = {
        "apiKey": API_KEY,
        "pageSize": page_size
    }
    
    if country_code:
        params["country"] = country_code
    if category:
        params["category"] = category
    if keyword:
        params["q"] = keyword

    with st.spinner("Fetching latest news..."):
        try:
            response = requests.get(API_URL, params=params)
            response_data = response.json()
            
            if response.status_code == 200:
                articles = response_data.get("articles", [])
                
                if not articles:
                    st.warning("No articles found matching your criteria. Try adjusting your filters or keyword.")
                else:
                    st.success(f"Successfully fetched {len(articles)} articles!")
                    
                    # Display articles in a clean grid or list format
                    for index, article in enumerate(articles):
                        st.subheader(f"{index + 1}. {article.get('title')}")
                        
                        # Author and Source Info
                        source = article.get("source", {}).get("name", "Unknown Source")
                        author = article.get("author")
                        author_str = f" by {author}" if author else ""
                        st.caption(f"**Source:** {source}{author_str} | **Published at:** {article.get('publishedAt')[:10]}")
                        
                        # Layout layout for Image + Description
                        col1, col2 = st.columns([1, 3])
                        
                        image_url = article.get("urlToImage")
                        if image_url:
                            col1.image(image_url, use_container_width=True)
                        else:
                            # Placeholder if no image is available
                            col1.image("https://via.placeholder.com/150x100.png?text=No+Image", use_container_width=True)
                            
                        col2.write(article.get("description") or "No description available for this article.")
                        col2.markdown(f"[Read full article strictly at the source]({article.get('url')})")
                        
                        st.write("---")
            else:
                # Handle API specific error messages
                error_msg = response_data.get("message", "Unknown error occurred.")
                st.error(f"Failed to fetch data from API. Error: {error_msg} (Status Code: {response.status_code})")
                
        except requests.exceptions.RequestException as e:
            st.error(f"A connection error occurred: {e}")
else:
    st.info("💡 Adjust the filters in the sidebar and click **Fetch Headlines** to load the news!")
