from .models import RunningInsTime
from .handlers import RedisStartClass
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions


class RunningInsTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RunningInsTime
        fields = ['running_ins_name', 'redis_type', 'redis_ip', 'running_ins_port', 'redis_ins_mem'] or '__all__'


@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated,))
def redisstop(request, ins_id):
    running_ins_time = RunningInsTime.objects.all()
    running_ins = running_ins_time.filter(id=ins_id)
    running_ins_name = running_ins.values('running_ins_name').first()
    running_ins_ip = running_ins.values('redis_ip').first()
    running_ins_port = running_ins.values('running_ins_port').first()
    redisins = RedisStartClass(host=running_ins_ip['redis_ip'],
                               redis_server_ctl="/opt/repoll/redis/src/redis-cli -p {0} shutdown".format(running_ins_port['running_ins_port']))
    serializer = RunningInsTimeSerializer(running_ins, many=True)
    result = serializer.data[0]
    if redisins.start_server():
        result['redis_status'] = "DOWN"
        return Response(result)
    result['redis_status'] = "ERROR"
    return Response(result)


@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated,))
def redisstart(request, ins_id):
    running_ins_time = RunningInsTime.objects.all()
    running_ins = running_ins_time.filter(id=ins_id)
    running_ins_name = running_ins.values('running_ins_name').first()
    running_ins_ip = running_ins.values('redis_ip').first()
    running_ins_port = running_ins.values('running_ins_port').first()
    redisins = RedisStartClass(host=running_ins_ip['redis_ip'],
                               redis_server_ctl="/opt/repoll/redis/src/redis-server /opt/repoll/conf/{0}.conf".format(running_ins_port['running_ins_port']))
    serializer = RunningInsTimeSerializer(running_ins, many=True)
    result = serializer.data[0]
    if redisins.start_server():
        result['redis_status'] = "UP"
        return Response(result)
    result['redis_status'] = "ERROR"
    return Response(result)