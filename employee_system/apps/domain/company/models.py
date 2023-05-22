from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=80)
    project = models.ForeignKey(
        "projects.Project", related_name="company_project", on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return str(self.name)
    
