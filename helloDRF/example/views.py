from rest_framework import viewsets, permissions, status, generics, mixins
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from .models import Book
from .serializers import BookSerializer

# Create your views here.

# 함수형 뷰(FBV)
@api_view(['GET'])
def helloAPI(request):
    return Response("hello world!")

@api_view(['GET', 'POST']) # 데코레이터를 사용하여 GET, POST 요청 모두 처리 가능하도록 처리
def booksAPI(request):
    if request.method == 'GET': 
        books = Book.objects.all() #전체 데이터 가져오기
        serializer = BookSerializer(books, many=True) #전체 데이터 한번에 직렬화
        return Response(serializer.data, status=status.HTTP_200_OK)             # 200 보내며 성공
    elif request.method == 'POST':
        serializer = BookSerializer(data=request.data) #요청으로 들어온 데이터 한번에 직렬화
        if serializer.is_valid(): #유효한 데이터라면
            serializer.save() #역직렬화를 통해 save(), 모델시리얼라이저의 기본 create() 함수가 동작함
            return Response(serializer.data, status=status.HTTP_201_CREATED)    # 201 보내며 성공
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # 400 보내며 에러

@api_view(['GET'])
def bookAPI(request, bid):
    book = get_object_or_404(Book, bid=bid) # 특정 bid의 책 데이터를 가져옴
    serializer = BookSerializer(book)
    return Response(serializer.data, status=status.HTTP_200_OK)

# 클래스형 뷰(CBV)
class HelloAPI(APIView):
    def get(self, request, format=None):
        return Response("hello world")

class BooksAPI(APIView):
    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK) 
    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookAPI(APIView):
    def get(self, request, bid):
        book = get_object_or_404(Book, bid=bid)
        serializer = BookSerializer(book)
        return Response(serializer.data, status=status.HTTP_200_OK) 
    




# mixin과 generics 사용
class BooksAPIMixins(mixins.ListModelMixin, mixins.CreateModelMixin,generics.GenericAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class BookAPIMixins(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'bid'

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    def put(self, request, *args, **kwargs): 
        return self.update(request, *args, **kwargs) 
    def delete(self, request, *args, **kwargs): 
        return self.destroy(request, *args, **kwargs) 




# mixins 세트 -> generics의 코드들이 xinins로 만들어본 코드임.
class BooksAPIGenerics(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookAPIGenerics(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'bid'