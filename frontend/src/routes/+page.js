import { api_url } from '$lib/store.js';

export const load = async ({ fetch }) => {
    const resp = await fetch(`${api_url}/post`, {
        method: 'get',
        headers: {
            'Content-Type': 'application/json'
        },
    });

    if (resp.ok) {
        const data = await resp.json();
        if (resp.status == 200) {
            return {
                blogs: data.data.blogs,
                projects: data.data.projects,
            }
        }
    }
}