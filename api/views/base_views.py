from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from api.serializers.base_serializers import ProfileSerializer, UserSerializer
from base.models import Profile

def create_user_data(profile):
    return {
        'id':profile.user.id,
        'username':profile.user.username,
        'first_name':profile.user.first_name,
        'last_name':profile.user.last_name,
        'email':profile.user.email,
        'phone_no':profile.phone_no,
        'date_of_birth':profile.date_of_birth,
        'address':profile.address,
        "position":profile.position,
        'date_joined':profile.user.date_joined,
        'last_login':profile.user.last_login
    }

@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({"message": "Both Username and Password are required."}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)

    if user is not None:
        login(request, user)

        refresh = RefreshToken.for_user(user)
        data = { 'refresh': str(refresh), 'access': str(refresh.access_token) }
        return Response(data, status=status.HTTP_202_ACCEPTED)
    else:
        return Response({"message":"Invalid Credentials!"}, status=status.HTTP_401_UNAUTHORIZED)
    
@api_view(['GET','POST'])
def users_view(request):
    if request.method == 'GET':
        users = User.objects.filter(is_superuser=False, is_staff=False)
        user_details_list = []

        for user in users:
            profile = Profile.objects.get(user=user)
            entry = create_user_data(profile)
            user_details_list.append(entry)

        return Response(user_details_list, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        userSerializer = UserSerializer(data=request.data)

        if userSerializer.is_valid():
            user = userSerializer.save()
            profile_data = request.data
            profile_data['user'] = user.id
            profileSerializer = ProfileSerializer(data=profile_data)
            
            if profileSerializer.is_valid():
                profile = profileSerializer.save()
                data = create_user_data(profile)
                return Response(data, status=status.HTTP_201_CREATED)
            else:
                user.delete()
                return Response(profileSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(userSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"message":"Invalid Request!"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

@api_view(['GET','PUT','DELETE'])
def user_view(request, id):
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return Response({"message":"A user with the given ID does not exist"}, status=status.HTTP_404_NOT_FOUND)
    
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=user)
        profile.save()
    
    if request.method == 'GET':
        data = create_user_data(profile)
        return Response(data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        userSerializer = UserSerializer(user, data=request.data)
        if userSerializer.is_valid():
            userSerializer.save()

            profileSerializer = ProfileSerializer(profile, data=request.data)
            if profileSerializer.is_valid():
                profile = profileSerializer.save()
                data = create_user_data(profile)
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response(profileSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(userSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        user.delete()
        return Response({"message":f"ID {id}: {user.first_name} {user.last_name} has been deleted!"}, status=status.HTTP_200_OK)
    else:
        return Response({"message":"Invalid Request!"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)