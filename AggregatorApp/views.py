from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
# from .forms import UserRegistrationForm
from .models import RawNews, Profile, News, BlockedSources, SavedNews
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import UserForm, ProfileForm
from django.contrib.auth import views as auth_views
from django.views.generic import ListView, DetailView
from taggit.models import Tag, TaggedItem
from django.db.models import Count
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required


def index(request):
    return render(request, 'AggregatorApp/index.html')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('AggregatorApp:index')
    else:
        form = UserCreationForm()
    return render(request, 'AggregatorApp/sign-up.html', {'form': form})


@login_required(login_url='/sign-in/')
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


@staff_member_required()
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
            elif s == 'technology' or s == 'science':
                section = 'Science and Technology'
            elif s == 'religion' or s == 'travel' or s == 'lifestyle':
                section = 'Culture'
            elif s == 'oddities':
                section = 'Other'
            for t in n.tags:
                if t.lower() == 'sport' or t.lower() == 'sports':
                    section = 'Sports'
                if t.lower() == 'politics':
                    section = 'Politics'

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


def category(request, section):
    object_list = News.objects.all()
    s = section
    st = section.title()
    if s == 'science-technology':
        st = 'Science and Technology'

    object_list = object_list.filter(section=st)

    return render(request, 'AggregatorApp/category-table.html', {'object_list': object_list, 'section': st})


def category_top(request):
    object_list = News.objects.all()
    section = 'Top'

    tag = get_object_or_404(Tag, slug='ap-top-news')
    object_list = object_list.filter(tags__in=[tag])

    return render(request, 'AggregatorApp/category-table.html', {'object_list': object_list, 'section': section})


def add_tags(request, tag_slug=None):
    tag = None
    user = request.user

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        profile = Profile.objects.get(user=user)
        profile.tag.add(tag)
        profile.save()

    return redirect('AggregatorApp:user-feed')


@login_required(login_url='/sign-in/')
def user_feed(request):
    ol = News.objects.all()
    profile = Profile.objects.filter(user=request.user)
    blocked = BlockedSources.objects.filter(user=request.user)
    nid_list = []
    object_list = []

    for user_tags in profile:
        if user_tags.tag:
            for tags in user_tags.tag.all():
                test_list = ol.filter(tags__in=[tags])

                for item in test_list:
                    nid_list.append(item.news_id)
        else:
            print('No tags.')

    if nid_list:
        nid_set = set(nid_list)
        print(nid_set)

        for i in nid_set:
            r = ol.get(news_id=i)

            if blocked:
                for b in blocked:
                    if b.source_name != r.source:
                        object_list.append(r)
                    else:
                        print('News ' + str(r.news_id) + ' is blocked -- ' + str(r.source) + ' blocked.')
            else:
                object_list.append(r)
    else:
        print('No tags selected. -- 2')

    return render(request, 'AggregatorApp/user-feed.html', {'object_list': object_list, 'profile': profile})


def save_news(request, pk):
    user = request.user
    news = News.objects.get(pk=pk)
    tags = TaggedItem.objects.filter(object_id=pk)

    news2 = SavedNews(user=user, source=news.source, headline=news.headline,
                      author=news.author, date_time=news.date_time, tags=tags,
                      url=news.url, content=news.content, section=news.section)

    news2.save()
    le = []

    for t in tags:
        print(t.tag.name)
        print(type(t.tag.name))
        le.append(t.tag.name)

    for i in le:
        news2.tags.add(i)
        news2.save()

    return redirect('AggregatorApp:index')
