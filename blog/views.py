# Create your views here.
from django.db.models import Subquery, OuterRef
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from utilities.paginator import ResponsePaginator
from .models import Content, ContentScore
from .serializers import ContentSerializer, ContentScoreSerializer


class ListContentAPIView(generics.GenericAPIView):
    serializer_class = ContentSerializer
    pagination_class = ResponsePaginator()
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user

        data = Content.valid_objects.all().annotate(
            user_score=Subquery(ContentScore.objects.filter(content=OuterRef('pk'), owner=user).values('score')[:1])
        )

        result = self.pagination_class.paginate_queryset(data, request)
        serializer = self.serializer_class(result, many=True, context={'request': request})
        return self.pagination_class.get_paginated_response(serializer.data)


class SubmitScoreAPIView(generics.GenericAPIView):
    serializer_class = ContentScoreSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        content = serializer.validated_data['content']
        score = serializer.validated_data['score']

        content_score, created = ContentScore.objects.update_or_create(owner=request.user, content=content,
                                                                       defaults={"score": score})

        if created:
            return Response({"message": "Score created successfully."}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "Score updated successfully."}, status=status.HTTP_200_OK)
