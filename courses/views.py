from re import search
from unicodedata import category
from rest_framework import status
from logging import raiseExceptions
from educator import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from .models import *
from base.models import *
from base.api.serializers import *
from rest_framework import filters
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from .pagination import PaginationHandlerMixin
from rest_framework.pagination import PageNumberPagination
from .filters import CourseFilter


class AddCategoryUser(APIView):
    permission_classes = [IsAuthenticated,]
    def put(self,request):
        email = request.user.email
        user = NewUserRegistration.objects.get(email__iexact=email)
        serializer = catSerializer(data=request.data)

        if serializer.is_valid():
            for i in range(11):
                s = 'Interest' + str(i+1)
                if serializer.data[s] == True:
                    gettingCategory = interests.objects.get(id=i + 1)
                    user.interested.add(gettingCategory)
        else:
            return Response({'msg':'Invalid Entry'}, status=status.HTTP_400_BAD_REQUEST)            
        
        serializer = profileSerializer(user, many=False)

        return Response(serializer.data)
        


class ViewAllCategories(APIView):
    def get(self,request):
        categories = interests.objects.all()
        serializer = categorySerializer(categories, many=True)
        
        return Response(serializer.data)

class ViewAllCourses(APIView):
    def get(self,request):
        data = Course.objects.all()
        data = Course.objects.order_by('-rating')
        serializer = TopicSerializer(data, many=True)
        return Response(serializer.data)


class CourseView(APIView):
    permission_classes = [IsAuthenticated,]
    def post(self,request):
        email = request.user.email
        user = NewUserRegistration.objects.get(email__iexact=email)
        request.POST._mutable = True
        request.data["educator_mail"] = request.user.id
        request.data["educator_name"] = user.name
        request.POST._mutable = False
        if user.is_educator == True:
            serializer = TopicSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)    
        else:
            return Response({'msg':'user is not an educator'})    
 
class BasicPagination(PageNumberPagination):
    page_size_query_param = 'limit'            

class viewFilteredCourses(APIView, PaginationHandlerMixin):
    permission_classes = [IsAuthenticated,]
    pagination_class = BasicPagination
    serializer_class = TopicSerializer
    def get(self,request):
        email = request.user.email
        user = NewUserRegistration.objects.get(email__iexact=email)
        array = user.interested.all()
        courses = Course.objects.filter(category__in=array)
        
        courses = Course.objects.order_by('-rating')
        page = self.paginate_queryset(courses)
        if page is not None:
            serializer = self.get_paginated_response(self.serializer_class(page,many=True).data)
        else:
            serializer = self.serializer_class(courses, many=True)
        
        return Response(serializer.data)
        
        
class CourseRating(APIView):
    permission_classes = [IsAuthenticated,]
    def post(self,request):
        email = request.user.email
        user = NewUserRegistration.objects.get(email__iexact=email)
        history = feedbackmodel.objects.filter(user = user.name,course=request.data.get('course'))
        if len(history)!=0:
            return Response({'msg':'you already gave your review for this course'})
        request.POST._mutable = True
        request.data["sender"] = user.id
        request.data["user"] = user.name
        request.POST._mutable = False
        seri = GetRatingSerializer(data=request.data)
        if seri.is_valid(raise_exception=True):
            seri.save()
            ck = feedbackmodel.objects.latest('time')
            course=ck.course
            count = course.review_count
            rating = course.rating
            ser = RatingSerializer(instance = course,data=request.data)
            if ser.is_valid(raise_exception=True):
                ser.save()
                review = course.latest_review
                # return Response(check)
                if count == 0:
                    ser = RatingSerializer(instance = course,data=request.data)
                    if ser.is_valid(raise_exception=True):
                        course.rating = review
                        course.review_count = 1
                        ser.save()
                        return Response({'msg':'Thanks for your review'})
                else:
                    present_rating = rating*count
                    new_rating = (present_rating + review)/(count + 1)
                    count+=1
                    course.review_count = count
                    ser = RatingSerializer(instance = course,data=request.data)
                    if ser.is_valid(raise_exception=True):
                        course.rating = new_rating
                        ser.save()
                        return Response({'msg':'Thanks for your review'})
                return Response({'msg':'Something went wrong'})
            # ser = RatingSerializer(instance = course,data=request.data)
            # if ser.is_valid(raise_exception=True):
            #     ser.save()
            #     return Response(rating)
            return Response({'msg':'enter valid details'})

class searching(APIView):
    
    def get(self,request):
        queryset = Course.objects.all()
        myFilter = CourseFilter(request.GET, queryset=queryset)
        queryset = myFilter.qs
        
        searchResult = request.GET.get('search-area') or ''
        
        if searchResult:
            queryset = queryset.filter(topic__icontains=searchResult)
            
        serializer = TopicSerializer(queryset, many=True)
        
        if serializer.data == []:
            return Response({'msg':'Nothing Found'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.data)  
    
class purchasedcourses(APIView):
    permission_classes = [IsAuthenticated,]
    def get(self,request):
        email = request.user.email
        user = NewUserRegistration.objects.get(email__iexact=email)
        array = user.purchasedCourse.all()
        courses = Course.objects.filter(id__in=array)
        ser = TopicSerializer(courses, many=True)
        return Response(ser.data)
    

class LessonView(APIView):
    permission_classes = [IsAuthenticated,]
    
    def get(self,request):
        lesson = lessons.objects.all()
        serializer = lessonSerializer(lesson, many=True)
        
        return Response(serializer.data)
    
    
    
    def post(self,request):
        email = request.user.email
        user = NewUserRegistration.objects.get(email__iexact=email)
        topic = request.data.get("topic")
        course = Course.objects.get(id=topic)
        
        if str(course.educator_mail) != str(email):
            return Response({'msg':'invalid'})
        
        
        try:
            print(course.educator_mail)
            print(email)
            if user.is_educator == True:
                    request.POST._mutable = True
                    request.data["topic"] = topic
                    request.POST._mutable = False
                    serializer = lessonSerializer(data=request.data)
                    if serializer.is_valid(raise_exception=True):
                        serializer.save()
                        print(serializer['topic'])
                        return Response(serializer.data)    
            else:
                    return Response({'msg':'user is not an educator'})
        except:
            return Response({'msg':'invalid'}, status=status.HTTP_400_BAD_REQUEST)     
        
    
class viewSpecificCourseLesson(APIView):
    def post(self,request):
        try:
            topic = request.data.get("topic")
            lesson = lessons.objects.filter(topic=topic)
            serializer = lessonSerializer(lesson, many=True)
            if serializer.data == []:
                return Response({"msg":"No such course exists"},status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.data)
        except:
            return Response({"msg":"Enter a valid course"}, status=status.HTTP_400_BAD_REQUEST)  
            
class CourseFeedback(APIView):
    def get(self,request,ck):
        course = feedbackmodel.objects.filter(course = ck)
        ser = GetRatingSerializer(instance = course , many = True)
        return Response(ser.data)