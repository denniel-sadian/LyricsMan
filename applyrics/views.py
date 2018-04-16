from django.shortcuts import render
from applyrics.models import Lyrics, Correction, SubmittedLyrics
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import SubmitLyricsForm

context = {'current_year': timezone.now().year}


def index(request):
    try:
        if len(request.GET):
            search = request.GET.get('q')
            one = Lyrics.objects.filter(title__contains=search)
            two = Lyrics.objects.filter(written_by__contains=search)
            three = Lyrics.objects.filter(text__contains=search)
            found = set((list(one) + list(two) + list(three)))
            final_found = sorted(found, key=lambda i: i.title)
            paginator = Paginator(final_found, 10)
            page = request.GET.get('page')
            lyrics_ = paginator.get_page(page)
            context['lyrics'] = lyrics_
            context['letter'] = 'Found'
            context['how_many'] = len(final_found)
        else:
            latest = Lyrics.objects.order_by('-pub_date')[:15]
            context['lyrics'] = latest
            context['letter'] = 'Latest'
            context['how_many'] = len(latest)
        return render(request, 'applyrics/index.html', context)
    except (EmptyPage, PageNotAnInteger):
        return render(request, 'applyrics/404_page.html', context)


def letter_list(request, letter):
    try:
        found = Lyrics.objects.all().filter(
            title__startswith=letter).order_by('title')
        paginator = Paginator(found, 10)
        page = request.GET.get('page')
        lyrics_ = paginator.get_page(page)
        context['lyrics'] = lyrics_
        context['letter'] = letter
        context['how_many'] = len(found)
        context['searched'] = ''
    except (EmptyPage, PageNotAnInteger):
        return render(request, 'applyrics/404_page.html', context)
    return render(request, 'applyrics/index.html', context)


def lyrics(request, letter, pk):
    try:
        found = Lyrics.objects.all().filter(title__startswith=letter)
        one = found.get(pk=pk)
        context['lyrics'] = one
        context['who_corrected'] = ''
        if request.method == 'POST':
            name = request.POST['name']
            correction = request.POST['correction']
            Correction(by=name, date_time=timezone.now(),
                       song_title=one.title, text=correction).save()
            context['who_corrected'] = name
        return render(request, 'applyrics/one.html', context)
    except Lyrics.DoesNotExist:
        return render(request, 'applyrics/404_page.html', context)


def submit(request):
    if request.method == 'POST':
        form = SubmitLyricsForm(request.POST)
        if form.is_valid:
            SubmittedLyrics(
                name=form['name'].value(),
                email=form['email'].value(),
                title=form['title'].value(),
                writer=form['writer'].value(),
                date=form['date'].value(),
                lyrics=form['lyrics'].value(),
                replaced_new_lines=False,
                published=False
            ).save()
            context['who'] = form['name'].value()
            return render(request, 'applyrics/submit.html',
                          context)
    context['who'] = ''
    return render(request, 'applyrics/submit.html', context)
