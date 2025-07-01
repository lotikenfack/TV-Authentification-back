# TV-Authentification-back

## Configuration Initiale

### Étapes pour démarrer le projet

1. **Installer les dépendances** :
   ```bash
   pip install -r requirements.txt
   ```

2. **Appliquer les migrations** :
   ```bash
   python manage.py migrate
   ```

3. **Créer un superutilisateur** :
   ```bash
   python manage.py createsuperuser
   ```

4. **Démarrer le serveur de développement** :
   ```bash
   python manage.py runserver
   ```

5. **Démarrer le broker Redis** :
   Assurez-vous que Redis est installé et en cours d'exécution.
   ```bash
   redis-server
   ```

6. **Démarrer les workers Celery** :
   ```bash
   celery -A tv_auth worker --loglevel=info
   ```

### Tâches Périodiques

- `invalidate_expired_keys` : Invalide les clés expirées ou ayant dépassé le quota.
- `delete_scheduled_keys` : Supprime les clés planifiées pour suppression.

Ces tâches sont exécutées automatiquement si Celery est configuré correctement.