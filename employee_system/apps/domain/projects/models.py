from django.db import models
from apps.infrastructure.models import ActivityModel
from apps.domain.users.models import User
from apps.domain.company.models import Company
from apps.infrastructure.constants import STATUS, STATUS_PENDING

class ProjectRole(models.Model):
    name = models.CharField(max_length=50)
    ord = models.IntegerField()

    def __str__(self):
        return self.name.title()

    # def get_name_str(self):
    #     return self.get_name_display()


class Project(ActivityModel):

    name = models.CharField(
        max_length=100, blank=False, null=False, unique=True, db_index=True
    )
    is_deleted = models.BooleanField(db_column="deleted", default=False)
    is_third_party_project = models.BooleanField()
    details = models.CharField(max_length=255, blank=True, null=True)
    team_leader = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="projects_lead",
    )
    manager = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="projects_managed",
    )
    # company = models.ForeignKey(
    #     "company.Company",
    #     on_delete=models.CASCADE,
    #     blank=True,
    #     null=True,
    #     related_name="projects",
    # )
    members = models.ManyToManyField(
        "users.User", blank=True, related_name="projects", through="ProjectMember"
    )
    status = models.CharField(
        choices=STATUS, default=STATUS_PENDING, max_length=20, null=False, blank=False
    )
    detailed_description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
    
    def get_third_party_company(self):
        if self.is_third_party_project:
            company = Company.objects.get(project=self.id)
            return company
            

    class Meta:
        ordering = ["name"]


class ProjectMember(ActivityModel):
    """
    As a member of a team a user can be and admin or a regular
    user. This model is used in the m2m relation.
    """

    project = models.ForeignKey(
        "Project", related_name="project_memberships", on_delete=models.CASCADE
    )
    employee = models.ForeignKey(
        User, related_name="project_memberships", on_delete=models.CASCADE
    )
    role = models.ForeignKey(
        "ProjectRole",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="project_members",
    )

    def __str__(self):
        return f"{self.project.name} : {self.user.email} : {self.role}"

    class Meta:
        unique_together = (("project", "employee"),)
        ordering = ["project__name"]
