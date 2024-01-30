import matplotlib.pyplot as plt
import streamlit as st

# Create a figure and an axis
fig1, ax = plt.subplots(figsize=(12, 8))

# Add a line to the axis
ax.plot([1, 2, 3], [4, 5, 6])

# Show the figure
st.pyplot(fig1)
