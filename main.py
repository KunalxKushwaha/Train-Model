import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import time

# ---------------------------
# Config
# ---------------------------
tracks = [1, 2, 3]  # Track numbers
track_length = 30   # simulation distance
train_length = 3    # number of coaches (excluding engine)

# Example train setup
trains = [
    {"id": "T1", "position": 0, "track": 1, "priority": "High", "hold": False, "color": "royalblue"},
    {"id": "T2", "position": 6, "track": 2, "priority": "Medium", "hold": False, "color": "seagreen"},
    {"id": "T3", "position": 12, "track": 3, "priority": "Low", "hold": False, "color": "firebrick"},
]

# ---------------------------
# Helper: draw trains with realistic engine + coaches
# ---------------------------
def plot_trains(trains, t):
    fig, ax = plt.subplots(figsize=(14, 6))

    # Draw tracks
    for track in tracks:
        # ballast background
        ax.fill_between([0, track_length], track - 0.3, track + 0.3, color="#d9d9d9", alpha=0.6)
        # rails
        ax.hlines(y=track - 0.1, xmin=0, xmax=track_length, color="black", linewidth=3)
        ax.hlines(y=track + 0.1, xmin=0, xmax=track_length, color="black", linewidth=3)
        # sleepers
        for x in range(0, track_length + 1, 2):
            ax.add_patch(patches.Rectangle((x - 0.1, track - 0.3), 0.2, 0.6, color="saddlebrown"))

    # Draw trains
    for train in trains:
        start = train["position"]
        y = train["track"]

        # Engine (distinct look)
        engine = patches.Rectangle((start, y - 0.18), 1.5, 0.36,
                                   linewidth=1.5, edgecolor="black",
                                   facecolor=train["color"], zorder=3)
        ax.add_patch(engine)
        # Engine window
        ax.add_patch(patches.Rectangle((start + 0.2, y - 0.08), 0.4, 0.16,
                                       facecolor="skyblue", edgecolor="black", linewidth=0.5))

        # Label on engine
        ax.text(start + 0.75, y, train["id"], color="white",
                ha="center", va="center", fontsize=9, weight="bold")

        # Coaches
        for i in range(1, train_length + 1):
            coach_x = start + 1.5 + (i - 1) * 1.4
            coach = patches.FancyBboxPatch(
                (coach_x, y - 0.15), 1.2, 0.3,
                boxstyle="round,pad=0.05,rounding_size=0.1",
                linewidth=1, edgecolor="black",
                facecolor=train["color"], alpha=0.85, zorder=2
            )
            ax.add_patch(coach)
            # Windows for coach
            for w in range(3):
                ax.add_patch(patches.Rectangle((coach_x + 0.2 + w * 0.3, y - 0.06),
                                               0.25, 0.12, facecolor="white",
                                               edgecolor="black", linewidth=0.4))

    ax.set_xlim(0, track_length)
    ax.set_ylim(0.5, len(tracks) + 0.7)
    ax.set_yticks(tracks)
    ax.set_xlabel("Distance (time units)", fontsize=12)
    ax.set_ylabel("Track", fontsize=12)
    ax.set_title(f"🚆 Professional Train Simulation at Time {t}", fontsize=16, weight="bold")
    ax.grid(False)
    st.pyplot(fig)

# ---------------------------
# Streamlit App
# ---------------------------
def main():
    st.title("🚆 Professional Train Movement Simulator")
    st.write("Each train runs on a separate track. You can hold/release trains using the sidebar.")

    # Sidebar controls
    for train in trains:
        train["hold"] = st.sidebar.checkbox(f"Hold {train['id']}?", value=False)

    # Simulation speed
    speed = st.sidebar.slider("Simulation speed (sec per step)", 0.1, 1.0, 0.3)

    # Start button
    start_btn = st.button("▶ Start Simulation")
    if start_btn:
        placeholder = st.empty()
        for t in range(track_length):
            # Update train positions
            for train in trains:
                if not train["hold"]:
                    train["position"] += 1
                    if train["position"] > track_length:
                        train["position"] = 0  # loop back

            # Draw
            with placeholder.container():
                plot_trains(trains, t)
                time.sleep(speed)

if __name__ == "__main__":
    main()
