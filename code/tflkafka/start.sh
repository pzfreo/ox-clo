docker-machine rm --force tfl
docker-machine create --driver digitalocean --digitalocean-region=lon1  --digitalocean-size=2gb --digitalocean-access-token=$DIGOCTOK  --digitalocean-image ubuntu-18-04-x64 tfl
doctl compute floating-ip-action assign 46.101.65.164 $(doctl compute droplet list tfl -t $DIGOCTOK --format ID --no-header) -t $DIGOCTOK 
eval $(docker-machine env tfl)
docker-compose up --build -d


