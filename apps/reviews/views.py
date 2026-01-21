from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from apps.movies.models import Movie
from .models import Review, ReviewLike
from .forms import ReviewForm


class AddReviewView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/add_review.html'
    
    def get(self, request, *args, **kwargs):
        movie_id = self.kwargs.get('pk')
        existing_review = Review.objects.filter(user=request.user, movie_id=movie_id).first()
        if existing_review:
            return redirect('reviews:edit_review', review_pk=existing_review.pk)
        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        movie_id = self.kwargs.get('pk')
        context['movie'] = get_object_or_404(Movie, pk=movie_id)
        return context
    
    def form_valid(self, form):
        movie_id = self.kwargs.get('pk')
        movie = get_object_or_404(Movie, pk=movie_id)
        form.instance.user = self.request.user
        form.instance.movie = movie
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('movies:movie_info', kwargs={'pk': self.object.movie.pk})


class EditReviewView(UserPassesTestMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/edit_review.html'
    pk_url_kwarg = 'review_pk'
    
    def test_func(self):
        review = self.get_object()
        return review.user == self.request.user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['movie'] = self.object.movie
        return context
    
    def get_success_url(self):
        return reverse_lazy('movies:movie_info', kwargs={'pk': self.object.movie.pk})


class DeleteReviewView(UserPassesTestMixin, DeleteView):
    model = Review
    template_name = 'reviews/review_confirm_delete.html'
    pk_url_kwarg = 'review_pk'
    
    def test_func(self):
        review = self.get_object()
        return review.user == self.request.user
    
    def get_success_url(self):
        return reverse_lazy('movies:movie_info', kwargs={'pk': self.object.movie.pk})


class UserReviewsListView(LoginRequiredMixin, ListView):
    model = Review
    template_name = 'reviews/reviews_list.html'
    context_object_name = 'reviews'
    paginate_by = 9
    login_url = 'login'
    
    def get_queryset(self):
        return Review.objects.filter(user=self.request.user).select_related('movie', 'user').prefetch_related('likes')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'My Reviews'
        return context


class ToggleReviewLikeView(LoginRequiredMixin, View):
    """Toggle like/unlike on a review for the current user."""

    def post(self, request, *args, **kwargs):
        review = get_object_or_404(Review, pk=kwargs.get('review_pk'))
        like_qs = ReviewLike.objects.filter(review=review, user=request.user)

        if like_qs.exists():
            like_qs.delete()
        else:
            ReviewLike.objects.create(review=review, user=request.user)

        return HttpResponseRedirect(request.META.get('HTTP_REFERER') or reverse_lazy('reviews:reviews_list'))
