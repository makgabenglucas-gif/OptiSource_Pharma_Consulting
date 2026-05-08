st.divider()

st.subheader("🪙 Green Rewards / Tokens")

st.write("Earn rewards for eco-friendly supply chain actions.")

green_actions = st.slider(
    "Number of Eco-Friendly Actions",
    0,
    100,
    10
)

tokens = green_actions * 5

st.metric("Green Tokens Earned", f"{tokens} Tokens")

if tokens >= 200:
    st.success("Excellent sustainability performance!")
elif tokens >= 100:
    st.info("Good sustainability contribution!")
else:
    st.warning("Increase eco-friendly actions to earn more rewards.")
