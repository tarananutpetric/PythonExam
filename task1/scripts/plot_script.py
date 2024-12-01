import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from utils import colourON, colourOFF


def monthlyOperations(data, output):
    """
    Top: Creates a histogram of operation hours of turbine per month.
    Bottom: Creates a plot of average prices at various settings (turbine off/on/total).
    """
    fig, axs = plt.subplots(2, 1, figsize=(12, 10), sharex=True)
    x_positions = np.arange(len(data["Month"]))

    # Top plot: Stacked histogram of Hours ON and OFF
    width = 0.6  # Bar width
    axs[0].bar(
        x_positions,
        data["Hours ON"],
        label="Hours ON",
        color=colourON,
        width=width,
        bottom=data["Hours OFF"],
    )
    axs[0].bar(
        x_positions, data["Hours OFF"], label="Hours OFF", color=colourOFF, width=width
    )
    axs[0].set_ylabel("Hours")
    axs[0].set_title("Operation hours")
    axs[0].legend()
    axs[0].grid(True, linestyle="--", alpha=0.6)

    # Bottom plot: Average price ON and OFF
    axs[1].plot(
        data["Month"],
        data["Average price ON"],
        label="Average Price Turbine ON",
        marker="o",
        linestyle="-",
        color=colourON,
    )
    axs[1].plot(
        data["Month"],
        data["Average price OFF"],
        label="Average Price Turbine OFF",
        marker="o",
        linestyle="-",
        color=colourOFF,
    )
    axs[1].plot(
        data["Month"],
        data["Average price"],
        label="Average Price",
        marker="o",
        linestyle="-",
        color="orange",
    )
    axs[1].set_ylabel("EUR/MWh")
    axs[1].set_title("Average price")
    axs[1].set_xticks(x_positions)
    axs[1].set_xticklabels(data["Month"], rotation=45, fontsize=10)
    axs[1].legend()
    axs[1].grid(True, linestyle="--", alpha=0.6)

    # Adjust layout and save the plot
    plt.tight_layout()
    plt.savefig(output, dpi=300, bbox_inches="tight")
    print(f"Created {output} plot.")


def monthlyRevenue(data, output):
    """
    Top: Creates a plot of total revenue per month.
    Bottom: Creates a plot of average hourly revenue per month.
    """
    fig, axs = plt.subplots(2, 1, figsize=(12, 10), sharex=True)

    # Top plot: Total revenue
    x_positions = np.arange(len(data["Month"]))

    axs[0].plot(data["Month"], data["Total revenue [EUR]"], marker="o", linestyle="-")
    axs[0].set_ylabel("EUR")
    axs[0].set_title("Total revenue")
    axs[0].grid(True, linestyle="--", alpha=0.6)

    # Bottom plot: Average price ON and OFF
    axs[1].plot(
        data["Month"], data["Average revenue [EUR/h]"], marker="o", linestyle="-"
    )
    axs[1].set_ylabel("EUR/h")
    axs[1].set_title("Average hourly revenue")
    axs[1].set_xticks(x_positions)
    axs[1].set_xticklabels(data["Month"], rotation=45, fontsize=10)
    axs[1].grid(True, linestyle="--", alpha=0.6)

    # Adjust layout and save the plot
    plt.tight_layout()
    plt.savefig(output, dpi=300, bbox_inches="tight")
    print(f"Created {output} plot.")


