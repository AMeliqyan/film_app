from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_page, name='login'),
    path('edit/', views.edit, name='edit'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout_user, name='logout'),
    path('passwordcheng/', views.passwordcheng, name='passwordcheng'),
    path('add_film/', views.add_film, name='add_film'),
    path('film_page/<int:id>', views.film_index, name='film_id'),
    path('del_film/<int:id>', views.del_film, name='del_film'),
    path('update_film/<int:id>', views.update_film, name='update_film'),
    path('feedback/<int:id>', views.feedback, name='feedback'),
    path('user_users/', views.user_users, name='user_users'),
    path('user_films/', views.user_films, name='user_films'),
    path('accept_film/<int:id>', views.accept_film, name='accept_film'),
    path('decline_film/<int:id>', views.decline_film, name='decline_film'),
    path('user_notification', views.user_notification, name='user_notification'),
    path('seen/<int:id>', views.seen, name='seen'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('password_reset/', views.ResetPasswordView.as_view(), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='film/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='film/password_reset_complete.html'),
         name='password_reset_complete'),

]
