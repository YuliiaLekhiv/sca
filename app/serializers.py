from rest_framework import serializers
from .models import SpyCat, Mission, Target

class SpyCatSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpyCat
        fields = '__all__'

    def update(self, instance, validated_data):
        if 'salary' in validated_data and len(validated_data) == 1:
            instance.salary = validated_data.get('salary', instance.salary)
            instance.save()
            return instance
        else:
            raise serializers.ValidationError("Only the salary field can be updated.")




class TargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Target
        fields = ['id', 'name', 'country', 'notes', 'complete', 'breed', 'mission']

    def update(self, instance, validated_data):
        if instance.complete or (instance.mission and instance.mission.complete):
            if 'notes' in validated_data:
                raise serializers.ValidationError("Cannot update notes for a completed target or mission.")
        return super().update(instance, validated_data)

class MissionSerializer(serializers.ModelSerializer):
    targets = serializers.PrimaryKeyRelatedField(queryset=Target.objects.all(), many=True)

    class Meta:
        model = Mission
        fields = ['id', 'cat', 'complete', 'targets']

    def validate_targets(self, value):
        for target in value:
            if target.mission is not None:
                raise serializers.ValidationError(f"Target {target.id} is already assigned to another mission.")
        return value

    def create(self, validated_data):
        targets_data = validated_data.pop('targets')
        mission = Mission.objects.create(**validated_data)
        mission.targets.set(targets_data)
        return mission