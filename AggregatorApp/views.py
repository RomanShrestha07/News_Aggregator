from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
import requests, json
# from .forms import UserRegistrationForm
from .models import RawNews, Profile, News, BlockedSources, SavedNews, Comment
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import UserForm, ProfileForm, CommentForm
from django.contrib.auth import views as auth_views
from django.views.generic import ListView, DetailView, DeleteView
from taggit.models import Tag, TaggedItem
from django.db.models import Count
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.dateparse import parse_date


def index(request):
    object_list = News.objects.all()
    section = 'index'

    popular_tag = get_object_or_404(Tag, slug='ap-top-news')
    pop = News.objects.filter(tags__in=[popular_tag])
    cul = News.objects.filter(section='Culture')
    opi = News.objects.filter(section='Opinion')
    oth = News.objects.filter(section='Other')

    try:
        popular_news = remove_blocked_sources(pop, request.user)
        cultural_news = remove_blocked_sources(cul, request.user)
        opinion_news = remove_blocked_sources(opi, request.user)
        other_news = remove_blocked_sources(oth, request.user)
    except:
        popular_news = set(pop)
        cultural_news = set(cul)
        opinion_news = set(opi)
        other_news = set(oth)
        print('Invalid user.')

    return render(request, 'AggregatorApp/index.html',
                  {'section': section, 'popular_news': popular_news, 'cultural_news': cultural_news,
                   'opinion_news': opinion_news, 'other_news': other_news})


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
            messages.error(request, 'Please enter the data according to the guidelines below.')
    else:
        form = UserCreationForm()
    return render(request, 'AggregatorApp/sign-up.html', {'form': form})


class SignIn(auth_views.LoginView):
    template_name = 'AggregatorApp/sign-in.html'


def view_profile(request):
    profile = Profile.objects.get(user=request.user)

    return render(request, 'AggregatorApp/profile-view.html', {'profile': profile})


@login_required(login_url='/sign-in/')
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            print('Your profile was successfully updated!')
            return redirect('AggregatorApp:profile')
        else:
            print('Please correct the error below.')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'AggregatorApp/profile-update.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })


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
            elif s == 'ap fact check':
                section = 'Opinion'
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
        print(news_id)
        print(n.headline)

        if n.content and n.headline:
            news2 = News(source=source, news_id=news_id,
                         headline=n.headline, author=n.author,
                         date_time=date, url=n.url, content=n.content,
                         section=section, image=n.image, description=n.description)

            news2.save()

            for t in n.tags:
                try:
                    news2.tags.add(t.lower())
                except:
                    news2.tags.add('-')

                news2.save()

    print("Successful")

    return redirect('AggregatorApp:index')


def sidebar_news(object_list, user):
    popular_news_list = []
    opinion_news_list = []
    cultural_news_list = []
    other_news_list = []

    popular_tag = get_object_or_404(Tag, slug='ap-top-news')
    pop = News.objects.filter(tags__in=[popular_tag])
    opi = News.objects.filter(section='Opinion')
    cul = News.objects.filter(section='Culture')
    oth = News.objects.filter(section='Other')

    blocked_sources = []
    blocked_all = []
    try:
        blocked_all = BlockedSources.objects.filter(user=user)
    except:
        print('Invalid user')

    for b in blocked_all:
        blocked_sources.append(b.source_name)

    for item in pop:
        if item not in object_list and item.source not in blocked_sources:
            popular_news_list.append(item)

    for item in opi:
        if item not in object_list and item.source not in blocked_sources:
            opinion_news_list.append(item)

    for item in cul:
        if item not in object_list and item.source not in blocked_sources:
            cultural_news_list.append(item)

    for item in oth:
        if item not in object_list and item.source not in blocked_sources:
            other_news_list.append(item)

    popular_news = list(set(popular_news_list))
    opinion_news = list(set(opinion_news_list))
    cultural_news = list(set(cultural_news_list))
    other_news = list(set(other_news_list))

    return popular_news, opinion_news, cultural_news, other_news


def remove_blocked_sources(object_list, user):
    blocked_sources = []
    blocked_all = BlockedSources.objects.filter(user=user)
    print(blocked_all)
    for b in blocked_all:
        blocked_sources.append(b)

    if blocked_sources:
        print(blocked_sources)
        ol = object_list.exclude(source__in=blocked_sources)
        object_list = set(ol)
        print(object_list)
    else:
        ol = object_list
        object_list = set(ol)
        print(object_list)

    return object_list


