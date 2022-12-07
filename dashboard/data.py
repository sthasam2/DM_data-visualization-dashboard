import pandas as pd

#########################
# DATA
#########################

# data frame

df = pd.read_csv("../assets/cleaned.csv")
df.drop(df[df["tradeYear"] < 2010].index, inplace=True)


df["district"] = df["district"].replace(
    {
        1: "Dongcheng",
        2: "Fengtai",
        3: "Tongzhou",
        4: "Daxing",
        5: "Fangshan",
        6: "Changping",
        7: "Chaoyang",
        8: "Haidian",
        9: "Shijingshan",
        10: "Xicheng",
        11: "Pinggu",
        12: "Mentougou",
        13: "Shunyi",
    }
)
df["buildingStructure"] = df["buildingStructure"].replace(
    {
        1: "unknown",
        2: "mixed",
        3: "brick and wood",
        4: "brick and concrete",
        5: "steel",
        6: "steel-concrete composite",
    }
)
df["buildingType"] = df["buildingType"].replace(
    {
        1: "tower",
        2: "bungalow",
        3: "combination of plate and tower",
        4: "plate",
    }
)
df["renovationCondition"] = df["renovationCondition"].replace(
    {
        1: "other",
        2: "rough",
        3: "Simplicity",
        4: "hardcover",
    }
)
df["elevator"] = df["elevator"].replace(
    {
        1: "yes",
        0: "no",
    }
)

# Scaling

df["totalPrice"] = df["totalPrice"].apply(lambda x: x * 10000)

# Average price every year and month

average_price_df = (
    df.groupby(["tradeYear", "tradeMonth"])["totalPrice"].mean().reset_index()
)
average_price_df["tradeTime"] = [
    f"{x}-{y}" for x, y in zip(average_price_df.tradeYear, average_price_df.tradeMonth)
]

avg_district = df.groupby(["district"])["totalPrice"].mean()
building_str = df.groupby(["buildingStructure"])["totalPrice"].mean()
