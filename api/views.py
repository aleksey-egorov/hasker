from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from django.db.models import Q
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.response import Response
from rest_framework.decorators import action

from question.models import Question, Answer
from api.serializers import IndexSerializer, TrendingSerializer, SearchSerializer, QuestionSerializer, AnswerSerializer


class IndexViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all().order_by('-pub_date')
    serializer_class = IndexSerializer

class TrendingViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.order_by('-votes')[:10]
    serializer_class = TrendingSerializer

class SearchViewSet(viewsets.ModelViewSet):
    serializer_class = SearchSerializer

    def get_queryset(self):
        query = self.request.GET.get('q')
        queryset = Question.objects.filter(Q(heading__icontains=query) | Q(content__icontains=query)).order_by('votes','-pub_date')[:20]
        return queryset

class QuestionViewSet(viewsets.ModelViewSet):

    def retrieve(self, request, version=None, pk=None):
        question = get_object_or_404(Question, pk=pk)
        serializer = QuestionSerializer(question)
        return Response(serializer.data)

    @action(methods=['get'], detail=True, url_path='answers', url_name='answers')
    def answers(self, request, version=None, pk=None):
        if version == 'v1':
            question = get_object_or_404(Question, pk=pk)
            answers = Answer.objects.filter(question_ref=question).order_by('votes').all()
            serializer = AnswerSerializer(answers, many=True)
            return Response(serializer.data)
        elif version == 'v2':
            question = get_object_or_404(Question, pk=pk)
            answers = Answer.objects.filter(question_ref=question).order_by('-pub_date').all()
            serializer = AnswerSerializer(answers, many=True)
            return Response(serializer.data)