def news_by_tag(request, tag_slug=None):
    object_list = News.objects.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    try:
        object_list = remove_blocked_sources(object_list, request.user)
    except:
        print('Invalid user.')

    side_news = sidebar_news(object_list, request.user)
    popular_news = side_news[0]
    opinion_news = side_news[1]
    cultural_news = side_news[2]

    return render(request, 'AggregatorApp/saved-news.html',
                  {'object_list': object_list, 'tag': tag, 'popular_news': popular_news, 'opinion_news': opinion_news,
                   'cultural_news': cultural_news})


def news_by_source(request, source):
    object_list = News.objects.filter(source__in=[source])
    s = source
    blocked = ''
    blocked_sources = []
    blocked_all = BlockedSources.objects.all()
    for b in blocked_all:
        blocked_sources.append(b.source_name)

    if s in blocked_sources:
        blocked = 'The source is blocked.'

    try:
        object_list = remove_blocked_sources(object_list, request.user)
    except:
        print('Invalid user.')

    side_news = sidebar_news(object_list, request.user)
    popular_news = side_news[0]
    opinion_news = side_news[1]
    cultural_news = side_news[2]

    return render(request, 'AggregatorApp/source-news.html',
                  {'object_list': object_list, 'source': s, 'cultural_news': cultural_news,
                   'opinion_news': opinion_news, 'popular_news': popular_news, 'blocked': blocked})


def news_by_date(request, date):
    date_str = date
    d = parse_date(date_str)

    ol = News.objects.all().filter(date_time=d)

    try:
        object_list = remove_blocked_sources(ol, request.user)
    except:
        object_list = set(ol)
        print('Invalid user.')

    side_news = sidebar_news(object_list, request.user)
    popular_news = side_news[0]
    opinion_news = side_news[1]
    cultural_news = side_news[2]

    return render(request, 'AggregatorApp/source-news.html',
                  {'object_list': object_list, 'date': d, 'popular_news': popular_news,
                   'opinion_news': opinion_news, 'cultural_news': cultural_news})


def news_by_author(request, author):
    ol = News.objects.all().filter(author=author)
    a = author
    try:
        object_list = remove_blocked_sources(ol, request.user)
    except:
        object_list = set(ol)
        print('Invalid user.')

    side_news = sidebar_news(object_list, request.user)
    popular_news = side_news[0]
    opinion_news = side_news[1]
    cultural_news = side_news[2]

    return render(request, 'AggregatorApp/source-news.html',
                  {'object_list': object_list, 'author': a, 'popular_news': popular_news,
                   'opinion_news': opinion_news, 'cultural_news': cultural_news})


class NewsDetail(DetailView):
    model = News
    template_name = 'AggregatorApp/news-detail.html'

    def get_context_data(self, **kwargs):
        context = super(NewsDetail, self).get_context_data(**kwargs)

        popular_tag = get_object_or_404(Tag, slug='ap-top-news')
        pn = News.objects.filter(tags__in=[popular_tag])
        on = News.objects.filter(section='Opinion')
        saved = []

        if self.request.user:
            try:
                sn = SavedNews.objects.filter(user=self.request.user)

                for s in sn:
                    saved.append(s.url)
            except:
                print('Invalid User.')

        popular_news = set(pn)
        opinion_news = set(on)

        obj = self.get_object()
        if obj in popular_news:
            popular_news.discard(obj)
        if obj in opinion_news:
            opinion_news.discard(obj)

        context['popular_news'] = popular_news
        context['opinion_news'] = opinion_news
        context['saved'] = saved
        return context


