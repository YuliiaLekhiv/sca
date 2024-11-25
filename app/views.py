from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import SpyCat, Mission, Target
from .serializers import SpyCatSerializer, MissionSerializer, TargetSerializer

class SpyCatViewSet(viewsets.ModelViewSet):
    queryset = SpyCat.objects.all()
    serializer_class = SpyCatSerializer

class MissionViewSet(viewsets.ModelViewSet):
    queryset = Mission.objects.all()
    serializer_class = MissionSerializer

    def destroy(self, request, *args, **kwargs):
        mission = self.get_object()
        if mission.cat:
            return Response({"error": "Cannot delete a mission assigned to a cat."}, status=status.HTTP_400_BAD_REQUEST)
        return super().destroy(request, *args, **kwargs)

# app/views.py



class TargetViewSet(viewsets.ModelViewSet):
    queryset = Target.objects.all()
    serializer_class = TargetSerializer

    def update(self, request, *args, **kwargs):
        target = self.get_object()
        if target.complete or (target.mission and target.mission.complete):
            if 'notes' in request.data:
                return Response({"error": "Cannot update notes for a completed target or mission."}, status=status.HTTP_400_BAD_REQUEST)
        return super().update(request, *args, **kwargs)