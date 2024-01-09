import { initWebsocketClient } from './ws.mjs'

export async function login() {
    const resp = await fetch('/login')
    return resp.json()
}

initWebsocketClient()

const user = await login()
console.log('[Login Success]', user)
