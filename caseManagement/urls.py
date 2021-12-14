from django.urls import path, include
from .views import case_view,case_details_view,new_case_view
from django.conf import settings
from django.views.static import serve



app_name = "case_urls"
urlpatterns = [
    path('',case_view, name="case"),
    path('create/new/^',new_case_view, name="new_case"),
    path('<int:pk>/detail/^',case_details_view, name="case_detail"),
    path(r'^download/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]