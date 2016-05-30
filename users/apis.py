# from django.http import JsonResponse
# from rest_framework import viewsets
# from rest_framework.decorators import list_route
# from rest_framework.permissions import AllowAny
#
# from .models import User
# from .serializers import UserRegistrationSerializer, UserSerializer
#
#
# @list_route(methods=['post'])
# def register(request):
#     serialized = UserRegistrationSerializer(data=request.data)
#     if serialized.is_valid():
#         User.objects.create_user(
#             serialized.data['email'],
#             serialized.data['password']
#         )
#         return JsonResponse({"status": "200", "message": "OK"})
#     else:
#         return JsonResponse({"status": "400", "message": serialized.errors})
#
#
# class UserViewSet(viewsets.GenericViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [AllowAny, ]
#
#     @list_route(methods=['post'])
#     def register(self, request):
#         """
#         发送邮件验证
#         """
#         serializer = UserRegistrationSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         phone = serializer.data['phone']
#         try:
#             is_shopuser = int(request.POST.get('is_shopuser', False))
#         except ValueError:
#             return Response(data={'message': '400001 is_shopuser 参数类型错误'}, status=status.HTTP_400_BAD_REQUEST)
#         if is_shopuser:
#             # 商家注册
#             user = ShopUser.objects.create_shopuser(phone=phone)
#         else:
#             try:
#                 user = User.objects.get(phone=phone)
#             except User.DoesNotExist:
#                 user = User.objects.create_user(phone=phone)
#
#         if user.last_verify_time:
#             interval_seconds = (timezone.now() - user.last_verify_time).seconds
#             if interval_seconds < MAX_SMS_INTERVAL_SECONDS:
#                 # 两次验证码间隔小于1分钟
#                 return Response(data={'message': '403002 验证码请求过于频繁'}, status=status.HTTP_403_FORBIDDEN)
#         generate_verify_code(phone)
#         return Response(data={'message': '验证码发送成功'}, status=status.HTTP_200_OK)
#     #
#     # @list_route(methods=['post'])
#     # def login(self, request):
#     #     serializer = UserLoginSerializer(data=request.data)
#     #     serializer.is_valid(raise_exception=True)
#     #
#     #     try:
#     #         user = User.objects.get(phone=serializer.data['phone'])
#     #     except User.DoesNotExist:
#     #         return Response(data={'message': '404001 未找到绑定该手机号的用户'}, status=status.HTTP_404_NOT_FOUND)
#     #
#     #     if (timezone.now() - user.last_verify_time).seconds > MAX_SMS_VALID_SECONDS:
#     #         return Response(data={'message': '401001 验证码已经超时失效'}, status=status.HTTP_401_UNAUTHORIZED)
#     #
#     #     if user.verify_code != serializer.data['verify_code']:
#     #         return Response(data={'message': '401002 验证码错误'}, status=status.HTTP_401_UNAUTHORIZED)
#     #
#     #     user.verify_code = None
#     #     user.save()
#     #     token = get_jwt_token(user)
#     #     return Response({'jwt': token}, status=status.HTTP_200_OK)
#     #
#     # @list_route(methods=['get'], permission_classes=[IsAuthenticated])
#     # def check(self, request):
#     #     serializer = UserSerializer(request.user)
#     #     return Response(serializer.data, status=status.HTTP_200_OK)
