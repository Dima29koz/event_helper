document.addEventListener('DOMContentLoaded', () => {
    console.log('start');
    const room_id = 1

    // Connect to websocket
    let socket = io('/event_management');
    //let socket = io(location.protocol + '//' + document.domain + ':' + location.port + '/game_room');
    socket.on('connect', () => {
        console.log('connect');
        socket.emit('join', {'room_id': room_id});
    });

    socket.on('join', data => {
        console.log(data);
    });
});