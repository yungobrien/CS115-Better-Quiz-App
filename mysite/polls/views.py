from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib.auth import authenticate, login
from django.contrib import messages

from django.template.response import TemplateResponse

from .models import Choice, Question, Quiz, Student, AnswerSet, ClassQuizResults

'''
def my_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
            login(request, user)
            # Redirect to success page
'''


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_quiz_list'

    def get_queryset(self):
        return Quiz.objects.all()


class DetailView(generic.DetailView):
    model = Quiz
    template_name = 'polls/detail.html'

    def get_queryset(self):
        return Quiz.objects.all()

#added to test submitting multiple forms with one button
class QuizDetailView(generic.DetailView):
    model = Quiz
    template_name = 'polls/quizdetail.html'

    def get_queryset(self):
        return Quiz.objects.all()


class ResultsView(generic.DetailView):
    model = Quiz
    template_name = 'polls/results.html'

#class AnswerSetDetailView(generic.DetailView):
class AnswerSetView(generic.ListView):
    #model = AnswerSet
    context_object_name = 'set_list'
    template_name = 'polls/answersets.html'

    def get_queryset(self):
        return AnswerSet.objects.all()


class ClassQuizResultsView(generic.ListView):
    #model = ClassQuizResults 
    template_name = 'polls/classresults.html'
    context_object_name = 'results_list'

    def get_queryset(self):
        return ClassQuizResults.objects.all()


def classquizresults(request, classquizresults_id):
    results = get_object_or_404(ClassQuizResults, pk=classquizresults_id)
    #results = ClassQuizResults.objects.get_or_create(pk=classquizresults_id)
    #get user
    #current_user = request.user

    #get student object from user object
    quiz = get_object_or_404(Quiz, pk=results.quiz.id)

    results.set_average()
    results.save()
    
    return render(request, 'polls/classquizresults.html', {
        'quiz': quiz,
        'class_results': results,
        #'classquizresults_id': results.id,
        })

def show_results(request, answer_set_id):
    #get user
    current_user = request.user

    #get student object from user object
    possible_student = Student.objects.get_or_create(user=current_user)
    current_student = possible_student[0]
    current_student.save()

    answerset = get_object_or_404(AnswerSet, pk=answer_set_id)
    #get quiz
    quiz = get_object_or_404(Quiz, pk=answerset.quiz.id)

    answerset.save()
    
    return render(request, 'polls/show_results.html', {
        'quiz': quiz,
        'answerset': answerset,
        'answer_set_id': answerset.id,
        })


#def submit_quiz(request, answer_set_id):
def submit_quiz(request, quiz_id):
    current_user = request.user
    possible_student = Student.objects.get_or_create(user=current_user)
    current_student = possible_student[0]
    #current_student is what we want
    current_student.save()

    quiz = get_object_or_404(Quiz, pk=quiz_id)

    #use student and quiz objects to get or create an answer set
    possible_answer_set = AnswerSet.objects.get_or_create(
        student = current_student, 
        quiz=quiz,
    )
    answer_set = possible_answer_set[0]
    answer_set.save()

    #create or add to class quiz results
    poss_results = ClassQuizResults.objects.get_or_create(quiz=quiz)
    class_results = poss_results[0]
    #current_student is what we want
    class_results.save()

    if request.method == 'POST':
        post_obj = request.POST
        post_dict = post_obj.dict()

        #number of quiz questions
        num_questions = quiz.question_set.count()

        #if post dictionary has less the number of questions + 1
        # where the 1 is for the CSRF token, reload and send message
        if len(post_dict) < num_questions + 1:
            messages.add_message(request, 30, 'You cannot submit a quiz unless you have answered every question')
            for k, v in post_dict.items():
                if k != 'csrfmiddlewaretoken':
                    for question in quiz.question_set.all():
                        if int(k) == question.id:
                            answer = Choice.objects.get(pk=v) 
                            answer.votes += 1
                            answer.save()

                            answer_set.answers.add(answer)
                            answer_set.update_score()

            return render(request,'polls/detail.html',{
                'quiz': quiz,
                'answerset': answerset,
                })
            #render html with message flag set


        for set_choice in answer_set.answers.all():
            answer_set.answers.remove(set_choice)
            answer_set.save()

        for k, v in post_dict.items():
            if k != 'csrfmiddlewaretoken':
                for question in quiz.question_set.all():
                    if int(k) == question.id:
                        answer = Choice.objects.get(pk=v) 
                        answer.votes += 1
                        answer.save()

                        answer_set.answers.add(answer)
                        answer_set.update_score()


    return HttpResponseRedirect(reverse('polls:show_results', args=(answer_set.id,)))
