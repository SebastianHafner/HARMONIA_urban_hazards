import geopandas as gpd
from pathlib import Path
from utils import parsers


def urban_land_deformation_processing(root_folder: str, pilot: str, insar_name: str, clipped: bool) -> None:
    root_folder = Path(root_folder)
    assert root_folder.exists()

    # Load the InSAR points data
    file_name = f'{pilot}_{insar_name}_clipped.shp' if clipped else f'{pilot}_{insar_name}.shp'
    points_file = root_folder / 'land_deformation' / 'raw' / pilot / 'vector' / file_name
    points = gpd.read_file(points_file)

    # Load the building block polygons (exposure component)
    polygons_file = root_folder / 'exposure' / 'Pilot_Cities_BB' / pilot / f'{pilot}_Building Blocks_4326.shp'
    polygons = gpd.read_file(polygons_file)

    # Add unique index for building blocks
    polygons['bb_id'] = polygons.index

    # Add point count to building blocks (i.e., number of points contained by each building block)
    polygons = polygons.join(gpd.sjoin(points, polygons).groupby("bb_id").size().rename("n_points"), how="left")
    polygons['n_points'] = polygons['n_points'].fillna(0).astype('int64')

    # Perform a spatial join to get points within building_blocks
    points_bb = gpd.sjoin(points, polygons, how="inner", op="within")
    out_file = root_folder / 'land_deformation' / 'preprocessed' / pilot / f'{pilot}_{insar_name}_BB_subset.shp'
    # points_bb.to_file(out_file)

    # Points are grouped by their corresponding building blocks
    grouped = points_bb[['velocity', 'bb_id']].groupby(['bb_id'])
    # Compute mean velocity (mean_v) and absolute maximum velocity (max_v) among the points located within a
    # specific building block
    agg_values = grouped.agg([('mean_v', 'mean'), ('max_v', lambda x: max(x, key=abs))])

    # Add the aggregated values per building block to the respective building block polygon
    polygons = polygons.join(agg_values['velocity'], on='bb_id', how='left')
    polygons = polygons.drop('bb_id', axis='columns')

    # Save the building block layer enriched with velocity information at the building block level
    out_file = root_folder / 'land_deformation' / 'preprocessed' / pilot / f'{pilot}_{insar_name}_BB.shp'
    polygons.to_file(out_file)


if __name__ == '__main__':
    args = parsers.argument_parser_land_deformation().parse_known_args()[0]
    urban_land_deformation_processing(args.root_folder, args.pilot, args.s1_product, parsers.str2bool(args.clipped))