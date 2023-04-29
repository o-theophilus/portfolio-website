import { api_url } from '$lib/store.js';

export const load = async ({ fetch, parent }) => {
    const { data } = await parent()

    const resp = await fetch(`${api_url}/post`, {
        method: 'get',
        headers: {
            'Content-Type': 'application/json',
            Authorization: data.locals.token
        },
    });

    if (resp.ok) {
        const data = await resp.json();
        if (data.status == 200) {
            return {
                posts: data.data.posts,
                tags: data.data.tags,
            }
        }
    }
}