docker build -t ocr-api -f Dockerfile .
docker-compose -f docker-compose.yaml pull
docker-compose -f docker-compose.yaml up