def category(request, section):
    object_list = News.objects.all()
    s = section
    st = section.title()

    top = []
    row_top = []
    row_bottom = []
    rest = []
    pn = []
    cultural_news = []
    opinion_news = []
    other_news = []

    if s == 'science-technology':
        st = 'Science and Technology'

    if section == 'top':
        tag = get_object_or_404(Tag, slug='ap-top-news')
        object_list = object_list.filter(tags__in=[tag])
    else:
        object_list = object_list.filter(section=st)

    try:
        ols = remove_blocked_sources(object_list, request.user)
    except:
        ols = set(object_list)
    object_list = list(ols)

    length = len(object_list)
    if object_list:
        top.append(object_list[0])

    if length == 2:
        for i in range(1, length):
            item = object_list[i]
            rest.append(item)

    elif length == 3:
        for i in range(1, length):
            item = object_list[i]
            row_top.append(item)

    elif length == 4:
        for i in range(1, length):
            item = object_list[i]
            if i <= 2:
                row_top.append(item)
            else:
                rest.append(item)

    elif length >= 5:
        for i in range(1, length):
            item = object_list[i]
            if i <= 2:
                row_top.append(item)
            elif 2 < i <= 4:
                row_bottom.append(item)
            else:
                rest.append(item)

    popular_tag = get_object_or_404(Tag, slug='ap-top-news')
    pop = News.objects.filter(tags__in=[popular_tag])
    cul = News.objects.filter(section='Culture')
    opi = News.objects.filter(section='Opinion')
    oth = News.objects.filter(section='Other')

    try:
        pop = remove_blocked_sources(pop, request.user)
        cul = remove_blocked_sources(cul, request.user)
        opi = remove_blocked_sources(opi, request.user)
        oth = remove_blocked_sources(oth, request.user)
    except:
        pop = set(pop)
        print('Invalid user.')

    popular_news = not_in(pop, pn, top, row_top, row_bottom, rest)
    cultural_news = not_in(cul, cultural_news, top, row_top, row_bottom, rest)
    opinion_news = not_in(opi, opinion_news, top, row_top, row_bottom, rest)
    other_news = not_in(oth, other_news, top, row_top, row_bottom, rest)

    return render(request, 'AggregatorApp/category.html',
                  {'object_list': object_list, 'st': st, 'section': section, 'top': top,
                   'row_top': row_top, 'row_bottom': row_bottom, 'rest': rest,
                   'popular_news': popular_news, 'cultural_news': cultural_news,
                   'opinion_news': opinion_news, 'other_news': other_news})


def not_in(og_list, new_list, top, row_top, row_bottom, rest):
    for item in og_list:
        if item not in top and item not in row_top and item not in row_bottom and item not in rest:
            new_list.append(item)
    return new_list


@login_required(login_url='/sign-in/')
def add_tags(request, tag_slug=None):
    tag = None
    user = request.user

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        profile = Profile.objects.get(user=user)
        profile.tag.add(tag)
        profile.save()

    return redirect('AggregatorApp:user-feed')


def added_tags_list(request):
    profile = Profile.objects.filter(user=request.user)
    blocked = BlockedSources.objects.filter(user=request.user)
    tag_list = []

    for user_tags in profile:
        if user_tags.tag:
            for tags in user_tags.tag.all():
                print(type(tags))
                tag_list.append(tags)
        else:
            print('No tags.')

    return render(request, 'AggregatorApp/added-tags.html', {'tag_list': tag_list})


def remove_tags(request, tag_slug=None):
    tag = None
    user = request.user

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        profile = Profile.objects.get(user=user)
        profile.tag.remove(tag)
        profile.save()

    return redirect('AggregatorApp:added-tags-list')


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
                print(tags)
                test_list = ol.filter(tags__in=[tags])

                for item in test_list:
                    nid_list.append(item.news_id)
        else:
            print('No tags.')

    if nid_list:
        nid_set = set(nid_list)

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

    object_list = set(object_list)
    side_news = sidebar_news(object_list, request.user)
    popular_news = side_news[0]
    opinion_news = side_news[1]
    cultural_news = side_news[2]

    return render(request, 'AggregatorApp/user-feed.html',
                  {'object_list': object_list, 'profile': profile, 'popular_news': popular_news,
                   'opinion_news': opinion_news, 'cultural_news': cultural_news})


@login_required(login_url='/sign-in/')
def save_news(request, pk):
    user = request.user
    news = News.objects.get(pk=pk)
    tags = TaggedItem.objects.filter(object_id=pk)

    news2 = SavedNews(user=user, source=news.source, headline=news.headline,
                      author=news.author, date_time=news.date_time,
                      url=news.url, content=news.content, section=news.section,
                      image=news.image, description=news.description)

    news2.save()

    for t in tags:
        news2.tags.add(t.tag)
        news2.save()

    return redirect('AggregatorApp:saved-news')


@login_required(login_url='/sign-in/')
def saved_news_list_view(request):
    object_list = SavedNews.objects.filter(user=request.user)

    side_news = sidebar_news(object_list, request.user)
    popular_news = side_news[0]
    opinion_news = side_news[1]
    cultural_news = side_news[2]

    return render(request, 'AggregatorApp/saved-news.html',
                  {'object_list': object_list, 'popular_news': popular_news, 'opinion_news': opinion_news,
                   'cultural_news': cultural_news})


