import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path




experiments = {
    "performance_static.csv": "Static Page",
    "performance_longtext.csv": "Long Text",
    "performance_longcolor.csv": "Long Color",
    "performance_dom_explosion.csv": "High DOM",
    "performance_color_mutation_storm.csv": "Color Mutation",
}




project_dir = Path(__file__).resolve().parent
data_dir = project_dir / "data"

frames = []

for filename, experiment_name in experiments.items():
    file_path = data_dir / filename

    if not file_path.exists():
        print(f"Warning: {filename} not found — skipping.")
        continue

    df = pd.read_csv(file_path)

    df["experiment"] = experiment_name

    df["dark_reader"] = df["dark_reader"].map({
        0: "Dark Reader OFF",
        1: "Dark Reader ON"
    })

    frames.append(df)


if not frames:
    raise FileNotFoundError("No experiment CSV files were found.")


data = pd.concat(frames, ignore_index=True)




summary = (
    data.groupby(["experiment", "dark_reader"], observed=True)[
        ["system_cpu_percent", "brave_cpu_percent"]
    ]
    .mean()
    .reset_index()
)

experiment_order = [
    "Static Page",
    "Long Text",
    "Long Color",
    "High DOM",
    "Color Mutation",
]

summary["experiment"] = pd.Categorical(
    summary["experiment"],
    categories=experiment_order,
    ordered=True,
)

summary = summary.sort_values("experiment")



fig, axes = plt.subplots(
    1,
    2,
    figsize=(15, 6)
)


# System CPU
for condition in summary["dark_reader"].dropna().unique():
    subset = summary[summary["dark_reader"] == condition]

    axes[0].plot(
        subset["experiment"],
        subset["system_cpu_percent"],
        marker="o",
        linewidth=2,
        label=condition
    )

axes[0].set_title("Average System CPU Usage")
axes[0].set_ylabel("CPU Usage (%)")
axes[0].set_xlabel("Webpage Type")
axes[0].tick_params(axis="x", rotation=25)
axes[0].grid(True, alpha=0.25)
axes[0].legend()


# Brave CPU
for condition in summary["dark_reader"].dropna().unique():
    subset = summary[summary["dark_reader"] == condition]

    axes[1].plot(
        subset["experiment"],
        subset["brave_cpu_percent"],
        marker="o",
        linewidth=2,
        label=condition
    )

axes[1].set_title("Average Brave CPU Usage")
axes[1].set_ylabel("CPU Usage (%)")
axes[1].set_xlabel("Webpage Type")
axes[1].tick_params(axis="x", rotation=25)
axes[1].grid(True, alpha=0.25)
axes[1].legend()


fig.suptitle(
    "Browser Performance Across Different Webpage Workloads",
    fontsize=16,
    fontweight="bold"
)

plt.tight_layout()

results_dir = project_dir / "results"
results_dir.mkdir(exist_ok=True)

output_path = results_dir / "resource_comparison.png"

fig.savefig(
    output_path,
    dpi=300,
    bbox_inches="tight"
)

print(f"\nPlot saved to: {output_path}")

plt.show()