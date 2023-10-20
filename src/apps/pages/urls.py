from django.urls import path
from apps.pages import views

urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('ads/<slug:slug>/', views.AdsView.as_view(), name="ad_detail"),
    path('ads-comment/', views.AdsCommentView.as_view(), name="add_ads_comment"),
    path('doctor-search/', views.IndexDoctorSearchView.as_view(), name="index_doctor_search"),
    path('facility-search/', views.IndexFacilitySearchView.as_view(), name="index_facility_search"),
    path('issue-search/', views.IndexIssueSearchView.as_view(), name="index_issue_search"),
    path('index_doctor_pagination/', views.IndexDoctorPaginationView.as_view(), name="index_doctor_pagination_view"),
    path('about/', views.AboutView.as_view(), name="about"),
    path('contact/', views.ContactView.as_view(), name="contact"),
    path('index_news_pagination/', views.IndexNewsPaginationView.as_view(), name="index_news_pagination_view"),
    path('index_conference_pagination/', views.IndexConfPaginationView.as_view(), name="index_conf_pagination_view"),
    path('index_blog_pagination_view/', views.IndexBlogPaginationView.as_view(), name="index_blog_pagination_view"),

    path('news/', views.NewsListView.as_view(), name="news"),
    path('news/<slug:slug>/', views.NewsDetailView.as_view(), name="news_detail"),
    path('conference/', views.ConferenceListView.as_view(), name="conference"),
    path('conference/<slug:slug>/', views.ConferenceDetailView.as_view(), name="conference_detail"),
]
