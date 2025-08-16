from netCDF4 import Dataset
import numpy as np
import pandas as pd


def query_obj(obj):
    return [attr for attr in dir(obj) if not callable(getattr(obj, attr)) and not attr.startswith("__")]


def query_data(data, meta_exclude=None):
    text = ""
    if data.data:
        data = data.data
    for var in data:
        if meta_exclude is None or meta_exclude not in var:
            text += f"{var}, "
    print(text.rstrip(","))


def query_dataset(dataset, meta_exclude=None):
    if dataset.groups:
        for grp in dataset.groups:
            print(grp)
            text = "    "
            if dataset.groups[grp].groups:
                for nestgrp in dataset.groups[grp].groups:
                    print(text + nestgrp)
                    text2 = "    "
                    for var in dataset.groups[grp].groups[nestgrp].variables:
                        text2 += f"{var}, "
                    print(text + text2.rstrip(","))
            else:
                for var in dataset.groups[grp].variables:
                    if meta_exclude is None or meta_exclude not in var:
                        text += f"{var}, "
                print(text.rstrip(","))
    else:
        text = ""
        for var in dataset.variables:
            text += f"{var}, "
        print(text.rstrip(","))


def to_dataframe(obsDF):
    obsDF = obsDF
    if obsDF.data:
        obsDF = obsDF.data
    return pd.DataFrame(obsDF)
    

def fit_rate(data, dz=1000):
    df = to_dataframe(data)

    # 1. Filter valid data (both 'oman' and 'ombg' are not NaN)
    valid_df = df[df["oman"].notna() & df["ombg"].notna()].copy()
    valid_df = valid_df.dropna(subset=["height"])  # removes any rows in valid_df where height is missing (NaN)

    # 2. Compute overall RMS and fit_rate
    bias_a = valid_df["oman"].mean()
    bias_b = valid_df["ombg"].mean()
    rms_a = np.sqrt((valid_df["oman"]**2).mean())
    rms_b = np.sqrt((valid_df["ombg"]**2).mean())
    fit_rate_overall = (rms_b - rms_a) / rms_b
    print(f"OMA: bias={bias_a:.4f} rms={rms_a:.4f}")
    print(f"OMB: bias={bias_b:.4f} rms={rms_b:.4f}")
    print(f"Overall fit_rate: {fit_rate_overall:.4%}")

    # 3. Bin data by height every dz meters
    valid_df["height_bin"] = (valid_df["height"] // dz) * dz  # floor to nearest 1000

    # 4. Group by height_bin and compute RMS and fit_rate
    grouped = valid_df.groupby("height_bin").agg({
        "oman": lambda x: np.sqrt(np.mean(x**2)),
        "ombg": lambda x: np.sqrt(np.mean(x**2))
    }).rename(columns={"oman": "rms_a", "ombg": "rms_b"})

    grouped["fit_rate"] = (grouped["rms_b"] - grouped["rms_a"]) / grouped["rms_b"]
    grouped = grouped.reset_index()  # reset the groupby column "height" from index to normal columns
    for idx, row in grouped.iterrows():
        print(f"{idx}, {row['height_bin']:.0f}, {row['rms_a']:.4f}, {row['rms_b']:.4f}, {row['fit_rate']:.4%}")

    return grouped  # data frame
    

class _ObsDF:  # DataFrame-like obs structure
    def __init__(self, data):
        self.data = data

    def __getitem__(self, key):
        return self.data[key]

    def __getattr__(self, name):
        try:
            return self.__getitem__(name)
        except KeyError as e:
            raise AttributeError(f"No variable '{name}_{self.varname}' found.") from e


class obsSpace:
    def __init__(self, filepath):
        """
        Initialize an obsSpace object and load the NetCDF file.

        Parameters:
        - filepath (str): Path to the NetCDF file.
        """
        self.filepath = filepath
        self.dataset = Dataset(filepath, mode='r')

        # Read the dimension
        self.nlocs = len(self.dataset.dimensions['Location'])

        # Read the Location variable
        self.locations = self.dataset.variables['Location'][:]

        # Discover group names
        self.groups = list(self.dataset.groups.keys())

        #
        self._get_metadata()

        # Remove groups, provide direct access to varaibles, such as obsSpace.t, obsSpace.q, obsSpace.u, obsSpace.v, etc
        for var in ["airTemperature", "windEastward", "windNorthward", "specificHumidity", "brightnessTemperature"]:
            self._get_data_by_varname(var)

    def get_valid_subset(data, item, condition={"EffectiveQC2": 0}):
        data2 = np.array(data[item])
        key, value = next(iter(condition.items()))
        return data2[data[key] == value]

    def _get_metadata(self):
        # this is used for get metadata only
        dataset = self.dataset
        metadata = {}
        for var in dataset.groups['MetaData'].variables:
            metadata[var] = dataset.groups['MetaData'].variables[var][:]
        self.metadata = metadata

    def _get_data_by_varname(self, varname):
        dataset = self.dataset
        # This will get both metadata and regular data
        data = {}
        only_has_metadata = True
        for grp in dataset.groups:
            if dataset.groups[grp].groups:
                for nestgrp in dataset.groups[grp].groups:  # DiagnosticFlags
                    if varname in dataset.groups[grp].groups[nestgrp].variables:
                        data[nestgrp] = dataset.groups[grp].groups[nestgrp].variables[varname][:]
                        only_has_metadata = False
            else:
                if grp == "MetaData":
                    for var in dataset.groups['MetaData'].variables:
                        if var != "longitude_latitude_pressure":
                            data[var] = dataset.groups['MetaData'].variables[var][:]
                elif grp == "ObsError" and varname == "specificHumidity":
                    data["ObsError"] = dataset.groups["ObsError"].variables["relativeHumidity"][:]
                    only_has_metadata = False
                elif varname == "brightnessTemperature" and (grp == "ObsValue" or grp == "ObsValueAdj") and "brightnessTemperature" in dataset.groups[grp].variables:
                    data[grp] = dataset.groups[grp].variables["radiance"][:]
                    only_has_metadata = False
                elif varname in dataset.groups[grp].variables:
                    data[grp] = dataset.groups[grp].variables[varname][:]
                    only_has_metadata = False

        # assign the data dict
        if only_has_metadata:
            data = {}
        if varname == "airTemperature":
            self.t = _ObsDF(data)
        elif varname == "windEastward":
            self.u = _ObsDF(data)
        elif varname == "windNorthward":
            self.v = _ObsDF(data)
        elif varname == "specificHumidity":
            self.q = _ObsDF(data)
        elif varname == "brightnessTemperature":
            self.bt = _ObsDF(data)

    def __getitem__(self, key):
        # Enable obsSpace["t"]
        if key in ["t", "airTemperature"]:
            return self.t
        elif key in ["u", "windEastward"]:
            return self.u
        elif key in ["v", "windNorthward"]:
            return self.u
        elif key in ["q", "specificHumidity"]:
            return self.q
        elif key in ["bt", "brightnessTemperature"]:
            return self.bt
        raise KeyError(f"Key '{key}' not found.")

    def __getattr__(self, name):
        # Enable obsSpace.t
        try:
            return self.__getitem__(name)
        except KeyError:
            raise AttributeError(f"'obsSpace' object has no attribute or variable '{name}'")
