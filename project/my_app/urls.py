from django.urls import path,include
from . import views
urlpatterns = [
    path("signup/",views.Signup,name="signup"),
    path("",views.login,name="login"),
    path("home/",views.home,name="home"),
    path("library/",views.library,name="library"),
    path("create/",views.create,name="create"),
    path("list/",views.list_view,name="view"),
    path("edit/<int:id>",views.edit,name="edit"),
    path("delete/<int:id>",views.delete,name="delete"),
    path("profile/",views.profile,name="profile"),
    path("edit_profile/",views.edit_profile,name="edit_profile"),
    path("logout/",views.logout,name="logout"),
]
