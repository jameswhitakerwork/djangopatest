from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Question, Choice, Signature
from .forms import SignatureForm
from django.views import generic
from django.utils import timezone

from jsignature.utils import draw_signature
import json


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the latest 5 questions (not inc. future questions)"""
        return Question.objects.filter(
            pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # redisplay question voting form
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': 'You did not select a choice',
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse(
            'polls:results', args=(question.id,)))


def my_signature(request):
    form = SignatureForm(request.POST or None)
    if form.is_valid():
        signature = form.cleaned_data.get('signature')
        new_signature = Signature()
        new_signature.signature = json.dumps(signature)
        new_signature.save()
        print Signature.objects.get(pk=new_signature.pk)

        if signature:
            # as an image
            signature_picture = draw_signature(signature)
            print signature_picture
            # or as a file
            signature_file_path = draw_signature(signature, as_file=True)
            print signature_file_path

    return render(request, 'polls/signature.html', {
        'form': form
    })
