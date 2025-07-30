from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", TemplateView.as_view(template_name="base.html"), name="base"),
    path("catalog/", TemplateView.as_view(template_name="base.html")),
    path("catalog/clothes/", TemplateView.as_view(template_name="base.html")),
    path("catalog/clothes/men/", TemplateView.as_view(template_name="base.html")),
    path("catalog/clothes/women/", TemplateView.as_view(template_name="base.html")),
    path("catalog/shoes/", TemplateView.as_view(template_name="base.html")),
    path("catalog/accessories/", TemplateView.as_view(template_name="base.html")),
    path("about/", TemplateView.as_view(template_name="base.html")),
    path("about/team/", TemplateView.as_view(template_name="base.html")),
    path("about/contacts/", TemplateView.as_view(template_name="base.html")),
]
