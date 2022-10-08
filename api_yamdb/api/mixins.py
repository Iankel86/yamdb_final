from rest_framework import mixins, viewsets


class CreateListDestroyViewSet(mixins.CreateModelMixin,
                               mixins.ListModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    """Кастомный миксин для создания и удаления объектов, получения списка."""
    pass
