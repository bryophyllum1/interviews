from django.template import loader
from .models import Person, Interviewer, Interviewee, Interview
from django.views import generic
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone





class IndexView(generic.ListView):
	# model = Interview
	context_object_name='upcoming_interviews'
	queryset=Interview.objects.filter(start_datetime__gte=timezone.now())
	template_name='interviews/index.html'
	

	# def get_queryset(self):
	# 	return Interview.objects.order_by('start_datetime')
		# template=loader.get_template('interviews/index.html')
		# return render(request, 'interviews/index.html', {"upcoming_interviews": upcoming_interviews,})

def check_clash(ivi, start, end):
	if ((ivi.start_datetime <= start and ivi.end_datetime <= start)\
			or (ivi.start_datetime >= end and ivi.end_datetime >= end)):
		return False
	else:
		return True


class ScheduleInterview(generic.CreateView):
	model=Interview
	template_name = "interviews/schedule.html"
	fields = ['interviewee','interviewer', 'start_datetime', 'end_datetime', 'more_info']
	def get_success_url(self):
		return reverse("interviews:listView")

	def form_valid(self, form):
		self.object = form.save(commit=False)
		isdt = form.cleaned_data['start_datetime']
		iedt = form.cleaned_data['end_datetime']
		wees = form.cleaned_data['interviewee']
		wers = form.cleaned_data['interviewer']
		if isdt <= timezone.now():
			raise ValidationError("Please select a starting date in the present/future")
		if (iedt-isdt).total_seconds() < 0:
			raise ValidationError("Please select an ending date after starting date")
		if len(wees) < 2:
			raise ValidationError("There are less than two interviewers. Not done man!")
		for wee in wees:
			iv_list = wee.interviewee.all()
			for ivi in iv_list:
				if check_clash(ivi, isdt, iedt):
					raise ValidationError(f"{wee.name} has an interview that clashes with this one")
		for wer in wers:
			iv_list = wer.interviewer.all()
			for ivi in iv_list:
				if check_clash(ivi, isdt, iedt):
					raise ValidationError(f"{wer.name} has an interview that clashes with this one")
		self.object.save()
		form.save_m2m()

		for wee in wees:
			subject = f'Hi, {wee.name} your interview is scheduled from {isdt} to {iedt}'
			message = "Congratulations! Your Interview is scheduled."
			email_from = settings.EMAIL_HOST_USER
			recipient_list=[wee.email, ]
			send_mail( subject, message, email_from, recipient_list )
		return super(generic.edit.ModelFormMixin, self).form_valid(form)

class EditInterviews(generic.UpdateView):
	model = Interview
	template_name = "interviews/update.html"
	fields = ['interviewee','interviewer', 'start_datetime', 'end_datetime', 'more_info']
	def get_success_url(self):
		return reverse("interviews:listView")
	def form_valid(self, form):
		self.object = form.save(commit=False)
		isdt = form.cleaned_data['start_datetime']
		iedt = form.cleaned_data['end_datetime']
		wees = form.cleaned_data['interviewee']
		wers = form.cleaned_data['interviewer']
		if isdt <= timezone.now():
			raise ValidationError("Please select a starting date in the present/future")
		if (iedt-isdt).total_seconds() < 0:
			raise ValidationError("Please select an ending date after starting date")
		if len(wees) < 2:
			raise ValidationError("There are less than two interviewers. Not done man!")
		for wee in wees:
			iv_list = wee.interviewee.all()
			for ivi in iv_list:
				if ivi==self.object:
					continue
				if check_clash(ivi, isdt, iedt):
					raise ValidationError(f"{wee.name} has an interview that clashes with this one")
		for wer in wers:
			iv_list = wer.interviewer.all()
			for ivi in iv_list:
				if  ivi == self.object:
					continue
				if check_clash(ivi, isdt, iedt):
					raise ValidationError(f"{wer.name} has an interview that clashes with this one")
		self.object.save()
		form.save_m2m()

		for wee in wees:
			subject = f'Hi, {wee.name} your interview is scheduled from {isdt} to {iedt}'
			message = "Congratulations! Your Interview is scheduled."
			email_from = settings.EMAIL_HOST_USER
			recipient_list=[wee.email, ]
			send_mail( subject, message, email_from, recipient_list )
		return super(generic.edit.ModelFormMixin, self).form_valid(form)


class InterviewDetail(generic.DetailView):
	model = Interview
	template_name = 'interviews/interview_detail.html'
	context_object_name = 'interview'

class InterviewerDetail(generic.DetailView):
	model = Interviewer
	template_name = 'interviews/interviewer_detail.html'
	context_object_name = 'interviewer'


class IntervieweeDetail(generic.DetailView):
	model = Interviewee
	template_name = 'interviews/interviewee_detail.html'
	context_object_name = 'interviewee'


def index(request):
	return render(HttpResponse("Hi! Working on it man!"))

# def detail(request, interview_id):
# 	try:
# 		interview= Interview.objects.get(pk = interview_id)
# 	except Interview.DoesNotExist:
# 		raise Http404("Interview doesn't exist.")
# 	return render(request, 'interviews/detail.html', {'interview': interview})

# def schedule(request):
