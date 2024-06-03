
import streamlit as st
import folium
from streamlit_folium import st_folium

def house_map():
    # Sample data: list of (latitude, longitude) tuples
                    #Latitude First, Longitude Second,
    coordinates = [(38.011734, -121.36025)]

    # Calculate the center of the map as the average of the coordinates
    map_center = [
        sum([coord[0] for coord in coordinates]) / len(coordinates),
        sum([coord[1] for coord in coordinates]) / len(coordinates)
    ]

    # Create a folium map centered around the calculated center
    mymap = folium.Map(location=map_center, zoom_start=10)

    # Add markers to the map
    for coord in coordinates:
        folium.Marker(location=coord, popup=f'Location: {coord}').add_to(mymap)
    return mymap


mymap = house_map()
    # Streamlit app layout
st.title("Zillow House Map in Streamlit")
st.write("This is an example of a Folium map embedded in a Streamlit app. This shows our property's location in the Stockton area.")

    # Display the map using streamlit_folium
st_folium(mymap, width=1000, height=600)
