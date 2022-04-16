document.addEventListener('DOMContentLoaded', () => {

    var socket = io();

    let room = "Lounge";
    joinRoom(room);


    socket.on('incoming-message', data => {
        const table = document.getElementById('#table');
        const tr = document.createElement('tr');
        const p = document.createElement('p');
        const span_username = document.createElement('span');
        const span_timestamp = document.createElement('span');
        const br = document.createElement('br');

        if (data.username == username) {
            // if (document.getElementById('table').row.length < 2)
            p.setAttribute("class", "my-msg");

            span_username.setAttribute("class", "my-username");
            span_username.innerHTML = data.username;

            span_timestamp.setAttribute("class", "timestamp");
            span_timestamp.innerHTML = data.time_stamp;

            p.innerHTML = span_username.outerHTML + br.outerHTML + data.msg + br.outerHTML + span_timestamp.outerHTML;
            document.querySelector('#display-section').append(p);

        } else if (typeof data.username !== 'undefined') {
            p.setAttribute("class", "other-msg");

            span_username.setAttribute("class", "other-username");
            span_username.innerHTML = data.username;

            span_timestamp.setAttribute("class", "timestamp");
            span_timestamp.innerHTML = data.time_stamp;

            p.innerHTML = span_username.outerHTML + br.outerHTML + data.msg + br.outerHTML + span_timestamp.outerHTML;
            document.querySelector('#display-section').append(p);

        } else {
            printSysMsg(data.msg);
        }
        scrollDownChatWindow();
    });

    function scrollDownChatWindow() {
        const chatWindow = document.querySelector("#display-section");
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }

    if (document.querySelector('#send_message')) {
        document.querySelector('#send_message').onclick = () => {
            socket.emit('incoming-message', {
                'msg': document.querySelector('#user_input').value,
                'username': username,
                'isOkay': false,
                'room': room
            });
            console.log(username + " " + room)
            document.querySelector('#user_input').value = '';
        }
    }


    document.querySelector('#create-room').onclick = () => {
        socket.emit('create-room', { 'username': username, 'room': room, 'new_room_name': username })
    }

    socket.on('new-room-received', data => {
        console.log(data);
        let createdRoom = data.new_room_name

        const p = document.createElement('p');
        p.innerHTML = createdRoom
        p.setAttribute('class', 'select-room');
        document.querySelector('#sidebar').append(p);
        if (username == data.username) {
            leaveRoom(room);
            room = createdRoom;
            joinRoom(room);
        }
    })

    document.querySelectorAll('.select-room').forEach(p => {
        p.onclick = () => {
            let newRoom = p.innerHTML;
            if (newRoom == room) {
                msg = `Aktualnie jestes w pokoju ${room}.`
                printSysMsg(msg);
            } else {
                leaveRoom(room);
                room = newRoom;
                joinRoom(room);
            }
        }
    });


    function leaveRoom() {
        socket.emit('leave', { 'username': username, 'room': room });
    }

    function joinRoom() {
        socket.emit('join', { 'username': username, 'room': room });
        document.querySelector('#display-section').innerHTML = ''
    }

    function printSysMsg(msg) {
        const p = document.createElement('p');
        p.innerHTML = msg;
        document.querySelector('#display-section').append(p);
    }

})

