from rest_framework import mixins, viewsets, filters

from .permissions import IsAdminOrSuperUser


class DestroyCreateListMixins(mixins.CreateModelMixin,
                              mixins.ListModelMixin,
                              mixins.DestroyModelMixin,
                              viewsets.GenericViewSet):
    """Lля вьюсетов моделей Category и Genre."""
    permission_classes = (IsAdminOrSuperUser,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
