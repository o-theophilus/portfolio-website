import { api_url } from '$lib/store.js';

export const load = async ({ fetch, params }) => {
    const resp = await fetch(`${api_url}/tag/${params.slug}`, {
        method: 'get',
        headers: {
            'Content-Type': 'application/json'
        },
    });

    if (resp.ok) {
        const data = await resp.json();

        if (data.status == 200) {
            return {
                blogs: data.data.blogs,
                projects: data.data.projects,
                tags: data.data.tags,
            }
        }
    }

}