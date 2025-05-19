#!/bin/bash
set -x

PATH_BACKUP=$1

if [[ ! -e "$PATH_BACKUP/backup_superset_data.tgz" ]]; then
  echo "Fail to restore backup, cannot find file $PATH_BACKUP/backup_superset_data.tgz"
  exit 1
fi

if [[ ! -e "$PATH_BACKUP/backup_postgres_data.tgz" ]]; then
  echo "Fail to restore backup, cannot find file $PATH_BACKUP/backup_postgres_data.tgz"
  exit 1
fi

if [[ ! -e "$PATH_BACKUP/backup_backend_data.tgz" ]]; then
  echo "Fail to restore backup, cannot find file $PATH_BACKUP/backup_backend_data.tgz"
  exit 1
fi

cat $PATH_BACKUP/backup_superset_data.tgz | docker run --rm -i -v syslic_superset_data:/var/lib/postgresql/data/ alpine tar xzf - -C /var/lib/postgresql/data/
cat $PATH_BACKUP/backup_postgres_data.tgz | docker run --rm -i -v syslic_postgres_data:/var/lib/postgresql/data/ alpine tar xzf - -C /var/lib/postgresql/data/
cat $PATH_BACKUP/backup_backend_data.tgz | docker run --rm -i -v syslic_syslic_data:/opt/data alpine tar xzf - -C /opt/data

