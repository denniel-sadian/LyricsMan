from django.contrib import admin
from . import models
from django.core.mail import send_mail
from threading import Thread


def delete_all(modeladmin, request, queryset):
    if queryset.count() > 0:
        deleted = 0
        for i in queryset:
            i.delete()
            deleted += 1
        modeladmin.message_user(
            request, f'{deleted} item{" has" if deleted is 1 else "s have"} '
                     'been deleted.')


delete_all.short_description = 'Delete all selected'


class LyricsAdmin(admin.ModelAdmin):
    list_display = ('title', 'written_by', 'pub_date', 'replaced_new_lines',
                    'id')
    actions = ['replace_new_lines_with_br_tag', 'remove_br_tags', delete_all]

    def replace_new_lines_with_br_tag(self, request, queryset):
        if queryset.count() > 0:
            replaced = 0
            for i in queryset:
                if not i.replaced_new_lines:
                    lines = i.text.strip().split('\n')
                    for line in lines:
                        lines[lines.index(line)] = f'{line.strip()} <br/>'
                    i.text = '\n'.join(lines)
                    i.replaced_new_lines = True
                    i.save()
                    replaced += 1
            if replaced:
                self.message_user(
                    request, f'{replaced} song lyrics '
                             f'{"has" if replaced is 1 else "have"} '
                             'been altered.')
            else:
                self.message_user(request,
                                  'Their new lines were replaced already.')

    def remove_br_tags(self, request, queryset):
        if queryset.count() > 0:
            replaced = 0
            for i in queryset:
                if i.replaced_new_lines:
                    lines = i.text.strip().split('\n')
                    for line in lines:
                        lines[lines.index(line)] = \
                            line.strip().replace('<br/>', '')
                    i.text = '\n'.join(lines)
                    i.replaced_new_lines = False
                    i.save()
                    replaced += 1
            if replaced:
                self.message_user(
                    request, f'{replaced} song lyrics '
                             f'{"has" if replaced is 1 else "have"} '
                             'been altered.')
            else:
                self.message_user(
                    request, 'Their <br/> tags were replaced already.')

    remove_br_tags.short_description = 'Remove <br/> tags'
    replace_new_lines_with_br_tag.short_description = \
        'Replace new lines with <br/> tag'


class CorrectionAdmin(admin.ModelAdmin):
    list_display = ('by', 'song_title', 'date_time', 'pk')
    actions = [delete_all]


class SubmittedLyricsAdmin(admin.ModelAdmin):
    list_display = ('title', 'email', 'name', 'date', 'replaced_new_lines',
                    'published')
    actions = ['replace_new_lines_with_br_tag', 'publish', delete_all]

    def replace_new_lines_with_br_tag(self, request, queryset):
        if queryset.count() > 0:
            replaced = 0
            for i in queryset:
                if not i.replaced_new_lines:
                    lines = i.lyrics.strip().split('\n')
                    for line in lines:
                        lines[lines.index(line)] = f'{line.strip()}<br/>'
                    i.lyrics = '\n'.join(lines)
                    i.replaced_new_lines = True
                    i.save()
                    replaced += 1
            if replaced:
                self.message_user(
                    request, f'{replaced} submitted lyrics '
                             f'{"has" if replaced is 1 else "have"} '
                             'been altered.')
            else:
                self.message_user(
                    request, 'Their new lines were replaced already.')

    def publish(self, request, queryset):
        if queryset.count() > 0:
            published = 0
            for i in queryset:
                if i.replaced_new_lines and not i.published:
                    models.Lyrics(
                        title=i.title,
                        pub_date=i.date,
                        text=i.lyrics,
                        written_by=i.writer,
                        remarks='You can submit a correction if something '
                                'is wrong with the lyrics.',
                        replaced_new_lines=True,
                    ).save()
                    print('here - ' * 20)
                    i.published = True
                    i.save()
                    published += 1
                    Thread(target=send_mail, args=(
                        'Published',
                        f'Good day, {i.name}! Your submitted song lyrics in '
                        'LyricsMan.com has been published now. '
                        'Thanks for submitting, feel free to submit again.',
                        'sadiandenniel@gmail.com', [i.email], True)
                           ).start()
            if published > 0:
                self.message_user(
                    request, f'{published} submitted lyrics '
                             f'{"has" if published is 1 else "have"} '
                             'been published.')
            else:
                self.message_user(request, 'None has been published.')

    publish.short_description = 'Publish selected'
    replace_new_lines_with_br_tag.short_description = \
        'Replace new lines with <br/> tag'


admin.site.register(models.Lyrics, LyricsAdmin)
admin.site.register(models.Correction, CorrectionAdmin)
admin.site.register(models.SubmittedLyrics, SubmittedLyricsAdmin)
