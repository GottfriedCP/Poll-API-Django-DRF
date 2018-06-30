from django.contrib.auth import authenticate
from rest_framework import generics, status, viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Poll, Choice
from .serializers import PollSerializer, ChoiceSerializer, VoteSerializer, UserSerializer

class PollList(generics.ListCreateAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

class PollDetail(generics.RetrieveDestroyAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

#two classes above are replaced by below:
class PollViewSet(viewsets.ModelViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    
    def destroy(self, request, *args, **kwargs):
        poll = Poll.objects.get(pk=self.kwargs['pk'])
        if not request.user == poll.created_by:
            raise PermissionDenied('You are not the owner of this poll')
        return super().destroy(request, *args, **kwargs)

class ChoiceList(generics.ListCreateAPIView):
    def get_queryset(self):
        # List choices of a poll, identified by its pk
        queryset = Choice.objects.filter(poll_id=self.kwargs['pk'])
        return queryset
    serializer_class = ChoiceSerializer

    def post(self, request, *args, **kwargs):
        # Choices of a poll can only be created by its owner
        poll = Poll.objects.get(pk=self.kwargs['pk'])
        if not request.user == poll.created_by:
            raise PermissionDenied('You are not the owner of this poll')
        return super().post(request, *args, **kwargs)

class CreateVote(APIView):
    def post(self, request, pk, choice_pk):
        voted_by = request.data.get('voted_by')
        data = {
            'choice': choice_pk,
            'poll': pk,
            'voted_by': request.user.pk, # originally, this was 'voted_by'
        }
        serializer = VoteSerializer(data=data)
        if serializer.is_valid():
            vote = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CreateUser(generics.CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    # Lines above are to excempt this endpoint from security
    serializer_class = UserSerializer

class LoginView(APIView):
    permission_classes = ()

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            return Response({'token': user.auth_token.key})
        else:
            return Response({'error': 'invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
            