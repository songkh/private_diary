import logging
from django.views import generic
from .forms import InquiryForm
from .forms import DiaryCreateForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Diary

# logger
logger = logging.getLogger(__name__)

# Index.html
class IndexView(generic.TemplateView):
    template_name = "index.html"

# Inquiry.html
class InquiryView(generic.FormView):
    template_name = "inquiry.html"
    form_class = InquiryForm
    success_url = reverse_lazy('diary:inquiry')

    def form_valid(self, form):
        form.send_email()
        messages.success(self.request, 'メッセージを送信しました。')
        logger.info('Inquiry sent by {}'.format(form.cleaned_data['name']))
        return super().form_valid(form)

# Diary_list.html
class DiaryListView(LoginRequiredMixin, generic.ListView):
    model = Diary
    template_name = 'diary_list.html'
    paginate_by = 2

    def get_queryset(self):
        diaries = Diary.objects.filter(user=self.request.user).order_by('-created_at')
        return diaries

# Diary_detail.html
class DiaryDetailView(LoginRequiredMixin, generic.DetailView):
    model = Diary
    template_name = 'diary_detail.html'
    #pk_url_kwarg = 'id'

# Diary_create.html
class DiaryCreateView(LoginRequiredMixin, generic.CreateView):
    model = Diary
    template_name = 'diary_create.html'
    form_class = DiaryCreateForm
    success_url = reverse_lazy('diary:diary_list')

    def form_valid(self, form):
        diary = form.save(commit=False)
        diary.user = self.request.user
        diary.save()
        messages.success(self.request, '日記を作成しました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.success(self.request, '日記の作成に失敗しました。')
        return super().form_invalid(form)

# Diary_update.html
class DiaryUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Diary
    template_name = 'diary_update.html'
    form_class = DiaryCreateForm

    def get_success_url(self):
        return reverse_lazy('diary:diary_detail', kwargs={'pk':self.kwargs['pk']})

    def form_valid(self, form):
        messages.success(self.request, '日記を更新しました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.success(self.request, '日記の更新に失敗しました。')
        return super().form_invalid(form)

# Diary_delete.html
class DiaryDeleteView(LoginRequiredMixin, generic.DetailView):
    model = Diary
    template_name = 'diary_delete.html'
    success_url = reverse_lazy('diary:diray_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, '日記を削除しました。')
        return super().delete(request, *args, **kwargs)