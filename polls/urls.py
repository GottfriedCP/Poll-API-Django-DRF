from django.urls import path
from rest_framework.routers import DefaultRouter
from .apiviews import PollList, PollDetail, PollViewSet, ChoiceList, CreateVote, CreateUser, LoginView

urlpatterns = [
    #path('polls/', PollList.as_view(), name='polls_list'),
    #path('polls/<int:pk>/', PollDetail.as_view(), name='polls_detail'),
    #paths above are replaced by router below
    path('polls/<int:pk>/choices/', ChoiceList.as_view(), name='choice_list'),
    path('polls/<int:pk>/choices/<int:choice_pk>/vote/', CreateVote.as_view(), name='create_vote'),
    path('users/', CreateUser.as_view(), name='user_create'),
    path('login/', LoginView.as_view(), name='login'),
]

router = DefaultRouter()
router.register('polls', PollViewSet, base_name='polls')

urlpatterns += router.urls