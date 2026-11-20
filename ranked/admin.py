# admin.py
from datetime import timedelta

from django.contrib import admin
from django.contrib.admin import AdminSite
from django.db.models import Avg, Count
from django.db.models.functions import TruncDate
from django.utils import timezone

from .models.models import Comment, Visitor, Vote


class DashboardAdminSite(AdminSite):
    site_header = "IUT — Zone Commentaires"
    site_title  = "Dashboard"
    index_title = "Tableau de bord"

    def index(self, request, extra_context=None):
        extra_context = extra_context or {}
        today = timezone.now().date()
        start = today - timedelta(days=6)

        # ---- KPI ----
        total_visitors = Visitor.objects.count()
        total_comments = Comment.objects.count()
        total_votes    = Vote.objects.count()
        avg_note       = Visitor.objects.aggregate(avg=Avg("note"))["avg"] or 0

        # ---- Visiteurs sur 7 jours ----
        raw = (
            Visitor.objects
            .filter(created_at__date__gte=start)
            .annotate(day=TruncDate("created_at"))
            .values("day").annotate(count=Count("id")).order_by("day")
        )
        by_day = {start + timedelta(days=i): 0 for i in range(7)}
        for row in raw:
            by_day[row["day"]] = row["count"]

        chart_labels   = [(start + timedelta(days=i)).strftime("%d/%m") for i in range(7)]
        chart_visitors = [by_day[start + timedelta(days=i)] for i in range(7)]

        # ---- Distribution des notes (1 → 5) ----
        note_raw = (
            Visitor.objects.values("note")
            .annotate(count=Count("id")).order_by("note")
        )
        note_by_value = {i: 0 for i in range(1, 6)}
        for row in note_raw:
            note_by_value[row["note"]] = row["count"]

        # ---- Votes ----
        vote_raw = Vote.objects.values("vote_type").annotate(count=Count("id"))
        vote_by_type = {"agree": 0, "not_agree": 0}
        for row in vote_raw:
            vote_by_type[row["vote_type"]] = row["count"]

        # ---- Derniers commentaires ----
        latest_comments = Comment.objects.order_by("-created_at")[:5]

        extra_context.update({
            "total_visitors":  total_visitors,
            "total_comments":  total_comments,
            "total_votes":     total_votes,
            "avg_note":        round(avg_note, 2),
            "chart_labels":    chart_labels,
            "chart_visitors":  chart_visitors,
            "note_labels":     [f"{i} ⭐" for i in range(1, 6)],
            "note_values":     [note_by_value[i] for i in range(1, 6)],
            "vote_labels":     ["D'accord", "Pas d'accord"],
            "vote_values":     [vote_by_type["agree"], vote_by_type["not_agree"]],
            "latest_comments": latest_comments,
        })
        return super().index(request, extra_context)
    
    def get_app_list(self, request, app_label=None):
        app_list = super().get_app_list(request, app_label)
        # ajoute un lien en haut
        app_list.insert(0, {
            "name": "Tableau de bord",
            "app_label": "dashboard",
            "models": [{
                "name": "Statistiques",
                "object_name": "Stats",
                "admin_url": "/admin/",
                "view_only": True,
            }],
        })
        return app_list


dashboard_site = DashboardAdminSite(name="admin")


# ---------- Enregistrements ----------
@admin.register(Comment, site=dashboard_site)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "extrait", "created_at", "modified_at")
    search_fields = ("text",)
    list_filter = ("created_at",)
    ordering = ("-created_at",)

    @admin.display(description="Extrait")
    def extrait(self, obj):
        if not obj.text:
            return "—"
        return obj.text[:60] + ("…" if len(obj.text) > 60 else "")


@admin.register(Visitor, site=dashboard_site)
class VisitorAdmin(admin.ModelAdmin):
    list_display = ("user_anonymos", "note", "a_commentaire", "session", "created_at")
    list_filter = ("note", "created_at")
    search_fields = ("user_anonymos",)
    ordering = ("-created_at",)

    @admin.display(boolean=True, description="Commentaire ?")
    def a_commentaire(self, obj):
        return bool(obj.comment)


@admin.register(Vote, site=dashboard_site)
class VoteAdmin(admin.ModelAdmin):
    list_display = ("comment", "vote_type", "session", "created_at")
    list_filter = ("vote_type", "created_at")
    ordering = ("-created_at",)