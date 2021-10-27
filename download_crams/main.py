#!/usr/bin/env python3

"""Copies HGDP CRAMs from EBI's FTP server."""

import csv
import gzip
import os
import subprocess
import click


@click.command()
@click.option('--shard_index', help='Sharding index', required=True, type=int)
@click.option('--shard_count', help='Total shard count', required=True, type=int)
def main(shard_index: int, shard_count: int) -> None:
    """Main entry point."""
    with gzip.open('hgdp_sample_metadata.tsv.gz', mode='rt') as metadata_file:
        reader = csv.DictReader(metadata_file, delimiter='\t')
        sample_index = 0
        for row in reader:
            url = row['url']
            if not url.endswith('.cram'):
                continue

            included = (sample_index % shard_count) == shard_index
            sample_index += 1
            if not included:
                continue

            path_components = url.split('/')
            path = '/'.join(path_components[3:])  # Remove the ftp://host/ prefix.
            filename = path_components[-1]

            home = os.getenv('HOME')
            output = f'{home}/data/cram/ebi/{filename}'

            print('Downloading {filename}')

            subprocess.run(
                [
                    f'{home}/.aspera/connect/bin/ascp',
                    '-i',
                    f'{home}/.aspera/connect/etc/asperaweb_id_dsa.openssh',
                    '-T',
                    '-l',
                    '300M',
                    '-P33001',
                    '-k1',
                    '-L-',
                    f'fasp-g1k@fasp.1000genomes.ebi.ac.uk:{path}',
                    f'{output}',
                ],
                check=True,
            )


if __name__ == '__main__':
    main()  # pylint: disable=no-value-for-parameter
