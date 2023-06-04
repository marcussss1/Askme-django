from django.urls import path

from askme import views

from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from Web import settings

urlpatterns = [
    path('', views.index, name="index"),
    path('question/<int:question_id>/', views.question, name="question"),
    path('hot/', views.hot, name="hot"),
    path('tag/<tag>/', views.tag, name="tag"),
    path('ask/', views.ask, name="ask"),
    path('profile/edit/', views.profile, name="profile"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('signup/', views.signup, name="signup"),

    path('like/', views.like, name="like"),
    path('clike/', views.clike, name="clike"),
    path('ransw/', views.set_right_answ, name="ransw"),

    path('ajax_comment/', views.ajax_comment, name='ajax_comment'),

    path('params/', views.request_params, name='params'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()