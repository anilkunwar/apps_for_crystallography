import os
os.environ["STREAMLIT_DEPRECATION_SHOW_PYPLOT_GLOBAL_USE"] = "False"
import streamlit as st
st.set_option('deprecation.showPyplotGlobalUse', False)
#import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

from orix import plot, sampling
from orix.crystal_map import Phase
from orix.quaternion import Orientation, symmetry
from orix.vector import Vector3d

# We'll want our plots to look a bit larger than the default size
new_params = {
    "figure.facecolor": "w",
    "figure.figsize": (20, 7),
    "lines.markersize": 10,
    "font.size": 15,
    "axes.grid": True,
}
plt.rcParams.update(new_params)

# Create a Streamlit app title
st.title("Inverse Pole Figures constructed using orix software")

# Explanation dictionary based on symmetry selection
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

# Dropdown for symmetry selection
#selected_symmetry = st.selectbox("Select a symmetry:", list(explanations.keys()))
selected_symmetry = st.sidebar.selectbox("Select a symmetry:", list(explanations.keys()))

# Display the explanation for the selected symmetry
st.markdown(f"**Explanation for {selected_symmetry} symmetry:**")
st.write(explanations[selected_symmetry])


# Display the plot using st.pyplot()
#st.pyplot(plot.IPFColorKeyTSL(getattr(symmetry, selected_symmetry)).plot())
fig = plot.IPFColorKeyTSL(getattr(symmetry, selected_symmetry)).plot()
st.pyplot(fig)


# Slider widgets for Euler angles
st.sidebar.title("Adjust Euler Angles")
euler_x = st.sidebar.slider("Euler X or $\phi 1$ (degrees)", min_value=0, max_value=360, value=0)
euler_y = st.sidebar.slider("Euler or $\phi $ Y (degrees)", min_value=0, max_value=360, value=0)
euler_z = st.sidebar.slider("Euler Z or $\phi 2$ (degrees)", min_value=0, max_value=360, value=0)

# Additional content
direction = Vector3d(((1, 0, 0), (0, 1, 0), (0, 0, 1)))  # X, Y, Z
kwargs = dict(projection="ipf", direction=direction)

# Generate ORIX plot using selected symmetry and adjusted Euler angles
st.markdown(f"IPF for {selected_symmetry} Symmetry with selected Euler Angles")
pg = getattr(symmetry, selected_symmetry)
ori = Orientation.from_euler([euler_x, euler_y, euler_z], pg, degrees=True)
#ori.scatter(**kwargs)
#plt.title(f"ORIX Plot for {selected_symmetry} Symmetry")
#st.pyplot(plt.gcf())  # Display the generated ORIX plot
fig, ax = plt.subplots()
ori.scatter(**kwargs, ax=ax)
st.pyplot(fig)  # Display the generated ORIX plot


#
# Slider for controlling the number of points
st.markdown(f"IPF for for {selected_symmetry} Symmetry with Random Points")
num_points = st.slider("Number of Points:", min_value=1, max_value=100000, value=100, step=10)
# Generate ORIX plot using selected symmetry
#pg = getattr(symmetry, selected_symmetry)
#ori = Orientation.random(100000)
ori = Orientation.random(num_points )
ori.symmetry = pg
rgb_z = plot.IPFColorKeyTSL(pg).orientation2color(ori)
#ori.scatter("ipf", c=rgb_z, direction=direction)
#plt.title(f"ORIX Plot for {selected_symmetry} Symmetry")
#st.pyplot(plt.gcf())  # Display the generated ORIX plot
fig, ax = plt.subplots()
ori.scatter("ipf", c=rgb_z, direction=direction, ax=ax)
st.pyplot(fig)  # Display the generated ORIX plot
#ori.scatter("ipf", c=rgb_z, direction=direction)





