import cdsapi

from utils import CheckAllowedOptions


class EfasQuery:
    """Class to generate query dictionaries to the EFAS forecast dataset."""

    def __init__(
        self,
        system_version,
        originating_centre,
        product_type,
        variable,
        model_levels,
        year,
        month,
        day,
        time,
        leadtime_hour,
        soil_level=None,
        area=None,
        download_format="zip",
    ):
        """
        Initialize the query generator with the required parameters. Validates that parameters are within allowed options.

        :param system_version: list of str
        The EFAS system version that was used to generate the simulations.
        The current EFAS version 5.0 was released on 2023-09-20. For older versions and their release date, please see the Documentation.
        The recommendation is to always use the latest EFAS version for any application of the data.
        Older versions should only be used if you need to use it for a specific reason, for example validation of old forecasts.
        Available options: ["operational", "version_4_0"].

        :param originating_centre: str
        Originating centre denotes the meteorological centre that produced the forcing data.
        The model COSMO-LEPS is the Limited Area Ensemble Prediciton System developed within COSMO consortium.
        The ECMWF forecasts are the high resolution and ensemble forecasts from the European Centre for Medium-range Weather Forecasts.
        DWD are the forecasts of the Deutches Wetterdienst using the COSMO-EU model for the first three days, then the ICON model for day 4-7.
        Available options: ["ecmwf", "dwd", "cosmo_leps"].

        :param product_type: list of str
        The forecasts used in EFAS and GloFAS are high-resolution and ensemble forecasts.
        The ensemble forecasts consists of control member (unperturbed) and perturbed ensemble members.
        Available options: ["control_forecast", "ensemble_perturbed_forecasts", "high_resolution_forecast"]

        :param variable: list of str
        Note that the term 'last hours' in the discharge time step refers to the hours preceeding the end of each time step.
        For more information about the variables we refer to the Documentation.
        Available options: ["river_discharge_in_the_last_6_hours", "river_discharge_in_the_last_24_hours"].

        :param model_levels: str
        Soil moisture, soil depth, field capacity and wilting point are available at three levels in the soil.
        All other variables are avaiable at the surface level.
        Available options: ['surface_level', 'soil_levels']

        :param soil_level: list of str, optional
        Required if `model_levels` is 'soil_levels'.
        Levels 1, 2 and 3 are top, middle and bottom levels respectively.
        The depth of each soil level changes for each point. For a full explanation of the soil levels, please see the documentation.
        Available options:  ["1", "2", "3"]

        :param year: list of str
        Years to query.
        Available options ["2018", "2019", "2020", "2021", "2022", "2023", "2024"]

        :param month: list of str
        Months to query.
        Available options: ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

        :param day: list of str
        Available options: [
              "01",
              "02",
              "03",
              "04",
              "05",
              "06",
              "07",
              "08",
              "09",
              "10",
              "11",
              "12",
              "13",
              "14",
              "15",
              "16",
              "17",
              "18",
              "19",
              "20",
              "21",
              "22",
              "23",
              "24",
              "25",
              "26",
              "27",
              "28",
              "29",
              "30",
              "31"
            ]

        :param time: list of str
        Start hour of the forecast.
        Allowed options: ['00:00', '12:00']

        :param leadtime_hour: list of str
        Time step of the forecast in hours.
        Allowed options: [
              "0",
              "6",
              "12",
              "18",
              "24",
              "30",
              "36",
              "42",
              "48",
              "54",
              "60",
              "66",
              "72",
              "78",
              "84",
              "90",
              "96",
              "102",
              "108",
              "114",
              "120",
              "126",
              "132",
              "138",
              "144",
              "150",
              "156",
              "162",
              "168",
              "174",
              "180",
              "186",
              "192",
              "198",
              "204",
              "210",
              "216",
              "222",
              "228",
              "234",
              "240",
              "246",
              "252",
              "258",
              "264",
              "270",
              "276",
              "282",
              "288",
              "294",
              "300",
              "306",
              "312",
              "318",
              "324",
              "330",
              "336",
              "342",
              "348",
              "354",
              "360"
            ]

        :param area: list of float, optional
        If None, the entire available area will be provided.
        If provided, sub-region extraction is performed with geographic bounding box given as [North, West, South, East].
        Please note that the resolution of versions <strong>2.1</strong> and <strong>3.2</strong> is 0.1 degrees and version <strong>4.0</strong> the resolution is 0.05.
        The area selected may be adjusted slightly such that the returned file will fully encompass the selection made.

        :param download_format: str
        Available options: ['zip', 'unarchived']. Default is 'zip'.
        If you select 'Zip' the files will always be zipped into a single file.
        If you select 'Unarchived' then the files will be returned unarchived if there is only one file, and zipped if there are multiple files.


        """
        self.system_version = (
            system_version if isinstance(system_version, list) else [system_version]
        )
        self.originating_centre = originating_centre
        self.product_type = (
            product_type if isinstance(product_type, list) else [product_type]
        )
        self.variable = variable if isinstance(variable, list) else [variable]
        self.model_levels = model_levels
        self.soil_level = soil_level
        self.year = year if isinstance(year, list) else [year]
        self.month = month if isinstance(month, list) else [month]
        self.day = day if isinstance(day, list) else [day]
        self.time = time if isinstance(time, list) else [time]
        self.leadtime_hour = (
            leadtime_hour if isinstance(leadtime_hour, list) else [leadtime_hour]
        )
        self.area = area
        self.data_format = "netcdf"
        self.download_format = download_format

        self.validate_parameters()

    def validate_parameters(self):
        """
        Validates the input parameters based on dataset constraints.
        Raises ValueError if any parameter is invalid or the combination of parameters is not allowed.
        """
        # Validate system version
        CheckAllowedOptions(self.system_version, ["operational", "version_4_0"])
        if self.system_version == ["version_4_0"]:
            CheckAllowedOptions(self.variable, ["river_discharge_in_the_last_6_hours"])
            CheckAllowedOptions(self.year, ["2023"])
            CheckAllowedOptions(self.month, ["September"])
            CheckAllowedOptions(self.day, ["19"])
            CheckAllowedOptions(self.time, ["12:00"])

        # Validate originating_centre
        CheckAllowedOptions(self.originating_centre, ["ecmwf", "dwd", "cosmo_leps"])
        if self.originating_centre == "dwd":
            CheckAllowedOptions(self.product_type, ["high_resolution_forecast"])
            CheckAllowedOptions(self.variable, ["river_discharge_in_the_last_6_hours"])
            CheckAllowedOptions(
                self.leadtime_hour,
                [
                    "0",
                    "6",
                    "12",
                    "18",
                    "24",
                    "30",
                    "36",
                    "42",
                    "48",
                    "54",
                    "60",
                    "66",
                    "72",
                    "78",
                    "84",
                    "90",
                    "96",
                    "102",
                    "108",
                    "114",
                    "120",
                    "126",
                    "132",
                    "138",
                    "144",
                    "150",
                    "156",
                    "162",
                    "168",
                ],
            )
        if self.originating_centre == "cosmo_leps":
            CheckAllowedOptions(self.product_type, ["ensemble_perturbed_forecasts"])
            CheckAllowedOptions(self.variable, ["river_discharge_in_the_last_6_hours"])
            CheckAllowedOptions(
                self.leadtime_hour,
                [
                    "0",
                    "6",
                    "12",
                    "18",
                    "24",
                    "30",
                    "36",
                    "42",
                    "48",
                    "54",
                    "60",
                    "66",
                    "72",
                    "78",
                    "84",
                    "90",
                    "96",
                    "102",
                    "108",
                    "114",
                    "120",
                    "126",
                    "132",
                ],
            )

        # Validate product_type
        CheckAllowedOptions(
            self.product_type,
            [
                "control_forecast",
                "ensemble_perturbed_forecasts",
                "high_resolution_forecast",
            ],
        )
        if self.product_type == ["high_resolution_forecast"]:
            CheckAllowedOptions(self.variable, ["river_discharge_in_the_last_6_hours"])
            CheckAllowedOptions(
                self.leadtime_hour,
                [
                    "0",
                    "6",
                    "12",
                    "18",
                    "24",
                    "30",
                    "36",
                    "42",
                    "48",
                    "54",
                    "60",
                    "66",
                    "72",
                    "78",
                    "84",
                    "90",
                    "96",
                    "102",
                    "108",
                    "114",
                    "120",
                    "126",
                    "132",
                    "138",
                    "144",
                    "150",
                    "156",
                    "162",
                    "168",
                    "174",
                    "180",
                    "186",
                    "192",
                    "198",
                    "204",
                    "210",
                    "216",
                    "222",
                    "228",
                    "234",
                    "240",
                ],
            )

        # Validate variable
        CheckAllowedOptions(
            self.variable,
            [
                "river_discharge_in_the_last_6_hours",
                "river_discharge_in_the_last_24_hours",
            ],
        )
        if self.variable == ["river_discharge_in_the_last_6_hours"]:
            CheckAllowedOptions(self.model_levels, ["surface_level"])
        if self.variable == ["river_discharge_in_the_last_24_hours"]:
            CheckAllowedOptions(self.model_levels, ["surface_level"])
            CheckAllowedOptions(self.year, ["2018", "2019", "2020"])
            CheckAllowedOptions(
                self.leadtime_hour,
                [
                    "24",
                    "48",
                    "64",
                    "72",
                    "96",
                    "120",
                    "144",
                    "168",
                    "192",
                    "216",
                    "240",
                    "264",
                    "288",
                    "312",
                    "336",
                    "360",
                ],
            )

        # Validate model levels and soil level
        CheckAllowedOptions(self.model_levels, ["surface_level", "soil_levels"])
        if self.model_levels == "soil_levels" and not self.soil_level:
            raise ValueError(
                "Soil_level is required when model_levels is 'soil_levels'."
            )
        if self.soil_level:
            if self.model_levels == "surface_level":
                raise ValueError(
                    "Soil_level should not be provided when model_levels is 'surface_level'."
                )
            CheckAllowedOptions(self.soil_level, ["1", "2", "3"])

        # Validate year
        CheckAllowedOptions(
            self.year, ["2018", "2019", "2020", "2021", "2022", "2023", "2024"]
        )
        if self.year == ["2018"]:
            CheckAllowedOptions(self.month, ["October", "November", "December"])
        if self.year == ["2023"]:
            CheckAllowedOptions(
                self.month,
                [
                    "January",
                    "February",
                    "March",
                    "April",
                    "May",
                    "June",
                    "July",
                    "August",
                    "September",
                ],
            )
        if self.year == ["2024"]:
            CheckAllowedOptions(
                self.month, ["May", "June", "July", "August", "September", "October"]
            )
            # assume the system can handle cases where multiple year/month combinations are given

        # validate month
        CheckAllowedOptions(
            self.month,
            [
                "01",
                "02",
                "03",
                "04",
                "05",
                "06",
                "07",
                "08",
                "09",
                "10",
                "11",
                "12",
            ],
        )

        # validate day
        allowed_days = [
            "01",
            "02",
            "03",
            "04",
            "05",
            "06",
            "07",
            "08",
            "09",
            "10",
            "11",
            "12",
            "13",
            "14",
            "15",
            "16",
            "17",
            "18",
            "19",
            "20",
            "21",
            "22",
            "23",
            "24",
            "25",
            "26",
            "27",
            "28",
            "29",
            "30",
            "31",
        ]
        CheckAllowedOptions(self.day, allowed_days)
        # assume the system can handle itself which are the possible days in month

        # Validate time
        CheckAllowedOptions(self.time, ["00:00", "12:00"])

        # Validate leadtime_hour
        CheckAllowedOptions(
            self.leadtime_hour,
            [
                "0",
                "6",
                "12",
                "18",
                "24",
                "30",
                "36",
                "42",
                "48",
                "54",
                "60",
                "66",
                "72",
                "78",
                "84",
                "90",
                "96",
                "102",
                "108",
                "114",
                "120",
                "126",
                "132",
                "138",
                "144",
                "150",
                "156",
                "162",
                "168",
                "174",
                "180",
                "186",
                "192",
                "198",
                "204",
                "210",
                "216",
                "222",
                "228",
                "234",
                "240",
                "246",
                "252",
                "258",
                "264",
                "270",
                "276",
                "282",
                "288",
                "294",
                "300",
                "306",
                "312",
                "318",
                "324",
                "330",
                "336",
                "342",
                "348",
                "354",
                "360",
            ],
        )

        # Validate area
        if self.area:
            if (
                not isinstance(self.area, list)
                or len(self.area) != 4
                or not all(isinstance(coord, (int, float)) for coord in self.area)
            ):
                raise ValueError(
                    "Area must be a list of four numerical values [North, West, South, East]."
                )

        # Validate download_format
        CheckAllowedOptions(self.download_format, ["unarchived", "zip"])

    def generateQuery(self):
        """
        Generate a query dictionary based on the initialized parameters.
        """
        query = {
            "system_version": self.system_version,
            "originating_centre": self.originating_centre,
            "product_type": self.product_type,
            "variable": self.variable,
            "model_levels": self.model_levels,
            "year": self.year,
            "month": self.month,
            "day": self.day,
            "time": self.time,
            "leadtime_hour": self.leadtime_hour,
            "download_format": self.download_format,
        }

        if self.soil_level:
            query["soil_level"] = self.soil_level

        if self.area:
            query["area"] = self.area

        if self.download_format:
            query["download_format"] = self.download_format

        return query

    def downloadFile(self, output):
        """
        Submits the query and saves the file.

        :param output: output file location
        """
        dataset = (
            "efas-forecast"  # fixed according to instructions; can be made a variable
        )
        client = cdsapi.Client()
        client.retrieve(dataset, self.generateQuery(), output)
