# BSO Smapshot

Implements a pipeline to retrieve [BSO](https://bso.swissartresearch.net) data from the [Smapshot](https://smapshot.heig-vd.ch/) platform.

## Usage

1. Copy the provided `.env.example` file
  1. `cp .env.example .env`
1. Run with `docker-compose up -d`

To execute the pipeline, run:
```
bash run.sh
```

To download the data from smapshot, run:
```
docker exec bso_smapshot python retrieve-smapshot-data.py
```
This will download the detailed data for all validated images in the SARI/BSO collection into the `/data` folder. The data is converted to XML for later mapping using the [X3ML Mapping Engine](https://github.com/isl/x3ml).
