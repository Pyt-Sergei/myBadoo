from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt, csrf_protect

from .serializers import MyUserSerializer, LikeSerializer
from .models import MyUser, Likes
from .authentication import SessionCsrfExemptAuthentication
from .email import email_send


class Home(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            return Response({
                'message': f'Hello, {request.user.email}',
                'user': MyUserSerializer(request.user, context={'request': request}).data,
            })
        return Response({'message': f'Hello, {request.user.__str__()}'})


class CreateUser(CreateAPIView):
    serializer_class = MyUserSerializer
    authentication_classes = [SessionCsrfExemptAuthentication]


class UserList(LoginRequiredMixin, ListAPIView):
    queryset = MyUser.objects.all()
    serializer_class = MyUserSerializer

    filterset_fields = ['gender', 'first_name', 'last_name']
    search_fields = ['^first_name', '^last_name', '^email']

    # raise_exception = True
    login_url = '/login/'


class UpdateView(UpdateAPIView):
    queryset = MyUser.objects.all()
    serializer_class = MyUserSerializer
    authentication_classes = [SessionCsrfExemptAuthentication]
    permission_classes = [IsAuthenticated]


class DeleteView(DestroyAPIView):
    queryset = MyUser.objects.all()
    serializer_class = MyUserSerializer
    authentication_classes = [SessionCsrfExemptAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response(
            {'message': f'The user {request.user.__str__()} has been deleted'},
            status=status.HTTP_204_NO_CONTENT
        )


@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            return JsonResponse({
                'status': 'ok',
                'message': 'Logged in as %s' % request.user.email,
            })
        return JsonResponse({'error': 'Wrong credentials'})
    return JsonResponse({'message': 'Welcome to login page'})


@login_required(login_url='/login/')
def logout_view(request):
    logout(request)
    return JsonResponse({'message': 'Logged out'})


@login_required(login_url='/login/')
@csrf_exempt
def like_view(request):
    if request.method == 'POST':
        receiver = request.POST.get('receiver')
        sender = request.user
        try:
            receiver = int(receiver)
            receiver = MyUser.objects.get(pk=receiver)
        except ValueError:
            try:
                receiver = MyUser.objects.get(email=receiver)
            except ObjectDoesNotExist:
                return JsonResponse({"error": f"User with email {receiver} doesn't exist"})
        except TypeError:
            return JsonResponse({'error': 'Provide a lovely user email address or id to like it'})
        except ObjectDoesNotExist:
            return JsonResponse({"error": f"User with id {receiver} doesn't exist"})
        else:
            if receiver.id == sender.id:
                return JsonResponse({'message': 'You cannot like yourself, baby ;)'})

        receiver_email = receiver.email
        like = Likes(sender_id=sender, receiver_id=receiver)
        like.save()

        # subject = f'Hello, {receiver_email}!'
        # message = f'You get this message because {request.user.email} likes you :)'
        # resp = email_send(subject, message, [receiver_email])
        # if not resp:
        #     print(resp)
        #     return JsonResponse({'message': 'You have liked the user %s' % receiver_email})
        # return JsonResponse(resp)
        JsonResponse({'message': 'You have liked the user %s' % receiver_email})

    likes = LikeSerializer(Likes.objects.filter(sender_id=request.user.id), many=True)
    return JsonResponse(likes.data, safe=False)
