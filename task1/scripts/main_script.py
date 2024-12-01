import os
import pandas as pd

from Lake import Lake
from utils import flowOptimisation


def main():
    """
    ## MAIN PROGRAM ##

    Models and optimises a hydroelectic setup to maximise revenue.
    """

    # import prices and inflow data and join into one dataframe
    data = pd.read_csv(
        "data/Spot_2023.csv",
        delimiter=";",
        names=["DateTime", "Price"],
        header=0,
        parse_dates=["DateTime"],
    )
    inflow_monthly = pd.read_csv(
        "data/reservoirs_monthly_mean_inflows.csv", delimiter=";"
    )
    data["Month"] = data["DateTime"].dt.month
    month_to_inflow = inflow_monthly.set_index("Mois")["Apports [m3/s]"].to_dict()
    data["Inflow"] = data["Month"].map(month_to_inflow)

    # initialise lake
    LakeAlpiq = Lake(
        e=0.003, Vmin=0, Vmax=400e6, Qmin=0, Qmax=50, coeff=0.6
    )  # convert e units to MWh

    # perform desired optimisation
    model = flowOptimisation(LakeAlpiq, data)

    # save to the dataframe optimised variables and objective
    data["q"] = [model.q[i]() for i in model.N]
    data["v"] = [model.v[i]() for i in model.N]
    data["Revenue [EUR/h]"] = model.e * data["q"] * data["Price"] * 3600

    # calculate some monthly quantities (average price, operation hours, ...)
    monthlyAverages = (
        data.groupby("Month")
        .apply(
            lambda group: pd.Series(
                {
                    "Average price ON": group["Price"][group["q"] > 0].mean(),
                    "Average price OFF": group["Price"][group["q"] == 0].mean(),
                    "Average price": group["Price"].mean(),
                    "Hours ON": (group["q"] > 0).sum(),
                    "Hours OFF": (group["q"] == 0).sum(),
                    "Average revenue [EUR/h]": group["Revenue [EUR/h]"].mean(),
                    "Total revenue [EUR]": group["Revenue [EUR/h]"].sum(),
                }
            )
        )
        .reset_index()
    )

    # save data
    os.makedirs("output/", exist_ok=True)
    data.to_csv("output/out.csv")
    monthlyAverages.to_csv("output/monthly.csv")
    print("Produced output files output/out.csv and output/monthly.csv .")


# -------------------------------
if __name__ == "__main__":
    main()
