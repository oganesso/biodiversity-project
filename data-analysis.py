import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# import data
species_info = pd.read_csv("species_info.csv")
observations = pd.read_csv("observations.csv")

# calculate summary stats
#   species info
unique_organism_categories = species_info.category.unique()
num_unique_organism_categories = species_info.category.nunique()
unique_conservation_status_categories = species_info.conservation_status.unique()
# num_of_no_concern_species = (species_info[species_info.conservation_status == np.nan]).count()
other_num_of_species = (species_info["conservation_status"]).count()
#   observations
unique_park_names = observations.park_name.unique()
median_observations = observations.observations.median()
mean_observations = observations.observations.mean()
observations_std_dev = observations.observations.std()
observations_first_quartile = observations.observations.quantile(.25)
observations_third_quartile = observations.observations.quantile(.75)
observation_duplciates = observations[observations.duplicated() == True]


# return summary stats
#   species info
print("\nunique_organism_categories:", unique_organism_categories)
print("num_unique_organism_categories:", num_unique_organism_categories)
print("unique_conservation_status_categories:", unique_conservation_status_categories)
# print("num_of_no_concern_species", num_of_no_concern_species)
print("other_num_of_species", other_num_of_species)
#   observations
print("unique_park_names", unique_park_names)
print("median_observations", median_observations)
print("mean_observations", mean_observations)
print("observations_std_dev", observations_std_dev)
print("observations_first_quartile", observations_first_quartile)
print("observations_third_quartile", observations_third_quartile)

# visual examination
sns.set_theme(rc={"figure.figsize":(15, 8)})
fig, axes = plt.subplots(1, 2)
#   What is the distribution of conservation_status for animals?
sns.countplot(data=species_info, x="conservation_status", ax=axes[0])
axes[0].set_ylabel("num of species")
axes[0].set_title("spread of conservation status (\"species of concern\" == \"at risk\")")
#   Are certain types of species more likely to be endangered?
sns.countplot(data=species_info, x="category", hue="conservation_status", ax=axes[1])
axes[1].set_xticklabels(unique_organism_categories, rotation=10)
axes[1].set_xlabel("class")
axes[1].set_ylabel("num of species")
axes[1].set_title("spread of conservation status, sorted by class")
plt.suptitle("conservation status proportions")
plt.show()
plt.clf()
#   Which species were spotted the most at each park?
observations.drop_duplicates(inplace=True, subset=["scientific_name"])
observations_sorted_by_park = observations.pivot(columns="park_name", index="scientific_name", values="observations")
print(observations["park_name"].value_counts())
for column in observations_sorted_by_park.columns:
    observations_sorted_by_park.sort_values(by=[column], ascending=False, inplace=True)
    print("\n\n" + "Most sighted species in", column + ":\n"), print(observations_sorted_by_park.head())
