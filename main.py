import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import time

# ---------------------------
# Config
# ---------------------------
tracks = [1, 2, 3]      # Track numbers
track_length = 40       # simulation distance
train_length = 4        # number of coaches (excluding engine)
station_start = 15      # station position (x start)
station_length = 8      # station width

# Example train setup
trains = [
    {"id": "T1", "position": 0, "track": 1, "priority": "High", "hold": False, "color": "royalblue"},
    {"id": "T2", "position": 6, "track": 2, "priority": "Medium", "hold": False, "color": "seagreen"},
    {"id": "T3", "position": 12, "track": 3, "priority": "Low", "hold": False, "color": "firebrick"},
]

# ---------------------------
# Helper: draw trains + station
# ---------------------------
def plot_trains(trains, t):
    fig, ax = plt.subplots(figsize=(14, 6))

    # Draw tracks + sleepers
    for track in tracks:
        ax.fill_between([0, track_length], track - 0.3, track + 0.3, color="#d9d9d9", alpha=0.6)
        ax.hlines(y=track - 0.1, xmin=0, xmax=track_length, color="black", linewidth=3)
        ax.hlines(y=track + 0.1, xmin=0, xmax=track_length, color="black", linewidth=3)
        for x in range(0, track_length + 1, 2):
            ax.add_patch(patches.Rectangle((x - 0.1, track - 0.3), 0.2, 0.6, color="saddlebrown"))

        # Draw individual platform for this track
        ax.add_patch(patches.Rectangle((station_start, track + 0.25), station_length, 0.25,
                                       facecolor="#e0e0e0", edgecolor="black", alpha=0.9))
        # Platform roof/shelter
        ax.add_patch(patches.Rectangle((station_start, track + 0.5), station_length, 0.15,
                                       facecolor="#999999", edgecolor="black", alpha=0.8))
        # Station signboard
        ax.text(station_start + station_length/2, track + 0.7, f"Station-{track}",
                ha="center", va="bottom", fontsize=10, weight="bold", color="darkblue")

    # Draw trains
    for train in trains:
        start = train["position"]
        y = train["track"]

        # Engine
        engine = patches.Rectangle((start, y - 0.18), 1.5, 0.36,
                                   linewidth=1.5, edgecolor="black",
                                   facecolor=train["color"], zorder=3)
        ax.add_patch(engine)
        ax.add_patch(patches.Rectangle((start + 0.2, y - 0.08), 0.4, 0.16,
                                       facecolor="skyblue", edgecolor="black", linewidth=0.5))
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
            for w in range(3):
                ax.add_patch(patches.Rectangle((coach_x + 0.2 + w * 0.3, y - 0.06),
                                               0.25, 0.12, facecolor="white",
                                               edgecolor="black", linewidth=0.4))

    ax.set_xlim(0, track_length)
    ax.set_ylim(0.5, len(tracks) + 1.2)
    ax.set_yticks(tracks)
    ax.set_xlabel("Distance (time units)", fontsize=12)
    ax.set_ylabel("Track", fontsize=12)
    ax.set_title(f"🚉 Train Simulation at Time {t}", fontsize=16, weight="bold")
    ax.grid(False)
    st.pyplot(fig)

# ---------------------------
# Streamlit App
# ---------------------------
def main():
    st.title("🚆 Train Simulation with Realistic Stations")
    st.write("Each track now has its own station platform where trains slow down while passing.")

    for train in trains:
        train["hold"] = st.sidebar.checkbox(f"Hold {train['id']}?", value=False)

    speed = st.sidebar.slider("Simulation speed (sec per step)", 0.1, 1.0, 0.3)

    start_btn = st.button("▶ Start Simulation")
    if start_btn:
        placeholder = st.empty()
        for t in range(track_length * 2):
            for train in trains:
                if not train["hold"]:
                    # Slow down at station zone
                    if station_start - 2 <= train["position"] <= station_start + station_length:
                        train["position"] += 0.3
                    else:
                        train["position"] += 1

                    if train["position"] > track_length:
                        train["position"] = 0

            with placeholder.container():
                plot_trains(trains, t)
                time.sleep(speed)

if __name__ == "__main__":
    main()
