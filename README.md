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

### Tâches Planifiées (Adaptation pour O2switch)

1. **Exécution via un cron job** :
   Configurez un cron job sur o2switch pour exécuter la commande de gestion Django périodiquement.
   Exemple de configuration :
   ```bash
   */5 * * * * /path/to/virtualenv/bin/python /path/to/project/manage.py run_scheduled_tasks
   ```

2. **Exécution via une vue HTTP** :
   Utilisez l'endpoint `/api/run_maintenance/` pour déclencher les tâches planifiées à la demande.
   Exemple de requête :
   ```bash
   curl -X GET http://your-domain/api/run_maintenance/
   ```
   Assurez-vous que cet endpoint est sécurisé (par exemple, via une clé secrète ou une liste blanche d'IP).