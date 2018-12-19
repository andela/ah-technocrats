from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from authors.apps.articles.models import ReportArticle, Article
from authors.apps.articles.serializers import ReportArticleSerializer
from authors.apps.authentication.models import User


class ReportListAPIView(APIView):
    permission_classes = (IsAdminUser,)
    serializer_class = ReportArticleSerializer

    def get(self, request):
        # TODO:  Catch empty result errors
        query_set = ReportArticle.objects.all()
        serializer = self.serializer_class(query_set, many=True)
        reports = []
        for i in range(len(serializer.data)):
            single_report = {
                "article": Article.objects.get(id=serializer.data[i]['article']).title,
                "reported_by": User.objects.get(id=serializer.data[i]['reported_by']).username,
                "report": ReportArticle.REPORT_CHOICES[serializer.data[i]['report']][1]
            }
            reports.append(single_report)
        return Response({"reports": reports}, status=status.HTTP_200_OK)


class ReportArticleAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ReportArticleSerializer

    def post(self, request, **kwargs):
        try:
            article_slug = kwargs.get('slug')
            article = Article.objects.get(article_slug=article_slug)
            reported_by = request.user
            report = request.data.get('report')
            data = {"article": article.pk, "reported_by": reported_by.pk, "report": report}
            serializer = self.serializer_class(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"Success": "You have submitted a report",
                             "article": article.title,
                             "report": ReportArticle.REPORT_CHOICES[int(report)][1]
                             }, status=status.HTTP_201_CREATED)
        except Article.DoesNotExist:
            return Response({"Error": "That article does not exist"}, status=status.HTTP_404_NOT_FOUND)
