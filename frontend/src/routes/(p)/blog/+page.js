import { api_url } from '$lib/store.js';

export const load = async ({ fetch, url, parent }) => {
    const { data } = await parent()
    let post_type = url.pathname.split('/')[1];

    const resp = await fetch(`${api_url}/${post_type}`, {
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
                post_type
            }
        }
    }
}