import pandas as pd
import numpy as np


data = 'data/pdh_data.parquet'


df = pd.read_parquet(data)

# Uniquement la France
df_fr = df[df.country == 'France']

# Uniquement les enregistrements associés à des mesures
df_fr = df_fr[df_fr.category=='Known']

# Métropolitaine
lat_min, lat_max = 41.0, 51.2
lon_min, lon_max = -5.1, 9.6 
df_fr = df_fr[(df_fr['lat'] >= lat_min) & (df_fr['lat'] <= lat_max) & 
               (df_fr['lon'] >= lon_min) & (df_fr['lon'] <= lon_max)]

# Uniquement les eaux de surface, souterraines et potables
df_fr_surf_ground_drink = df_fr[df_fr['matrix'].isin(['Surface water', 'Groundwater', 'Drinking water'])]

# Année 2023
df_fr_surf_ground_drink = df_fr_surf_ground_drink[df_fr_surf_ground_drink['year']==2023]

# Uniquement les colonnes utiles au traitement
df_fr_surf_ground_drink = df_fr_surf_ground_drink[['lat','lon','pfas_sum']]

# # Calculer le 99ème percentile
# percentile_99 = np.percentile(df_fr_surf_ground_drink.pfas_sum.values, 99)

# # Afficher le résultat
# print(f"Le 99ème percentile des concentrations de PFAS est : {percentile_99}")

# # On fixe les valeurs extrêmement élevées au 99ème percentile pour la lisibilité
# df_fr_surf_ground_drink['pfas_sum'] = np.clip(df_fr_surf_ground_drink['pfas_sum'], None, percentile_99)

# Longueur initiale du DataFrame
initial_length = len(df_fr_surf_ground_drink)

# Trier le DataFrame par latitude, longitude et pfas_sum (par ordre décroissant)
df_fr_surf_ground_drink = df_fr_surf_ground_drink.sort_values(by=['lat', 'lon', 'pfas_sum'], ascending=[True, True, False])

# Supprimer les doublons basés sur lat et lon, en gardant uniquement la première occurrence (valeur de pfas_sum la plus élevée)
df_fr_surf_ground_drink = df_fr_surf_ground_drink.drop_duplicates(subset=['lat', 'lon'], keep='first')

# Longueur après suppression des doublons
final_length = len(df_fr_surf_ground_drink)

# Calculer et afficher le nombre de doublons supprimés
duplicates_removed = initial_length - final_length
print(f"Nombre de doublons supprimés : {duplicates_removed}")

df_fr_surf_ground_drink.to_parquet("pfas_2023_surf_ground_drink.parquet")