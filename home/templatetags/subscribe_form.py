from django import template
from home.models import SubscribeFormSettings

register = template.Library()
# https://docs.djangoproject.com/en/4.2/howto/custom-template-tags/


@register.simple_tag(takes_context=True)
def get_subscribe_form(context):
    request = context['request']
    subscribe_form_settings = SubscribeFormSettings.for_request(request)
    subscribe_form_page = subscribe_form_settings.subscribe_form_page.specific
    form = subscribe_form_page.get_form(
        page=subscribe_form_page, user=request.user)
    return {'page': subscribe_form_page, 'form': form}