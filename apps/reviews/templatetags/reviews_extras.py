from django import template

register = template.Library()


@register.simple_tag
def has_liked(review, user):
    """Return True if the given user liked the review."""
    if not user or not user.is_authenticated:
        return False
    return review.likes.filter(user=user).exists()
