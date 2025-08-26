# Build the docker image
build:
	docker-compose build

# Run the app
run:
	docker-compose up --build


# Stop
down:
	docker-compose down

