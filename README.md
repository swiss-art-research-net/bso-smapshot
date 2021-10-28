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

To execute individual steps of the pipeline, use the Task runner. 
Display a list of available tasks by running:

Note: Replace `bso_smapshot` with your container name if necessary
```
docker exec bso_smapshot task --list
```

The command will output the list of tasks:
```
task: Available tasks for this project:
* perform-mapping:      Map Smapshot XML data in the temporary folder to CIDOC/RDF
* prepare-mapping:      Compare the retrieved XML files with the mapped TTL files and copy all unconverted XML files to a temporary folder.
* retrieve-data:        Download the detailed data for all validated images in the SARI/BSO collection into the `/data` folder. The data is converted to XML for later mapping using the X3ML Mapping Engine.
```

Run a given task as follows:
```
docker exec bso_smapshot task <task name>
```
e.g.

```
docker exec bso_smapshot task retrieve0data
```