from flask_socketio import Namespace, join_room, emit


class EventManagementNamespace(Namespace):
    @staticmethod
    def on_connect():
        print('connected')

    @staticmethod
    def on_join(data: dict):
        room_id = data.get('room_id')
        join_room(room_id)
        print('join')
        emit('join', {'msg': "join"}, room=room_id)
