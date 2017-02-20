from django.http import Http404, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from mongoengine import ImproperlyConfigured, DoesNotExist
from global_utils.code import Results

from django.views.generic import View
from global_utils.http import JsonResponse


class MongoListView(View):
    document = None
    queryset = None
    initial = {}

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(MongoListView, self).dispatch(request, *args, **kwargs)


    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        result = []
        for row in self.object_list:
            value = row.to_mongo().to_dict()
            value.pop('_id')
            result.append(value)
        return JsonResponse(Results().succss_result(result))

    def post(self, request, *args, **kwargs):
        self.object = None
        results = self.get_form_kwargs().get('data').dict()
        res = self.document(**results)
        res.save()
        return HttpResponseRedirect(res.get_absolute_url())

    def get_queryset(self):
        """
        Get the list of items for this view. This must be an interable, and may
        be a queryset (in which qs-specific behavior will be enabled).
        """
        if self.queryset is not None:
            queryset = self.queryset
            queryset = queryset.clone()
        elif self.document is not None:
            queryset = self.document.objects()
        else:
            raise ImproperlyConfigured("'%s' must define 'queryset' or 'document'"
                                       % self.__class__.__name__)
        return queryset

    def get_initial(self):
        """
        Returns the initial data to use for forms on this view.
        """
        return self.initial.copy()

    def get_form_kwargs(self):
        """
        Returns the keyword arguments for instanciating the form.
        """
        kwargs = {'initial': self.get_initial()}
        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        kwargs.update({'instance': self.object})
        return kwargs


class MongoObjectView(MongoListView):
    document = None
    slug_url_kwarg = 'slug'
    pk_url_kwarg = 'pk'
    slug_field = 'slug'

    def get(self, request, **kwargs):
        self.object = self.get_object()
        result = self.object.to_mongo().to_dict()
        result.pop('_id')
        return JsonResponse(Results().succss_result(result))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        old_results = self.object.to_mongo().to_dict()
        new_results = self.get_form_kwargs().get('data').dict()
        results=dict(old_results.items()+new_results.items())
        res = self.document(**results)
        res.save()
        self.object.delete()
        return HttpResponseRedirect(res.get_absolute_url())


    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        # return HttpResponseRedirect(self.object.delete_success_url())
        return JsonResponse(Results().succss_result())

    def get_object(self, queryset=None):
        """
        Returns the object the view is displaying.

        By default this requires `self.queryset` and a `pk` or `slug` argument
        in the URLconf, but subclasses can override this to return any object.
        """
        # Use a custom queryset if provided; this is required for subclasses
        # like DateDetailView
        if queryset is None:
            queryset = self.get_queryset()

        # Next, try looking up by primary key.
        pk = self.kwargs.get(self.pk_url_kwarg, None)
        slug = self.kwargs.get(self.slug_url_kwarg, None)
        if pk is not None:
            queryset = queryset.filter(pk=pk)

        # Next, try looking up by slug.
        elif slug is not None:
            slug_field = self.get_slug_field()
            queryset = queryset.filter(**{slug_field: slug})

        # If none of those are defined, it's an error.
        else:
            raise AttributeError("Generic detail view %s must be called with "
                                 "either an object pk or a slug."
                                 % self.__class__.__name__)

        try:
            obj = queryset.get()
        except DoesNotExist:
            raise Http404
            # opts = get_document_options(queryset._document)
            # raise Http404(("No %(verbose_name)s found matching the query") %
            #               {'verbose_name': opts.verbose_name})
        return obj

    def get_slug_field(self):
        """
        Get the name of a slug field to be used to look up by slug.
        """
        return self.slug_field
