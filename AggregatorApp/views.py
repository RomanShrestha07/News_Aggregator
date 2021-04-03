from django.contrib.auth import authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
# from .forms import UserRegistrationForm
from .models import RawNews, Profile, News
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import UserForm, ProfileForm
from django.contrib.auth import views as auth_views
from django.views.generic import ListView, DetailView
from taggit.models import Tag
from django.db.models import Count


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


def news_processing(request):
    news = RawNews.objects.all()
    c = 0

    for n in news:
        c = c + 1
        source = n.source
        date_time = n.date_time
        section = n.section
        if section:
            s = section.lower()
        else:
            s = 'none'
        news_id = ''

        print(c)
        print(n.headline)

        if source == 'AP News':
            news_id = "AP-News-" + str(c)

            if s == 'u.s. news' or s == 'world news':
                section = 'World'
            if s == 'technology':
                section = 'Science and Technology'
            if s == 'religion':
                section = 'Culture'
            for t in n.tags:
                if t.lower() == 'sport' or t.lower() == 'sports':
                    section = 'Sports'

        elif source == 'The Guardian':
            news_id = "Guardian-" + str(c)

            if s == 'sports' or s == 'football' or s == 'sport':
                section = 'Sports'
            elif s == 'money' or s == 'business':
                section = 'Business'
            elif s == 'technology' or s == 'science':
                section = 'Science and Technology'
            elif s == 'music' or s == 'books' or s == 'film' or s == 'fashion' or s == 'stage' or s == 'games':
                section = 'Entertainment'
            elif s == 'society' or s == 'culture' or s == 'art and design' or s == 'travel' or s == 'food' or s == 'life and style':
                section = 'Culture'
            elif s == 'opinion':
                section = 'Opinion'
            elif s == 'world news' or s == 'us news' or s == 'uk news' or s == 'australia news' or s == 'global development':
                section = 'World'
            elif s == 'politics':
                section = 'Politics'
            elif s == 'environment':
                section = 'Environment'
            elif s == 'education' or s == 'television & radio' or s == 'media' or s == 'none' or s == 'info':
                section = 'Other'
            else:
                section = 'Other'

        elif source == 'Reuters':
            news_id = "Reuters-" + str(c)

            if s == 'technology':
                section = 'Science and Technology'
            if s == 'markets':
                section = 'Business'
            if s == 'lifestyle':
                section = 'Culture'
            for t in n.tags:
                if t.lower() == 'sport':
                    section = 'Sports'
                elif 'entertainment' in t.lower():
                    section = 'Entertainment'

        date = date_time[0:10]

        news2 = News(source=source, news_id=news_id,
                     headline=n.headline, author=n.author,
                     date_time=date, url=n.url, content=n.content,
                     section=section)

        news2.save()

        for t in n.tags:
            try:
                news2.tags.add(t.lower())
            except:
                news2.tags.add('-')

            news2.save()

    print("Successful")

    return redirect('AggregatorApp:news-table-1')


class NewsTable(ListView):
    model = News
    template_name = 'AggregatorApp/test-table.html'


class NewsListView(ListView):
    model = News
    template_name = 'AggregatorApp/test.html'


def news_list_table(request, tag_slug=None):
    object_list = News.objects.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    return render(request, 'AggregatorApp/test-table-2.html', {'object_list': object_list, 'tag': tag})


class NewsDetail(DetailView):
    model = News
    template_name = 'AggregatorApp/test-detail.html'


# def news_detail(request, year, month, day, news_id, pk):
#     news = get_object_or_404(News, news_id=news_id, pk=pk)
#     similar_news = news.tags.similar_objects()
#     return render(request, 'AggregatorApp/test-detail.html', {'news': news, 'similar_news': similar_news})


def category_world_news(request):
    object_list = News.objects.all()
    section = 'World News'
    object_list = object_list.filter(section='World')

    return render(request, 'AggregatorApp/category-table.html', {'object_list': object_list, 'section': section})


def category_sports(request):
    object_list = News.objects.all()
    section = 'Sports'
    object_list = object_list.filter(section='Sports')

    return render(request, 'AggregatorApp/category-table.html', {'object_list': object_list, 'section': section})


def category_business(request):
    object_list = News.objects.all()
    section = 'Business'
    object_list = object_list.filter(section='Business')

    return render(request, 'AggregatorApp/category-table.html', {'object_list': object_list, 'section': section})


def category_science_technology(request):
    object_list = News.objects.all()
    section = 'Science and Technology'
    object_list = object_list.filter(section='Science and Technology')

    return render(request, 'AggregatorApp/category-table.html', {'object_list': object_list, 'section': section})


def category_entertainment(request):
    object_list = News.objects.all()
    section = 'Entertainment'
    object_list = object_list.filter(section='Entertainment')

    return render(request, 'AggregatorApp/category-table.html', {'object_list': object_list, 'section': section})


def category_culture(request):
    object_list = News.objects.all()
    section = 'Culture'
    object_list = object_list.filter(section='Culture')

    return render(request, 'AggregatorApp/category-table.html', {'object_list': object_list, 'section': section})


def category_opinion(request):
    object_list = News.objects.all()
    section = 'Opinion'
    object_list = object_list.filter(section='Opinion')

    return render(request, 'AggregatorApp/category-table.html', {'object_list': object_list, 'section': section})


def category_politics(request):
    object_list = News.objects.all()
    section = 'Politics'
    object_list = object_list.filter(section='Politics')

    return render(request, 'AggregatorApp/category-table.html', {'object_list': object_list, 'section': section})


def category_environment(request):
    object_list = News.objects.all()
    section = 'Environment'
    object_list = object_list.filter(section='Environment')

    return render(request, 'AggregatorApp/category-table.html', {'object_list': object_list, 'section': section})


def category_other(request):
    object_list = News.objects.all()
    section = 'Other'
    object_list = object_list.filter(section='Other')

    return render(request, 'AggregatorApp/category-table.html', {'object_list': object_list, 'section': section})
