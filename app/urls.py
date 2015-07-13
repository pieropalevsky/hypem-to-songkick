from django.conf.urls import patterns, include, url
from app.views import IndexView, ResultsView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name="index"),
    url(r'^results/$', ResultsView.as_view(), name="results"),
]