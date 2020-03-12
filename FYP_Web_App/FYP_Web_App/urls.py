"""FYP_Web_App URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from fyp_website import views
from accounts import views as acc_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^login/$', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    url(r'^signup/$', acc_views.signup, name='signup'),
    url(r'^settings/password/$', auth_views.PasswordChangeView.as_view(template_name='password_change.html'),
    name='password_change'),
    url(r'^settings/password/done/$', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'),
    name='password_change_done'),
    url(r'^account_info/', acc_views.account_info, name='account_info'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    url(r'^sna_viz/$', views.sna_viz, name='sna_viz'),
    url(r'^dataset_cntr', views.dataset_constructor, name='dataset_cntr'),
    url(r'^admin/', admin.site.urls),
    url(r'^query_csv_upload/$', views.query_csv_upload, name='query_csv_upload'),
    url(r'^rel_sup_csv_upload/$',views.rel_sup_csv_upload, name='rel_sup_csv_upload'),
    url(r'^get_analysis_results/$', views.get_analysis_results, name='get_analysis_results'),
    url(r'^cancel_analysis/$', views.cancel_analysis, name='cancel_analysis'),
    url(r'^text_file_upload/$', views.text_file_upload, name='text_file_upload'),
    url(r'^select_news_article/$', views.select_news_article, name='select_news_article'),
    url(r'^ind_sent_query/$', views.select_ind_sentence, name='ind_sent_query'),
]
