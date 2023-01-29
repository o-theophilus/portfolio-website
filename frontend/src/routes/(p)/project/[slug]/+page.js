import { api_url } from '$lib/store.js';

export const load = async ({ fetch, url, params }) => {
    let post_type = url.pathname.split('/')[1];

    const resp = await fetch(`${api_url}/${post_type}/${params.slug}`, {
        method: 'get',
        headers: {
            'Content-Type': 'application/json'
        },
    });

    if (resp.ok) {
        const data = await resp.json();

        if (data.status == 200) {
            return {
                post: data.data.post,
                tags: data.data.tags,
                post_type
            }
        }
    }
}