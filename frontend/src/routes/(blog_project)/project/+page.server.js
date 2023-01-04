import { api_url } from '$lib/store.js';

export const load = async ({ fetch, url }) => {
    let post_type = url.pathname.split('/')[1];

    const resp = await fetch(`${api_url}/${post_type}`, {
        method: 'get',
        headers: {
            'Content-Type': 'application/json'
        },
    });

    if (resp.ok) {
        const data = await resp.json();
        if (resp.status == 200) {
            return {
                posts: data.data.posts,
                all_tags: data.data.all_tags,
                post_type
            }
        }
    }
}