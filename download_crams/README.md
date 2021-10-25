# Download HGDP CRAMs from the EBI FTP server

The FTP server access [requires the Aspera software](https://www.internationalgenome.org/category/ftp/), which is why this script uses the `ibmcom/aspera-cli` Docker image.

```sh
analysis-runner --dataset hgdp --access-level test --output-dir cram/ebi --description "Copy HGDP CRAMs from EBI FTP" main.py
```
