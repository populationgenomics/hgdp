# Download HGDP CRAMs from the EBI FTP server

The FTP server access [requires the Aspera software](https://www.internationalgenome.org/category/ftp/). Unfortunately, within a Docker container, the downloads stall after a few hundred MB. For some reason this doesn't happen when running `ascp` directly in a VM.

1. Bring up a few (e.g. N=5) `n1-standard-1` VMs.
1. On each VM, run `setup.sh` to install Aspera and set up `gcsfuse`.
1. On each VM, run `main.py <index> <N>`, with `<index>` in [0, N-1] incrementing for each VM to parallelize the work through sharding.
