from rest_framework import serializers
from .models import MockupImage, MockupRequest

VALID_COLORS = ("white", "black", "blue", "yellow")

class MockupGenerateSerializer(serializers.Serializer):
    text = serializers.CharField()
    font = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    text_color = serializers.RegexField(
        r"^#(?:[0-9a-fA-F]{3}){1,2}$",
        required=False,
        allow_null=True
    )
    shirt_color = serializers.ListField(
        child=serializers.ChoiceField(choices=VALID_COLORS),
        required=False
    )

    def create(self, validated_data):
        colors = validated_data.pop("shirt_color", None)
        return MockupRequest.objects.create(
            text=validated_data.get("text"),
            font=validated_data.get("font"),
            text_color=validated_data.get("text_color"),
            shirt_colors=list(colors) if colors else list(VALID_COLORS),
        )

class MockupImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = MockupImage
        fields = ("image_url", "shirt_color", "created_at")

    def get_image_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.image.url)
