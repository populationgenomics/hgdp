# Download HGDP CRAMs from the EBI FTP server

The FTP server access [requires the Aspera software](https://www.internationalgenome.org/category/ftp/). Unfortunately, within a Docker container, the downloads stall after a few hundred MB. For some reason this doesn't happen when running `ascp` directly in a VM.

First, bring up a few (e.g. N=5) `n1-standard-1` VMs. Use a `standard` service account with access to the HGDP `main` bucket.

Then, on each VM:

1. `sudo apt update && sudo apt install -y git screen`
1. Open a `screen` session.
1. `git clone https://github.com/populationgenomics/hgdp.git && cd hgdp/download_crams`
1. Run `setup.sh` to install Aspera and set up `gcsfuse`.
1. Run `main.py --shard_index=<index> --shard_count=<N>`, with `<index>` in [0, N-1] incrementing for each VM to parallelize the work through sharding.
