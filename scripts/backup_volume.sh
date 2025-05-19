#!/bin/bash
set -x

docker run --rm -v sys-lic_superset_data:/var/lib/postgresql/data/ alpine tar -czv --to-stdout -C /var/lib/postgresql/data/ . > backup_superset_data.tgz
docker run --rm -v sys-lic_postgres_data:/var/lib/postgresql/data/ alpine tar -czv --to-stdout -C /var/lib/postgresql/data/ . > backup_postgres_data.tgz
docker run --rm -v sys-lic_syslic_data:/opt/data alpine tar -czv --to-stdout -C /opt/data . > backup_backend_data.tgz
