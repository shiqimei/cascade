export function initWebsocketClient() {
    const socket = io.connect('/ws')

    socket.on('connect', () => {
        console.log('[ws] Connected to the server');
        socket.emit('message', 'Hello from the client!');
    });

    socket.on('message', (msg) => {
        console.log('Received message:', msg)
    })
}