
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('team-registration', views.team_registration, name='team_registration'),
    path('registeration-completed', views.completed_registration, name='complete_registration'),
    path('match-fixture', views.get_match_fixture, name='get_match_fixture'),
    path('admin-login', views.admin_login, name='admin_login'),
    path('admin/list-all-teams', views.list_all_teams, name='list_all_teams'),
    path('admin/team-details/<int:team_id>',views.team_details, name='team_details'),
    path('admin/get-match-details', views.get_match_details, name='get_match_details'),
    path('admin/update-match-point', views.update_match_points, name='update_match_points'),
    path('admin-logout', views.admin_logout, name='admin_logout'),
]