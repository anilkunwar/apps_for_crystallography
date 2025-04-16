import streamlit as st

st.title("Import Debug")

try:
    import quaternion
    st.success("✅ Successfully imported `quaternion`")
except Exception as e:
    st.error("❌ Failed to import `quaternion`")
    st.exception(e)

st.write("Trying to import `orix`...")

try:
    from orix import plot, sampling
    st.success("✅ Successfully imported `orix.plot` and `sampling`")
except Exception as e:
    st.error("❌ Failed to import from `orix`")
    st.exception(e)
