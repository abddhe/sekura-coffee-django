const websocketSchema = location.protocol === "https" ? 'wss' : 'ws';
const websocketUrl = `${websocketSchema}://${location.host}/`

class NotificationWebsocket {
    constructor(websocketUrl) {
        this.url = websocketUrl + 'test'
        this.websocket = new WebSocket(this.url)
        this.onConnect()
        this.onDisconnect()
        this.onMessaging()
    }

    onConnect() {
        this.websocket.onopen=function (ev) {
            console.log('Goo')
        }
    }

    onDisconnect(){
        this.websocket.onclose = function (ev){
            console.warn("Down")
        }
    }
    onMessaging(){
        this.websocket.onmessage = function (ev){
            new Notification(JSON.parse(ev.data))
        }
    }
}


export {NotificationWebsocket, websocketUrl}