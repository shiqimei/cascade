import { initWebsocketClient } from './ws.mjs'
import { userFetch } from './utils/userFetch.mjs'

initWebsocketClient()

async function updateUserProfile() {
    const response = await userFetch('/api/github/user');
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    const { data } = await response.json();
    if (data != null) {
        document.querySelector('.user-profile-avatar').src = data.avatar
        document.querySelector('.user-profile-bio').textContent = data.bio
        document.querySelector('.user-profile-username').textContent = data.username
        document.querySelector('.user-profile-following').textContent = data.following
        document.querySelector('.user-profile-followers').textContent = data.followers
    }
}

async function updateRepos() {
    const start = Date.now()
    const response = await userFetch('/api/github/authorized_repos');
    const { data: repos } = await response.json();
    console.log('[fetch repos] duration: ', Date.now() - start + 'ms')
    console.log('repos: ', repos)
    const select = document.getElementById('repositorySelect');
    document.querySelector('.repos-count').textContent = repos.length
    select.removeChild(select.children[0])
    for (const repo of repos) {
        const option = new Option(repo, repo);
        select.add(option);
    }
}

updateUserProfile()
updateRepos()