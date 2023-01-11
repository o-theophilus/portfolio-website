import { api_url } from '$lib/store.js';

export const load = async ({ fetch, params }) => {
    const resp = await fetch(`${api_url}/tag`, {
        method: 'get',
        headers: {
            'Content-Type': 'application/json'
        },
    });

    if (resp.ok) {
        const data = await resp.json();

        if (resp.status == 200) {
            return {
                tags: data.data.tags,
            }
        }
    }

}