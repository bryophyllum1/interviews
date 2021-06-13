from django.urls import path
from interviews.views import IndexView, ScheduleInterview, InterviewDetail, InterviewerDetail, IntervieweeDetail, EditInterviews, accessView

app_name="interviews"
urlpatterns = [
	path('interview/<int:key>/<str:email>/', accessView),
    path('', IndexView.as_view(), name="listView2"),
    path('interview/', IndexView.as_view(), name="listView3"),
    path('list/', IndexView.as_view(), name="listView"),
    path('schedule/', ScheduleInterview.as_view(), name="schedule"),
    path('update/<int:pk>', EditInterviews.as_view(), name='update'),
    path('interview/<int:pk>', InterviewDetail.as_view(), name='viewInterview'),
    path('interviewer/<int:pk>', InterviewerDetail.as_view(), name='viewInterviewer'),
    path('interviewee/<int:pk>', IntervieweeDetail.as_view(), name='viewInterviewee'),

    # path('reschedule/', views.index, name='reschedule'),
    # path('/', views.index, name='listInterviews'),
]

