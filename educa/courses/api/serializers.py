import logging

from rest_framework import serializers

from ..models import Content, Course, Module, Subject

logger = logging.getLogger(__name__)

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'title', 'slug']


class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ['order', 'title', 'description']


class CourseSerializer(serializers.ModelSerializer):
    modules = ModuleSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = [
            'id',
            'subject',
            'title',
            'slug',
            'overview',
            'created',
            'owner',
            'modules',
        ]


class ItemRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        if value is None:
            return None
        render = getattr(value, 'render', None)
        if callable(render):
            try:
                return render()
            except (AttributeError, TypeError, ValueError):
                # render() is expected on content items; fall back to a string
                # representation if it is missing or raises type/value errors from
                # invalid content or templates.
                logger.exception('Failed to render content item %s', value)
                return str(value)
        return str(value)


class ContentSerializer(serializers.ModelSerializer):
    item = ItemRelatedField(read_only=True)

    class Meta:
        model = Content
        fields = ['order', 'item']


class ModuleWithContentsSerializer(ModuleSerializer):
    contents = ContentSerializer(many=True, read_only=True)

    class Meta(ModuleSerializer.Meta):
        fields = ModuleSerializer.Meta.fields + ['contents']


class CourseWithContentsSerializer(CourseSerializer):
    modules = ModuleWithContentsSerializer(many=True, read_only=True)

    class Meta(CourseSerializer.Meta):
        fields = CourseSerializer.Meta.fields
