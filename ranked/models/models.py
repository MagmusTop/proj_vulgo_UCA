from django.db import models

class Rank(models.Model):
    # Dans le diagramme, le champ s'appelle 'rank', mais 'score' ou 'note' est plus lisible en Python
    rank = models.IntegerField(help_text="Note sur 5")
    commentaire = models.TextField()
    nb_agree = models.IntegerField(default=0, help_text="Nombre de personnes d'accord")
    nb_not_agree = models.IntegerField(default=0, help_text="Nombre de personnes en désaccord")

    def __str__(self):
        return f"Note: {self.rank}/5 - {self.commentaire[:30]}..."

class Visitor(models.Model):
    # Correspond à la table 'user' dans ton diagramme
    user_anonymos = models.CharField(max_length=255, help_text="Identifiant ou pseudo du visiteur")
    # Relation vers Rank. J'utilise ForeignKey au cas où un visiteur laisserait plusieurs avis
    rank = models.ForeignKey(Rank, on_delete=models.CASCADE, related_name="visiteurs")

    def __str__(self):
        return f"{self.user_anonymos} -> {self.rank}"