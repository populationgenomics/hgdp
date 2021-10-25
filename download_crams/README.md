# Download HGDP CRAMs from the EBI FTP server

The FTP server access [requires the Aspera software](https://www.internationalgenome.org/category/ftp/). Unfortunately, the `ibmcom/aspera-cli` Docker image isn't compatible with Hail Batch's file localization paths.

````sh
gcloud builds submit --tag=australia-southeast1-docker.pkg.dev/cpg-common/images/aspera:v1 .
```

```sh
analysis-runner --dataset hgdp --access-level test --output-dir cram/ebi --description "Copy HGDP CRAMs from EBI FTP" main.py
````
