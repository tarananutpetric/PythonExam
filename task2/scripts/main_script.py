import cdsapi

from EfasQuery import EfasQuery

def main():
    """
    ## MAIN PROGRAM ##

    Creates a query and submits it to the efas dataset.
    """

    query = EfasQuery(
        system_version="operational",
        originating_centre="ecmwf",
        product_type=["control_forecast"],
        variable=["river_discharge_in_the_last_24_hours"],
        model_levels="surface_level",
        year="2020",
        month="05",
        day="30",
        time="00:00",
        leadtime_hour=["24", "48"],
        download_format="zip",
    )

    print(query.generate_query())

    # dataset = "efas-forecast"
    # client = cdsapi.Client()
    # client.retrieve(dataset, query.generate_query()).download()

# -------------------------------
if __name__ == "__main__":
    main()