def operations(data, output):
    """
    Creates plots with hourly spaced datapoints.
    Top: 	flow rate on turbine with colour-marked ON and OFF regimes.
            Scaled curve of electricity price [EUR/MWh] is overlaid as cross-check.
    Middle: Electricity price [EUR/MWh], colour-coded for regimes of turbine operations.
    Bottom: Lake volume over time. Scaled curve of monthly inflows is overlaid fto improve understanding.
    """
    # Scale and shift the Price data to match the range of Flow Rate (q)
    price_min, price_max = data["Price"].min(), data["Price"].max()
    q_min, q_max = data["q"].min(), data["q"].max()
    scaled_price = (data["Price"] - price_min) / (price_max - price_min) * (
        q_max - q_min
    ) + q_min

    # Scale and shift the Inflow data to match the range of Volume (v)
    inflow_min, inflow_max = data["Inflow"].min(), data["Inflow"].max()
    v_min, v_max = data["v"].min(), data["v"].max()
    scaled_inflow = (data["Inflow"] - inflow_min) / (inflow_max - inflow_min) * (
        v_max - v_min
    ) + v_min

    # Create a figure with three vertically stacked subplots
    fig, axs = plt.subplots(3, 1, figsize=(12, 12), sharex=True)

    # Plot Flow Rate  on the first subplot with area filled and scaled price overlay
    axs[0].plot(data["DateTime"], data["q"], color=colourON, linewidth=1)

    # Fill the area below the curve
    axs[0].fill_between(
        data["DateTime"], 0, data["q"], color=colourON, alpha=1.0, label="Turbine ON"
    )

    # Fill the area above the curve (from the curve to q_max)
    axs[0].fill_between(
        data["DateTime"],
        data["q"],
        q_max,
        color=colourOFF,
        alpha=1.0,
        label="Turbine OFF",
    )

    # Overlay the scaled price
    axs[0].plot(
        data["DateTime"],
        scaled_price,
        label="Scaled Price",
        color="saddlebrown",
        linewidth=1,
        linestyle="--",
    )

    # Add labels and title
    axs[0].set_ylabel("Flow rate [m3/s]", fontsize=12)
    axs[0].set_title("Flow rate on turbine with scaled price overlay", fontsize=14)
    axs[0].grid(True, linestyle="--", alpha=0.6)
    axs[0].legend()

    # Plot color-coded Price on the second subplot
    colors = np.where(
        data["q"] == 50, colourON, np.where(data["q"] == 0, colourOFF, "orange")
    )
    axs[1].scatter(data["DateTime"], data["Price"], c=colors, label="Price", s=10)
    axs[1].set_ylabel("Price [EUR/MWh]", fontsize=12)
    axs[1].set_title("Price at turbine operations", fontsize=14)
    axs[1].grid(True, linestyle="--", alpha=0.6)
    axs[1].legend(
        handles=[
            plt.Line2D(
                [0],
                [0],
                marker="o",
                color="w",
                label="Turbine ON MAX",
                markerfacecolor=colourON,
                markersize=10,
            ),
            plt.Line2D(
                [0],
                [0],
                marker="o",
                color="w",
                label="Turbine ON MID",
                markerfacecolor="orange",
                markersize=10,
            ),
            plt.Line2D(
                [0],
                [0],
                marker="o",
                color="w",
                label="Turbine OFF",
                markerfacecolor=colourOFF,
                markersize=10,
            ),
        ]
    )

    # Plot Volume on the third subplot with scaled Inflow overlay
    axs[2].plot(
        data["DateTime"], data["v"], label="Lake volume", color="green", linewidth=1
    )
    axs[2].plot(
        data["DateTime"],
        scaled_inflow,
        label="Scaled Inflow",
        color="purple",
        linewidth=1,
        linestyle="--",
    )
    axs[2].set_ylabel("Volume [m3]", fontsize=12)
    axs[2].set_title("Lake volume with scaled inflow overlay", fontsize=14)
    axs[2].grid(True, linestyle="--", alpha=0.6)
    axs[2].legend()

    # Set x-axis ticks to show only 13 evenly spaced labels for the shared x-axis
    total_ticks = 13
    tick_positions = np.linspace(0, len(data) - 1, total_ticks, dtype=int)
    tick_labels = data["DateTime"].iloc[tick_positions]

    # Format tick labels as strings
    formatted_labels = tick_labels.dt.strftime("%Y-%m-%d %H:%M:%S")
    axs[2].set_xticks(data["DateTime"].iloc[tick_positions])
    axs[2].set_xticklabels(formatted_labels, rotation=45, fontsize=10)

    # Set x-axis label for the shared axis
    axs[2].set_xlabel("DateTime", fontsize=12)

    # Adjust layout and save the plot
    plt.tight_layout()
    plt.savefig(output, dpi=300, bbox_inches="tight")
    print(f"Created {output} plot.")


def main():
    """
    ## MAIN PROGRAM ##

    Creates various plots of operations and revenue.
    """
    data = pd.read_csv("output/out.csv")
    data["DateTime"] = pd.to_datetime(data["DateTime"])
    monthly = pd.read_csv("output/monthly.csv")

    # Map Month column to actual month names for x-tick labels
    month_names = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ]
    monthly["Month"] = monthly["Month"].map(dict(enumerate(month_names, start=1)))

    #Create plots
    monthlyOperations(monthly, "output/monthlyOperations.png")
    monthlyRevenue(monthly, "output/monthlyRevenue.png")
    operations(data, "output/operations.png")


# -------------------------------
if __name__ == "__main__":
    main()
