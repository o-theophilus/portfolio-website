import { api_url } from '$lib/store.js';

export const load = async ({ fetch, params, parent }) => {
    const { data } = await parent()
    
    const resp = await fetch(`${api_url}/tags/${params.slug}`, {
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