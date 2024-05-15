from django.db import models
from wagtail.fields import RichTextField
from wagtail.models import Page
from django.shortcuts import render
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail.admin.panels import FieldPanel, InlinePanel, FieldRowPanel, MultiFieldPanel, PageChooserPanel
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.snippets.models import register_snippet
from modelcluster.fields import ParentalKey
from wagtail.contrib.forms.panels import FormSubmissionsPanel
from cloudinary.models import CloudinaryField
from shop.models import Category, Cart


class HomePage(Page):
    template = 'shop/shop.html'
    max_count = 1

    content_panels = Page.content_panels + [
        # FieldPanel('hero_section_title'),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super(HomePage, self).get_context(request, *args, **kwargs)

        # context["daily_devotions"] = daily_devotions
        return context


class SubscribeFormField(AbstractFormField):
    page = ParentalKey('SubscribeFormPage', on_delete=models.CASCADE, related_name='form_fields')

class SubscribeFormPage(AbstractEmailForm):
    template = 'home/subscribe_form.html'
    intro = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)
    content_panels = AbstractEmailForm.content_panels + [
        FormSubmissionsPanel(),
        FieldPanel('intro'),
        InlinePanel('form_fields', label="Form fields"),
        FieldPanel('thank_you_text'),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel('subject'),
        ], "Email"),
    ]

    def serve(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = self.get_form(request.POST, page=self, user=request.user)

            if form.is_valid():
                self.process_form_submission(form)
                
                # Update the original landing page context with other data
                landing_page_context = self.get_context(request)
                landing_page_context['email'] = form.cleaned_data['email']

                return render(
                    request,
                    self.get_landing_page_template(request),
                    landing_page_context
                )
        else:
            form = self.get_form(page=self, user=request.user)

        context = self.get_context(request)
        context['form'] = form
        return render(
            request,
            self.get_template(request),
            context
        )

@register_setting
class SubscribeFormSettings(BaseSiteSetting):
    subscribe_form_page = models.ForeignKey(
        'wagtailcore.Page', null=True, on_delete=models.SET_NULL)

    panels = [
        # note the page type declared within the pagechooserpanel
        PageChooserPanel('subscribe_form_page', ['home.SubscribeFormPage']),
    ]

@register_snippet
class OurValues(models.Model):
    value_title = models.CharField(max_length=500, null=True, blank=True)
    value_text = RichTextField(null=True, blank=True)
    value_image = CloudinaryField("image", null=True, blank=True, help_text="upload image")

    panels = [
        FieldPanel('value_title'),
        FieldPanel('value_text'),
        FieldPanel('value_image'),
    ]
    def __str__(self):
        return self.value_title
    
    class Meta:
        verbose_name_plural = "Our Values"

@register_snippet
class TrustedBy(models.Model):
    organization_name = models.CharField(max_length=500, null=True, blank=True)
    logo = CloudinaryField("image", null=True, blank=True, help_text="upload logo of trusted-by companies/businesses")

    panels = [
        FieldPanel('organization_name'),
        FieldPanel('logo'),
    ]
    def __str__(self):
        return self.organization_name
    
    class Meta:
        verbose_name_plural = "Trusted By Businesses"

@register_snippet
class Team(models.Model):
    full_name = models.CharField(max_length=500, null=True, blank=True)
    position = models.URLField(null=True, blank=True)
    photo = CloudinaryField("image", null=True, blank=True, help_text="upload photo")
    facebook = models.URLField(null=True, blank=True)
    twitter = models.URLField(null=True, blank=True)
    instagram = models.URLField(null=True, blank=True)
    linkedin = models.URLField(null=True, blank=True)
    whatsapp = models.URLField(null=True, blank=True)

    panels = [
        FieldPanel('full_name'),
        FieldPanel('position'),
        FieldPanel('photo'),
        FieldPanel('facebook'),
        FieldPanel('twitter'),
        FieldPanel('instagram'),
        FieldPanel('linkedin'),
        FieldPanel('whatsapp'),
    ]
    def __str__(self):
        return self.full_name
    
    class Meta:
        verbose_name_plural = "Teams"
    
class About(Page):
    max_count = 1
    template = 'home/about.html'
    welcome_to_tabitha_title = models.CharField(max_length=1000, null=True, blank=True)
    welcome_to_tabitha_text = RichTextField(null=True, blank=True)
    our_mission_title = models.CharField(max_length=1000, null=True, blank=True)
    our_mission_text = RichTextField(null=True, blank=True)
    our_mission_image = CloudinaryField("image", null=True, blank=True, help_text="upload image for Mission section")
    our_story_title = models.CharField(max_length=1000, null=True, blank=True)
    our_story_text = RichTextField(null=True, blank=True)
    our_story_image1 = CloudinaryField("image", null=True, blank=True, help_text="upload first for Story section")
    our_story_image2 = CloudinaryField("image", null=True, blank=True, help_text="upload second for Story section")

    content_panels = Page.content_panels + [
        FieldPanel('welcome_to_tabitha_title'),
        FieldPanel('welcome_to_tabitha_text'),
        FieldPanel('our_mission_title'),
        FieldPanel('our_mission_text'),
        FieldPanel('our_mission_image'),
        FieldPanel('our_story_title'),
        FieldPanel('our_story_text'),
        FieldPanel('our_story_image1'),
        FieldPanel('our_story_image2'),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super(About, self).get_context(request, *args, **kwargs)

        categories = Category.objects.all()
        if request.user.is_authenticated:
            cart = Cart.objects.get_or_create(user=request.user)[0]
            cart_items = cart.cartitem_set.all()
            context['cart_items'] = cart_items
        else:
            cart = None

        values = OurValues.objects.all()
        teams = Team.objects.all()
        trusted_by_companies = TrustedBy.objects.all()

        # context['cart_items'] = cart_items
        context['categories'] = categories
        context['values'] = values
        context['teams'] = teams
        # context['cart'] = cart
        context['trusted_by_companies'] = trusted_by_companies
        return context

@register_setting
class SiteSocial(BaseSiteSetting):
    facebook = models.URLField(max_length=500, null=True, blank=True)
    twitter = models.URLField(max_length=500, null=True, blank=True)
    instagram = models.URLField(max_length=500, null=True, blank=True)
    threads = models.URLField(max_length=500, null=True, blank=True)
    linkedin = models.URLField(max_length=500, null=True, blank=True)
    youtube = models.URLField(max_length=500, null=True, blank=True)
    tiktok = models.URLField(max_length=500, null=True, blank=True)


@register_setting
class SiteContact(BaseSiteSetting):
    email1 = models.EmailField(help_text='Your Email address', null=True, blank=True)
    address = models.CharField(max_length=500, null=True, blank=True)
    phone2 = models.CharField(max_length=500, null=True, blank=True)
    google_map_url  = models.URLField(max_length=1000, null=True, blank=True, help_text="Enter the google map iframe embed src link")

@register_setting
class SiteLogo(BaseSiteSetting):
    logo = CloudinaryField("image", null=True, blank=True, help_text="Upload site logo")

@register_setting
class ImportantPages(BaseSiteSetting):
    # Fetch these pages when looking up ImportantPages for or a site
    select_related = ["about", "home", "contact"]

    about = models.ForeignKey(
        'wagtailcore.Page', null=True, on_delete=models.SET_NULL, related_name='+')
    home = models.ForeignKey(
        'wagtailcore.Page', null=True, on_delete=models.SET_NULL, related_name='+')
    contact = models.ForeignKey(
        'wagtailcore.Page', null=True, on_delete=models.SET_NULL, related_name='+')
    panels = [
        PageChooserPanel('about', ['home.About']),
        PageChooserPanel('home', ['home.HomePage']),
        PageChooserPanel('contact', ['home.ContactFormPage']),
    ]

class ContactFormField(AbstractFormField):
    page = ParentalKey('ContactFormPage', on_delete=models.CASCADE, related_name='form_fields')

class ContactFormPage(AbstractEmailForm):
    template = 'home/contact.html'
    intro = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)
    content_panels = AbstractEmailForm.content_panels + [
        FormSubmissionsPanel(),
        FieldPanel('intro'),
        InlinePanel('form_fields', label="Form fields"),
        FieldPanel('thank_you_text'),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel('subject'),
        ], "Email"),
    ]

    def serve(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = self.get_form(request.POST, page=self, user=request.user)

            if form.is_valid():
                self.process_form_submission(form)
                
                # Update the original landing page context with other data
                landing_page_context = self.get_context(request)
                landing_page_context['email'] = form.cleaned_data['email']

                return render(
                    request,
                    self.get_landing_page_template(request),
                    landing_page_context
                )
        else:
            form = self.get_form(page=self, user=request.user)

        context = self.get_context(request)
        context['form'] = form
        return render(
            request,
            self.get_template(request),
            context
        )
    
    def get_context(self, request, *args, **kwargs):
        context = super(ContactFormPage, self).get_context(request, *args, **kwargs)

        categories = Category.objects.all()
        if request.user.is_authenticated:
            cart = Cart.objects.get_or_create(user=request.user)[0]
            cart_items = cart.cartitem_set.all()
            context['cart_items'] = cart_items
            context['cart'] = cart
        else:
            cart = None
        context['categories'] = categories
        return context
    
@register_setting
class ContactFormSettings(BaseSiteSetting):
    contact_form_page = models.ForeignKey(
        'wagtailcore.Page', null=True, on_delete=models.SET_NULL)

    panels = [
        # note the page type declared within the pagechooserpanel
        PageChooserPanel('contact_form_page', ['home.ContactFormPage']),
    ]