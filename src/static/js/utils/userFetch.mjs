
export async function login() {
    const resp = await fetch('/login')
    return resp.json()
}

export async function userFetch(url, options) {
    const user = await login()
    console.log('[Login Success]', user)

    const headers = new Headers()
    headers.set('Authorization', `Bearer ${user.jwt}`)

    return fetch(url, Object.assign({ headers }, options))
}