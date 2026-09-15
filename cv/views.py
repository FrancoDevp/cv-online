from django.views.generic import TemplateView

from .models import CVDocument, Education, Experience, Profile, Project, Skill


class HomeView(TemplateView):
    template_name = "cv/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["profile"] = Profile.load()
        context["documents"] = CVDocument.objects.all()
        context["experiences"] = Experience.objects.all()
        context["education"] = Education.objects.all()
        context["projects"] = Project.objects.filter(published=True)
        context["skills"] = Skill.objects.all()

        return context