class SavedNewsDetail(DetailView):
    model = SavedNews
    template_name = 'AggregatorApp/saved-news-detail.html'

    def get_context_data(self, **kwargs):
        context = super(SavedNewsDetail, self).get_context_data(**kwargs)

        popular_tag = get_object_or_404(Tag, slug='ap-top-news')
        popular_news = News.objects.filter(tags__in=[popular_tag])
        cultural_news = News.objects.filter(section='Culture')
        opinion_news = News.objects.filter(section='Opinion')

        if self.request.user:
            try:
                popular_news = remove_blocked_sources(popular_news, self.request.user)
                cultural_news = remove_blocked_sources(cultural_news, self.request.user)
                opinion_news = remove_blocked_sources(opinion_news, self.request.user)
            except:
                print('Invalid User.')

        context['popular_news'] = popular_news
        context['cultural_news'] = cultural_news
        context['opinion_news'] = opinion_news
        return context


@login_required(login_url='/sign-in/')
def saved_news_delete(request, pk):
    sd = SavedNews.objects.get(pk=pk)
    sd.delete()
    return redirect('AggregatorApp:saved-news')


def summarize(request, content):
    text = content
    r = requests.post(
        "https://api.deepai.org/api/summarization",
        data={
            'text': content,
        },
        headers={'api-key': 'quickstart-QUdJIGlzIGNvbWluZy4uLi4K'}
    )

    s = json.loads(r.json())
    summary = s['summary']
    return render(request, 'AggregatorApp/summary.html', {'summary': summary})


def news_detail(request, year, month, day, news_id, pk):
    date_str = str(year) + '-' + str(month) + '-' + str(day)
    d = parse_date(date_str)
    news = get_object_or_404(News, pk=pk, news_id=news_id, date_time=d)

    # related_news = news.tags.similar_objects()
    # print('--------------')
    # print(related_news)

    popular_tag = get_object_or_404(Tag, slug='ap-top-news')
    pn = News.objects.filter(tags__in=[popular_tag])
    on = News.objects.filter(section='Opinion')
    cn = News.objects.filter(section='Culture')
    saved = []

    if request.user:
        try:
            sn = SavedNews.objects.filter(user=request.user)

            for s in sn:
                saved.append(s.url)

            popular_news = remove_blocked_sources(pn, request.user)
            opinion_news = remove_blocked_sources(on, request.user)
            cultural_news = remove_blocked_sources(cn, request.user)
        except:
            popular_news = set(pn)
            opinion_news = set(on)
            cultural_news = set(cn)
            print('Invalid User.')

    if news in popular_news:
        popular_news.discard(news)
    if news in opinion_news:
        opinion_news.discard(news)
    if news in cultural_news:
        cultural_news.discard(news)

    # List of active comments for this post
    comments = news.comments.filter(active=True)

    new_comment = None

    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.user = request.user
            new_comment.news = news
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()
    return render(request, 'AggregatorApp/news-detail.html',
                  {'news': news, 'comments': comments, 'new_comment': new_comment, 'comment_form': comment_form,
                   'popular_news': popular_news, 'opinion_news': opinion_news, 'cultural_news': cultural_news,
                   'saved': saved})


def block_source(request, source):
    url = ''
    if source == 'AP News':
        url = 'https://apnews.com'
    elif source == 'The Guardian':
        url = 'https://www.theguardian.com'
    elif source == 'Reuters':
        url = 'https://www.reuters.com'

    source_block = BlockedSources(user=request.user, source_name=source, source_url=url)
    source_block.save()

    return redirect('AggregatorApp:blocked-sources-list')


@login_required(login_url='/sign-in/')
def blocked_sources_list(request):
    all_sources = News.objects.all()
    sources = []

    for s in all_sources:
        sources.append(s.source)

    sources = set(sources)

    blocked_sources = BlockedSources.objects.filter(user=request.user)
    bs_names = []
    for b in blocked_sources:
        bs_names.append(b.source_name)

    return render(request, 'AggregatorApp/blocked-sources.html',
                  {'sources': sources,'blocked_sources': blocked_sources, 'bs_names': bs_names})


@login_required(login_url='/sign-in/')
def unblock_source(request, pk):
    blocked_source = BlockedSources.objects.get(user=request.user, pk=pk)
    blocked_source.delete()

    return redirect('AggregatorApp:blocked-sources-list')
