from django.db import models
from django.contrib.sessions.models import Session

class Comment(models.Model):
    text = models.TextField(blank=True, null=True) 
    # 👇 Nouveaux champs
    created_at = models.DateTimeField(auto_now_add=True, help_text="Date de création")
    modified_at = models.DateTimeField(auto_now=True, help_text="Date de dernière modification")

    def __str__(self):
        if self.text:
            return f"Commentaire #{self.id} - {self.text[:30]}..."
        return f"Commentaire #{self.id} (sans texte)"

class Visitor(models.Model):
    user_anonymos = models.CharField(max_length=255, help_text="Pseudo du visiteur",unique=True)
    
    session = models.ForeignKey(
        Session, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name="visiteurs"
    )
    
    note = models.IntegerField(help_text="Note sur 5", null=False) 
    
    comment = models.ForeignKey(
        Comment, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name="visiteurs"
    )
    
    # 👇 Nouveaux champs
    created_at = models.DateTimeField(auto_now_add=True, help_text="Date de création")
    modified_at = models.DateTimeField(auto_now=True, help_text="Date de dernière modification")

    def __str__(self):
        return f"{self.user_anonymos} - Note: {self.note}/5"

class Vote(models.Model):
    VOTE_CHOICES = [
        ('agree', "D'accord"),
        ('not_agree', "Pas d'accord"),
    ]
    
    # Si le commentaire est supprimé (ex: modification du texte), les votes sont supprimés
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="votes")
    # On lie le vote à la session de l'utilisateur
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name="votes")
    vote_type = models.CharField(max_length=10, choices=VOTE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # 👇 CONTRAINTE CRUCIALE : 1 session ne peut avoir qu'un seul vote par commentaire
        constraints = [
            models.UniqueConstraint(fields=['comment', 'session'], name='unique_vote_per_session')
        ]

    def __str__(self):
        return f"{self.session.session_key[:8]}... a voté '{self.vote_type}' sur #{self.comment.id}"

