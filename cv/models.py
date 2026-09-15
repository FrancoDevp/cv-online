from django.db import models
from django.utils.formats import date_format


SKILL_KIND_CHOICES = [("herramienta", "Herramienta"), ("tecnica", "Técnica")]
SKILL_AREA_CHOICES = [
    ("qa", "QA / Testing"),
    ("it", "IT / Soporte"),
    ("desarrollo", "Desarrollo"),
    ("gestion", "Gestión / Versionado"),
]
SKILL_LEVEL_CHOICES = [
    ("trabajo", "Trabajo"),
    ("proyectos", "Proyectos"),
    ("formacion", "Formación"),
]
EXPERIENCE_AREA_CHOICES = [
    ("qa", "QA / Testing"),
    ("it", "IT / Soporte"),
    ("desarrollo", "Desarrollo"),
    ("otro", "Otro"),
]
EDUCATION_KIND_CHOICES = [
    ("carrera", "Carrera"),
    ("bootcamp", "Bootcamp"),
    ("curso", "Curso"),
]
PROJECT_CATEGORY_CHOICES = [
    ("web", "Desarrollo web"),
    ("qa", "QA / Testing"),
    ("education", "Formación académica"),
    ("other", "Otro"),
]


class PeriodDisplayMixin:
    @property
    def is_current(self):
        return self.end_date is None

    @property
    def period_display(self):
        end = "actualidad" if self.is_current else date_format(self.end_date, "b. Y")
        return f"{date_format(self.start_date, 'b. Y')} – {end}"


class Profile(models.Model):
    full_name = models.CharField(max_length=120, default="")
    headline = models.CharField(max_length=160, default="")
    tagline = models.CharField(max_length=160, default="")
    hero_description = models.TextField(default="")
    about = models.TextField(default="")
    email = models.EmailField(default="")
    location = models.CharField(max_length=200, default="")
    linkedin_url = models.URLField(default="")
    github_url = models.URLField(default="")
    page_title = models.CharField(max_length=200, default="")
    meta_description = models.TextField(default="")

    class Meta:
        verbose_name = "Perfil"
        verbose_name_plural = "Perfil"

    @classmethod
    def load(cls):
        return cls.objects.first()

    def __str__(self):
        return self.full_name


class CVDocument(models.Model):
    label = models.CharField(max_length=120, default="")
    static_path = models.CharField(max_length=200, default="")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "label"]
        verbose_name = "Documento del CV"
        verbose_name_plural = "Documentos del CV"

    def __str__(self):
        return self.label


class Skill(models.Model):
    KIND_CHOICES = SKILL_KIND_CHOICES
    AREA_CHOICES = SKILL_AREA_CHOICES
    LEVEL_CHOICES = SKILL_LEVEL_CHOICES

    name = models.CharField(max_length=100, default="")
    kind = models.CharField(max_length=20, choices=KIND_CHOICES)
    area = models.CharField(max_length=20, choices=AREA_CHOICES)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    group = models.CharField(max_length=100, default="", blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["area", "group", "order", "name"]
        constraints = [
            models.UniqueConstraint(fields=["name"], name="skill_name_unico"),
            models.CheckConstraint(
                condition=models.Q(kind__in=[choice[0] for choice in SKILL_KIND_CHOICES]),
                name="skill_kind_valido",
            ),
            models.CheckConstraint(
                condition=models.Q(area__in=[choice[0] for choice in SKILL_AREA_CHOICES]),
                name="skill_area_valido",
            ),
            models.CheckConstraint(
                condition=models.Q(level__in=[choice[0] for choice in SKILL_LEVEL_CHOICES]),
                name="skill_level_valido",
            ),
        ]
        verbose_name = "Habilidad"
        verbose_name_plural = "Habilidades"

    def __str__(self):
        return self.name


class Experience(PeriodDisplayMixin, models.Model):
    AREA_CHOICES = EXPERIENCE_AREA_CHOICES

    company = models.CharField(max_length=200, default="")
    position = models.CharField(max_length=200, default="")
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    area = models.CharField(max_length=20, choices=AREA_CHOICES)
    description = models.TextField(default="", blank=True)
    responsibilities = models.TextField()
    featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    skills = models.ManyToManyField(Skill, blank=True, related_name="experiences")

    class Meta:
        ordering = ["-start_date"]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(area__in=[choice[0] for choice in EXPERIENCE_AREA_CHOICES]),
                name="experience_area_valido",
            ),
        ]
        verbose_name = "Experiencia"
        verbose_name_plural = "Experiencias"

    def __str__(self):
        return f"{self.position} - {self.company}"


class Education(PeriodDisplayMixin, models.Model):
    KIND_CHOICES = EDUCATION_KIND_CHOICES

    institution = models.CharField(max_length=200, default="")
    title = models.CharField(max_length=200, default="")
    kind = models.CharField(max_length=20, choices=KIND_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField(default="", blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["-start_date"]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(kind__in=[choice[0] for choice in EDUCATION_KIND_CHOICES]),
                name="education_kind_valido",
            ),
        ]
        verbose_name = "Formación"
        verbose_name_plural = "Formaciones"

    def __str__(self):
        return f"{self.title} - {self.institution}"


class Project(models.Model):
    CATEGORY_CHOICES = PROJECT_CATEGORY_CHOICES

    title = models.CharField(max_length=200, default="")
    description = models.TextField(default="")
    technologies = models.CharField(max_length=300, default="", blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    github_url = models.URLField(default="", blank=True)
    demo_url = models.URLField(default="", blank=True)
    published = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "title"]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(category__in=[choice[0] for choice in PROJECT_CATEGORY_CHOICES]),
                name="project_category_valido",
            ),
        ]
        verbose_name = "Proyecto"
        verbose_name_plural = "Proyectos"

    def __str__(self):
        return self.title
