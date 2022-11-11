from django.shortcuts import render
from rest_framework import status
from logging import raiseExceptions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from courses.serializers import *
from .models import *
from base.models import *

# Create your views here.
class createcart(APIView):
    def post(self,request):
        ser = CartSerializer(data=request.data)
        if ser.is_valid(raise_exception=True):
            ser.save()
            return Response({'msg':'cart added successfully'})

class cartid(APIView):
    permission_classes = [IsAuthenticated,]
    def get(self,request):
        email = request.user.email
        cart_details = cart.objects.get(email__iexact =email)
        cart_id = cart_details.id
        return Response(cart_id)

class Cart_View(APIView):
    permission_classes = [IsAuthenticated,]
    def put(self,request):
        email = request.user.email
        user = NewUserRegistration.objects.get(email__iexact=email)
        course_array = user.purchasedCourse.all()
        course_id = request.data.get("course")
        for course in course_array:
            # crs = Course.objects.get(topic=a)
            # cid = crs.id
            # print(a.id)
            # print(ck)
            if (course.id==int(course_id)) :
                return Response({'msg':'course already purchased'}, status=status.HTTP_400_BAD_REQUEST)
                # print('iterate')
        cart_details = cart.objects.get(email__iexact =email)
        cart_id = cart_details.id
        request.POST._mutable = True
        request.data["cart"] = cart_id
        request.POST._mutable = False
        ser = AddCartSerializer(data=request.data)
        if ser.is_valid(raise_exception=True):
            # data =request.data
            carts=request.data.get("cart")
            course=request.data.get("course")
            cart_course = cart_courses.objects.filter(cart=carts,course=course)
            l = len(cart_course)
            if l == 0:
                ser.save()
                return Response({'msg':'course added successfully to cart'})
            else:
                return Response({'msg':'course already added to cart'}, status=status.HTTP_400_BAD_REQUEST)

    def get(self,request):
        email = request.user.email
        user = NewUserRegistration.objects.get(email__iexact=email)
        cart_id = cart.objects.get(email__iexact =email)
        # print(ct.id)
        courses = cart_courses.objects.filter(cart=cart_id.id)
        # print(courses)
        if len(courses) == 0:
            return Response({'msg':'no courses in cart'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            courselist= []
            for course in courses:
                cid = course.course.id
                crs = Course.objects.get(id=cid)
                ser = TopicSerializer(instance = crs)
                # print(ser.data)
                courselist.append(ser.data)

        # ser = TopicSerializer(instance = courselist, many = True)
        return Response(courselist)

class cartremove(APIView):
    permission_classes = [IsAuthenticated,]
    def delete(self,request,ck):
        email = request.user.email
        user = NewUserRegistration.objects.get(email__iexact=email)
        ct = cart.objects.get(email__iexact =email)
        # print(ct.id)
        cart_courseid = cart_courses.objects.filter(cart=ct.id,course=ck)
        if len(cart_courseid)==0:
            return Response({'msg':'course does not exist in cart'}, status=status.HTTP_400_BAD_REQUEST)
        cart_courseid.delete()
        return Response({'msg':'course removed successfully from cart'})