# Nom de ton image Docker
IMAGE_NAME = zephyr
CONTAINER_NAME = zephyr
PORT = 8097

# Build de l'image Docker
build:
	docker build -t $(IMAGE_NAME) .

# Lancer le conteneur avec le port 8097 exposé
run: build
	docker run -d -p $(PORT):8097 --name $(CONTAINER_NAME) $(IMAGE_NAME)

# Arrêter le conteneur
stop:
	docker stop $(CONTAINER_NAME)

# Supprimer le conteneur
rm: stop
	docker rm $(CONTAINER_NAME)

# Supprimer l'image
rmi: rm
	docker rmi -f $(IMAGE_NAME)

# Supprimer l'image et le conteneur
clean: rm rmi

# Afficher l'état du conteneur
status:
	docker ps -a | grep $(CONTAINER_NAME)

# Commande pour afficher les logs du conteneur
logs:
	docker logs $(CONTAINER_NAME)

API_URL=http://localhost:8097/api/metrics

# Commande pour récupérer la liste des métriques
list_metrics:
	@echo "Récupération des métriques..."
	@curl -s ${API_URL}