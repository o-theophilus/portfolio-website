import { api_url } from '$lib/store.js';

export const load = async ({ fetch }) => {
    const resp = await fetch(`${api_url}/tags`, {
        method: 'get',
        headers: {
            'Content-Type': 'application/json'
        },
    });

    if (resp.ok) {
        const data = await resp.json();

        if (data.status == 200) {
            return {
                tags: data.data.tags,
            }
        }
    }

}