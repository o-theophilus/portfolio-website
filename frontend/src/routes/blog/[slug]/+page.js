import { api_url } from '$lib/store.js';

export const load = async ({ fetch, url, params }) => {
    let type = url.pathname.split('/')[1];

    const resp = await fetch(`${api_url}/${type}/${params.slug}`, {
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
                comments: data.data.comments,
                ratings: data.data.ratings
            }
        }
    }
}