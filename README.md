# BSO Smapshot

Implements a pipeline to retrieve [BSO](https://bso.swissartresearch.net) data from the [Smapshot](https://smapshot.heig-vd.ch/) platform.

## Usage

1. Copy the provided `.env.example` file
  1. `cp .env.example .env`
1. Edit the `.env` file:
  1. `ENDPOINT`: SPARQL Graph store endpoint for data ingest
  1. `GRAPH`: Named graph used for ingesting data
  1. `USERNAME`: Username of endpoint with permissions to edit specified graph
  1. `PASSWORD`: Password of endpoint with permissions to edit specified graph
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

### Configure backend

The ingest step sends the data to a [RDF Graph Store](https://www.w3.org/TR/sparql11-http-rdf-update/) backend. The [Metaphacts](https://bitbucket.org/metaphacts/metaphacts-community/src/master/) and [ResearchSpace](http://researchspace.org) platforms both implement the API.

For security reasons, it's best to create a new user on the platform that has only access to the required operation and named graph. For MP and RS, create or edit the `shiro-roles.ini` and add a role with permissions for the named graph where the data will be pushed to. The name of the role can be chosen at will. 

For example, to create a role `push-smapshot` with permissions for the named graph `https://resource.swissartresearch.net/graph/smapshot` add:

```
[roles]
push-smapshot=sparql:graphstore:*:<https://resource.swissartresearch.net/graph/smapshot>
```

Then create a new user that has (only) the newly created role.