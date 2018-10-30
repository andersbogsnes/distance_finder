from distances import Distances
import pandas as pd
import argparse
import pathlib


def get_from_adresser(input_path):
    output_file = pathlib.Path('./data/cleaned_from_address.xlsx')

    if output_file.exists():
        return pd.read_excel(output_file)

    from_address_df = pd.read_excel(input_path)
    from_address_df['address_field'] = from_address_df.Adresse.str.cat(from_address_df.Postnr,
                                                                       sep=', ')
    from_address_clean = (from_address_df.rename(columns={'Region': 'assurandoer_region'})
                              .loc[:, ['navn', 'stilling', 'assurandoer_region', 'address_field']])

    output_file.parent.mkdir(exist_ok=True)
    from_address_clean.to_excel(output_file)

    return from_address_clean


def get_to_addresser(input_path):
    output_file = pathlib.Path('./data/cleaned_to_address.xlsx')
    if output_file.exists():
        return pd.read_excel(output_file)

    to_address_df = pd.read_excel(input_path)
    to_address_clean = to_address_df.rename(columns={'Adresse': 'address_field',
                                                     'Navn': 'kontor_navn',
                                                     'Region': 'kontor_region',
                                                     'Forretningsben': 'kontor_forretningsben'})
    output_file.parent.mkdir(exist_ok=True)
    to_address_clean.to_excel(output_file)

    return to_address_clean


def calculate_min_distance(merged_df, column='distance', threshold: int = None):
    idx = merged_df[merged_df.assurandoer_region == merged_df.kontor_region].groupby('navn')[
        column].idxmin().values

    min_df = merged_df.iloc[idx]
    if threshold:
        return min_df[min_df[column] <= threshold]
    else:
        return min_df


def merge_dfs(from_addresses, to_addresses, distances_df):
    return (distances_df
            .merge(from_addresses,
                   left_on='from_address',
                   right_on='address_field').drop('address_field', axis=1)
            .merge(to_addresses,
                   left_on='to_address',
                   right_on='address_field')).drop('address_field', axis=1)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('from_file',
                        help='Input file of from_addresses')

    parser.add_argument('to_file',
                        help='Input file of to_addresses')

    parser.add_argument('--from_colname',
                        help='Name of input column',
                        default='address_field')

    parser.add_argument('--to_colname',
                        help='Name of input column',
                        default='address_field')

    parser.add_argument('--db_name',
                        default='sqlite:///distances.db',
                        help='connection string for db')
    parser.add_argument('--metric', default='distance',
                        help='Which metric to use',
                        choices=['distance', 'duration'])
    parser.add_argument('--threshold', default=50000,
                        help='Threshold for metric')

    args = parser.parse_args()

    run(args.from_file,
        args.to_file,
        args.from_colname,
        args.to_colname,
        args.db_name,
        args.metric,
        args.threshold)


def run(from_file,
        to_file,
        from_colname,
        to_colname,
        db_name,
        metric,
        threshold):
    client = Distances(db_name)

    from_df = get_from_adresser(from_file)
    to_df = get_to_addresser(to_file)

    client.import_data_from_df(from_df, from_column=from_colname)
    client.import_data_from_df(to_df, to_column=to_colname)
    output_df = client.output_distances()

    merged_data = merge_dfs(from_df, to_df, output_df)
    min_distance = calculate_min_distance(merged_data, column=metric, threshold=threshold)

    min_distance.to_excel(f'results_max_{metric}_{threshold}.xlsx')


if __name__ == '__main__':
    main()
