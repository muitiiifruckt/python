from django.db import models

class ChessGame(models.Model):
    white_player = models.CharField(max_length=100)
    black_player = models.CharField(max_length=100)
    event = models.CharField(max_length=100, blank=True, null=True)
    site = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateField()
    round = models.CharField(max_length=10, blank=True, null=True)
    result = models.CharField(max_length=7)
    pgn_text = models.TextField()

    def __str__(self):
        return f"{self.white_player} vs {self.black_player} - {self.date}"
