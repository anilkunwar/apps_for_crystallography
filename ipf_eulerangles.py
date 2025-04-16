import streamlit as st
# Suppress deprecation warning for global use of Matplotlib's pyplot
st.set_option('deprecation.showPyplotGlobalUse', False)
import matplotlib.pyplot as plt
import numpy as np
from orix import plot, sampling
from orix.crystal_map import Phase
from orix.quaternion import Orientation, symmetry
from orix.vector import Vector3d

# Configure Matplotlib plot settings for better visualization
new_params = {
    "figure.facecolor": "w",  # Set figure background to white
    "figure.figsize": (20, 7),  # Set figure size for larger plots
    "lines.markersize": 10,  # Set marker size for scatter plots
    "font.size": 15,  # Set font size for text elements
    "axes.grid": True,  # Enable grid on axes
}
plt.rcParams.update(new_params)

# Set the title of the Streamlit app
st.title("Inverse Pole Figures constructed using orix software")

# Dictionary containing explanations for each symmetry type
explanations = {
    "Ci": "Cyclic symmetry (Cn) has an n-fold rotation axis.",
    "C2h": "C2h symmetry is Cn with the addition of a mirror (reflection) plane perpendicular to the axis of rotation (horizontal plane).",
    "D2h": "D2h symmetry has an n-fold rotation axis plus n twofold axes perpendicular to that axis.",
    "S6": "S6 symmetry contains only a 2n-fold rotation-reflection axis (S2n).",
    "D3d": "D3d symmetry includes diagonal mirror planes and is related to D3h symmetry.",
    "C4h": "C4h symmetry is a cyclic group with horizontal and vertical mirror planes.",
    "D4h": "D4h symmetry has an n-fold rotation axis plus n twofold axes perpendicular to that axis and diagonal mirror planes.",
    "C6h": "C6h symmetry is a cyclic group with horizontal and vertical mirror planes.",
    "D6h": "D6h symmetry includes diagonal mirror planes and is related to D6 symmetry.",
    "Th": "Th symmetry includes three horizontal mirror planes and an inversion center (i).",
    "Oh": "Oh symmetry includes horizontal and vertical mirror planes, an inversion center, and improper rotation operations.",
}

# Create a sidebar dropdown for selecting symmetry
selected_symmetry = st.sidebar.selectbox("Select a symmetry:", list(explanations.keys()))

# Display the explanation for the selected symmetry
st.markdown(f"**Explanation for {selected_symmetry} symmetry:**")
st.write(explanations[selected_symmetry])

# Display the IPF color key plot for the selected symmetry
st.pyplot(plot.IPFColorKeyTSL(getattr(symmetry, selected_symmetry)).plot())

# Sidebar sliders for adjusting Euler angles
st.sidebar.title("Adjust Euler Angles")
euler_x = st.sidebar.slider("Euler X or $\phi 1$ (degrees)", min_value=0, max_value=360, value=0)
euler_y = st.sidebar.slider("Euler or $\phi $ Y (degrees)", min_value=0, max_value=360, value=0)
euler_z = st.sidebar.slider("Euler Z or $\phi 2$ (degrees)", min_value=0, max_value=360, value=0)

# Define crystal directions for IPF projection
direction = Vector3d(((1, 0, 0), (0, 1, 0), (0, 0, 1)))  # X, Y, Z directions
kwargs = dict(projection="ipf", direction=direction)  # IPF plot parameters

# Generate and display IPF plot with selected Euler angles
st.markdown(f"IPF for {selected_symmetry} Symmetry with selected Euler Angles")
pg = getattr(symmetry, selected_symmetry)  # Get symmetry object
ori = Orientation.from_euler([euler_x, euler_y, euler_z], pg, degrees=True)  # Create orientation from Euler angles
ori.scatter(**kwargs)  # Plot the orientation
st.pyplot(plt.gcf())  # Display the plot

# Slider for controlling the number of random points
st.markdown(f"IPF for {selected_symmetry} Symmetry with Random Points")
num_points = st.slider("Number of Points:", min_value=1, max_value=100000, value=100, step=10)

# Generate and display IPF plot with random orientations
ori = Orientation.random(num_points)  # Generate random orientations
ori.symmetry = pg  # Assign selected symmetry
rgb_z = plot.IPFColorKeyTSL(pg).orientation2color(ori)  # Compute colors for orientations
ori.scatter("ipf", c=rgb_z, direction=direction)  # Plot the random orientations
st.pyplot(plt.gcf())  # Display the plot
