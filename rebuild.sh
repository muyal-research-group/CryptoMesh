readonly IMAGE_NAME=${1:-cryptomesh:api}

export CRYPTOMESH_API_IMAGE=$IMAGE_NAME
echo "🚀 Building docker image: $IMAGE_NAME"
docker build -f ./Dockerfile -t $IMAGE_NAME .
echo "Shutting down existing cryptomesh service..."
docker compose -f docker-compose.yml down 
echo "Deploying CryptoMesh service..."
docker compose -f ./docker-compose.yml up -d