# streamlit_app.py

import streamlit as st
import requests
import matplotlib.pyplot as plt

# ---- 1. User Inputs ----
st.title("♟️ Chess Dashboard")
username = st.text_input("Enter your Chess.com username", value="thunnu5")
time_class = st.selectbox("Select time control", ["blitz", "bullet", "rapid", "daily"])

if st.button("Generate Report"):
    # ---- 2. Fetch and Filter Games ----
    headers = {"User-Agent": "Chess Dashboard"}
    archives_url = f"https://api.chess.com/pub/player/{username}/games/archives"
    try:
        archive_list = requests.get(archives_url, headers=headers).json().get("archives", [])
        all_games = []
        for url in archive_list:
            games = requests.get(url, headers=headers).json().get("games", [])
            filtered = [g for g in games if g.get("time_class") == time_class]
            all_games.extend(filtered)

        if not all_games:
            st.warning("No games found for that time control.")
        else:
            # ---- 3. Pie Chart: Win/Loss/Draw ----
            wins, draws, losses = 0, 0, 0
            ratings = []
            for g in all_games:
                color = 'white' if g['white']['username'].lower() == username.lower() else 'black'
                result = g.get(color, {}).get("result")
                rating = g.get(color, {}).get("rating")
                if result == "win": wins += 1
                elif result == "draw": draws += 1
                elif result: losses += 1
                if rating: ratings.append(rating)

            fig1, ax1 = plt.subplots()
            ax1.pie([wins, losses, draws], labels=['Wins', 'Losses', 'Draws'], autopct='%1.1f%%')
            ax1.set_title("Win Breakdown")
            st.pyplot(fig1)

            # ---- 4. Line Chart: Rating Over Time ----
            fig2, ax2 = plt.subplots()
            ax2.plot(ratings, marker='o')
            ax2.set_title("Rating Progression")
            ax2.set_xlabel("Game #")
            ax2.set_ylabel("Rating")
            st.pyplot(fig2)

    except Exception as e:
        st.error(f"Something went wrong: {e}")
