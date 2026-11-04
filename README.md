# proj_vulgo_UCA

Application Django avec PostgreSQL, lancée avec Docker Compose.

## Prérequis

- Docker avec la commande `docker compose`
- Git (pour récupérer le projet)

## Configuration

À la racine du projet, créez votre fichier local `.env` à partir du modèle :

```sh
cp .env.example .env
```

Ouvrez `.env` et remplacez les valeurs d’exemple, en particulier le mot de
passe de la base (`DB_PASSWORD`) et la clé Django (`SECRET_KEY`) par des
valeurs propres à votre environnement. Ne partagez pas ces valeurs et ne
commitez jamais le fichier `.env`.

Variables utilisées :

| Variable | Rôle |
| --- | --- |
| `DB_NAME` | Nom de la base PostgreSQL |
| `DB_USER` | Utilisateur PostgreSQL |
| `DB_PASSWORD` | Mot de passe PostgreSQL |
| `DB_HOST` | Hôte PostgreSQL ; conserver `db` avec Docker Compose |
| `DB_PORT` | Port PostgreSQL |
| `SECRET_KEY` | Clé secrète Django, à générer et garder privée |
| `DEBUG` | Active ou désactive le mode debug Django |
| `DJANGO_ALLOWED_HOSTS` | Liste des hôtes autorisés, séparés par des virgules |
| `DATABASE_URL` | URL également fournie par Compose ; Django lit les paramètres `DB_*` ci-dessus |

Les valeurs de `.env.example` sont destinées au développement et ne doivent
pas être réutilisées telles quelles pour un déploiement.

## Lancer l’application

Depuis la racine du dépôt, après avoir configuré `.env` :

```sh
docker compose up --build -d
docker compose exec web python manage.py migrate
```

Ouvrez ensuite [http://localhost:8000](http://localhost:8000). Pour suivre les
journaux :

```sh
docker compose logs -f web
```

Pour arrêter les conteneurs :

```sh
docker compose down
```

Les données PostgreSQL sont conservées dans le volume Docker `pgdata`. Pour
les supprimer également, utilisez `docker compose down --volumes` ; cette
commande efface les données de la base.
