# Initialize the= database
db:
	@echo "Seeding database..."
	@export $(shell cat .env | xargs) && python seed_database.py

# Run the app
run:
	docker-compose up --build

# Stop
down:
	docker-compose down
