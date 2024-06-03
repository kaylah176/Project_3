import streamlit as st

def main():
    # Title of the web app
    st.title("Welcome to PropShare (Propery + Shares)")

    # Summary of the web app
    st.header("Summary")
    st.write("""
        This web application is designed to provide users with insightful data analysis and visualizations regarding the real estate property they're investing in.
        You can explore different sections using the sidebar on the left. Each section offers unique features
        and functionalities to help you interact with the real estate property value and tokens in various ways.
    """)

    # Navigation instructions
    st.header("How to Navigate")
    st.write("""
        To navigate through the app, use the sidebar on the left. Here are the main sections available:
        - **Home:** You are currently here. This section provides an overview and navigation instructions.
        - **NFT (1) and Ownership Tokens (100):** This section allows you to mint an NFT that will represent the real estate property you want to invest in.
        This needs to be done under a holding company, also known as an LLC. Through this, each stakeholder in the LLC has the ability to purchase or sell to others in the LLC. 
        Here are some basic rules: 
            - There are a total of 100 shares, each representing 1% ownership of the property.
            - You can not sell to yourself. Only to other individuals in the LLC or back to the holding company.
            - You can make updates to your contract's description once its deployed and even update the house's value.
        - **Real Estate Token Investment Analysis:** This gives you interactive tools and resources regarding the asset your investing in. This includes ... 
            - Real Estate Valuation Visualization (past 10 years)
            - Current Asset Photos According to Zillow 
            - Mortgate Repayments Calculator 
            - Real Investment Analysis similar to a Pro Forma that is used to project the financial aspect of buying and leasing a home 
    """)

    # # Sidebar with navigation options
    # st.sidebar.title("Navigation")
    # st.sidebar.write("Select a section to navigate:")
    # section = st.sidebar.radio("", ["Home", "Data Upload", "Data Visualization", "Data Analysis", "Contact"])

    # # Display different content based on the selected section
    # if section == "Home":
    #     st.write("You are on the Home page.")
    # elif section == "Data Upload":
    #     st.write("This is the Data Upload page.")
    # elif section == "Data Visualization":
    #     st.write("This is the Data Visualization page.")
    # elif section == "Data Analysis":
    #     st.write("This is the Data Analysis page.")
    # elif section == "Contact":
    #     st.write("This is the Contact page.")

if __name__ == "__main__":
    main()
