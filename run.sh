if [[ $ENV_FILE ]]
then
  source $ENV_FILE
else
  source .env
fi

docker exec $PROJECT_NAME task run