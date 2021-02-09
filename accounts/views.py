from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from .serializers import UserSerializer, ProfileAndVRSerializer, FeedBackSerializer
from .models import ProfileAndVR, AccountResetLink, FeedBack
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
import datetime
from django.utils import timezone
import string
import random
from sogo.scheduler import scheduler

# Create your views here.


def generate_token():
    token = ''
    for i in range(50):
        token += random.choice(string.ascii_letters +
                               string.digits + string.hexdigits)
    return token


def set_activation_token():
    token = generate_token()
    while ProfileAndVR.objects.filter(activation_token=token).first():
        token = generate_token()
    return token


def send_activation_token(user, profile):
    if not profile.activation_token:
        profile.activation_token = set_activation_token()
        profile.save()
    subject, from_email, to = 'Activate your account', \
                              'info@sogovr.com', user.email
    text_content = 'Hey {} please reset password'.format(user.username)
    html_content = '<p>Hey {a} please reset password .' \
                   '</p><a href="https://sogovr.com/activate-account/{b}">' \
                   'https://sogovr.com/activate-account/{b}</a>' \
        .format(a=user.username, b=profile.activation_token)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = User.objects.all()

        return queryset


class ProfileAndVRViewSet(ModelViewSet):
    serializer_class = ProfileAndVRSerializer
    queryset = ProfileAndVR.objects.all()


class ChangePassword(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        print(request.data)
        element_counter = 0
        user_id = request.data.get('user_id')
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        if user_id:
            element_counter += 1
        if old_password:
            element_counter += 1
        if new_password:
            element_counter += 1
        if element_counter != 3:
            return Response({"message": "element required for the request is missing"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(pk=user_id)
            if user.check_password(old_password):
                user.set_password(new_password)
                user.save()
                return Response({"message": "Password changed successful"},
                                status=status.HTTP_201_CREATED)
            else:
                return Response({"message": "old password does not match"},
                                status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"message": "User not found"})


class ResendActivationToken(APIView):

    def post(self, request):
        email = request.data.get("email")
        print(email)

        errors = []

        if not email:
            errors.append(dict(email='email field is required'))

        if len(errors) > 0:
            return Response({"message": errors}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(email=email)
            profile = ProfileAndVR.objects.get(user=user)
            # send_activation_token(user, profile)
            scheduler.add_job(send_activation_token, 'date', run_date=timezone.now(),
                          args=[user, profile])
            return Response({"message": "activation token resent to your email"},
                            status=status.HTTP_200_OK)
        except:
            return Response({"message": "User not found"}, status=status.HTTP_400_BAD_REQUEST)


class ActivateAccount(APIView):

    def post(self, request):
        email = request.data.get("email")
        token = request.data.get("token")

        errors = []

        if not email:
            errors.append(dict(email='email field is required'))

        if not token:
            errors.append(dict(token='token field is required'))

        if len(errors) > 0:
            return Response({"message": errors}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(email=email)
            profile = ProfileAndVR.objects.get(user=user)
            if token == profile.activation_token:
                profile.active = True
                profile.save()
                return Response({"message": "account has been activated successful"},
                                status=status.HTTP_200_OK)
            return Response({"message": "invalid activation token"}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"message": "User not found"}, status=status.HTTP_400_BAD_REQUEST)


class SendResetPassword(APIView):
    permission_classes = permissions.AllowAny,

    def get_user_or_none(self, email):
        user = User.objects.filter(email=email).first()
        return user

    def get_link(self, user):
        link = AccountResetLink.objects.filter(user=user).first()
        if not link:
            link = AccountResetLink.objects.create(user=user)
        else:
            if timezone.now() > (link.date_time + datetime.timedelta(hours=2)):
                print('Current time is 2mins ahead of expiry date')
                link.delete()
                link = AccountResetLink.objects.create(user=user)
                return link
        return link

    def send_reset_link(self, email, user, link):
        subject, from_email, to = 'FORGOT YOUR PASSWORD?', 'info@sogovr.com', email
        text_content =  """
                        There was a request to change your password!, 
                        If did not make this request, just ignore this email. 
                        Otherwise, please click the button below to change your password:
                        https://sogovr.com/reset-password/{}

                        For security, this request was received from Alpha and Nimbus.
                        If you did not request a password reset, please ignore this email or contact
                        admin@sogovr.com if you have question
                        """.format(link.reset_token)
        html_content = """
                        <div style="padding: 20px;">
                        <p>Hey {a} please reset password</p>
                        <p>There was a request to change your password!,</p>
                        <p style="margin-bottom: 30px"> If did not make this request, just ignore this email. 
                        Otherwise, please click the button below to change your password: </p>
                        <a style="margin: 20px 0 auto; padding: 20px 50px; border: 1px solid black; border-radius: 20px; margin-top: 30px; margin-bottom: 30px"
                         href="https://sogovr.com/reset-password/{b}">
                        RESET PASSWORD</a>
                        <p style="margin-top: 30px">
                        For security, this request was received from Alpha and Nimbus.
                        If you did not request a password reset, please ignore this email or contact
                        <a mailto="admin@sogovr.com" >admin@sogovr.com</a> if you have question
                        </p>
                        </div>
                      """.format(a=user.username, b=link.reset_token)
        msg = EmailMultiAlternatives(
            subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({"message": "email field is required"}, status=status.HTTP_400_BAD_REQUEST)

        user = self.get_user_or_none(email)
        if user:
            link = self.get_link(user)
            scheduler.add_job(self.send_reset_link, 'date', run_date=timezone.now(),
                          args=[email, user, link])
            return Response({"message": "Reset link has been sent to your account"},
                            status=status.HTTP_200_OK)
        else:
            return Response({"message": "User not found"}, status=status.HTTP_400_BAD_REQUEST)


class ConfirmResetToken(APIView):

    def post(self, request):
        token = request.data.get("reset_token")
        if not token:
            return Response({"token": "reset token is required"}, status=status.HTTP_400_BAD_REQUEST)
        reset_link = AccountResetLink.objects.filter(reset_token=token).first()
        if reset_link:
            if timezone.now() <= (reset_link.date_time + datetime.timedelta(minutes=5)):
                return Response({"message": "reset token is valid"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "reset token has expired"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "Invalid reset token"}, status=status.HTTP_400_BAD_REQUEST)


class ResetPassword(APIView):

    def post(self, request):
        token = request.data.get("reset_token")
        password = request.data.get("password")
        errors = []
        if not token:
            errors.append({"token": "reset token is required"})
        if not password:
            errors.append({"password": "new password is required"})
        if len(errors) > 0:
            return Response({"message": errors}, status=status.HTTP_400_BAD_REQUEST)

        reset_link = AccountResetLink.objects.filter(reset_token=token).first()
        if not reset_link:
            return Response({"message": "Invalid reset token"}, status=status.HTTP_400_BAD_REQUEST)
        if timezone.now() <= (reset_link.date_time + datetime.timedelta(hours=2)):
            user = reset_link.user
            user.set_password(password)
            user.save()
            return Response({"message": "password changed successful"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "Reset token has expired"})


class FeedBackViewSet(ModelViewSet):
    queryset = FeedBack.objects.all()
    serializer_class = FeedBackSerializer


def jwt_response_payload_handler(token, user=None, request=None):
    return dict(token=token, userid=user.id)
