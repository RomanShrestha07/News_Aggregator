from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.http import HttpResponse
# from .forms import UserRegistrationForm
from .models import RawNews, Profile, News
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import UserForm, ProfileForm
from django.contrib.auth import views as auth_views
from django.views.generic import ListView, DetailView


def index(request):
    return render(request, 'AggregatorApp/index.html')


def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            print('Your profile was successfully updated!')
            return redirect('AggregatorApp:index')
        else:
            print('Please correct the error below.')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'AggregatorApp/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


class SignIn(auth_views.LoginView):
    template_name = 'AggregatorApp/sign-in.html'


class TestTable(ListView):
    model = News
    template_name = 'AggregatorApp/test-table.html'


class NewsListView(ListView):
    model = News
    template_name = 'AggregatorApp/test.html'


class NewsDetail(DetailView):
    model = News
    template_name = 'AggregatorApp/test-detail.html'


def news_detail(request):
    news = RawNews.objects.all()
    c = 0

    for n in news:
        c = c + 1
        source = n.source
        date_time = n.date_time
        news_id = ''

        if source == 'AP News':
            news_id = "AP-News-" + str(c)

        date = date_time[0:10]

        news2 = News(source=source, news_id=news_id,
                     headline=n.headline, author=n.author,
                     date_time=date, url=n.url, content=n.content)

        news2.save()

        for t in n.tags:
            news2.tags.add(t)
            news2.save()

    print("Successful")

    return render(request, 'AggregatorApp/index.html')
