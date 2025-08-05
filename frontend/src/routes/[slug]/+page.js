import { get } from 'svelte/store';
import { error } from '@sveltejs/kit';
import { memory } from "$lib/store.svelte.js"

export const load = async ({ fetch, params, parent }) => {
    let _state = get(memory)
    let i = _state.findIndex(x => x.name == "post_item");
    if (i != -1 && _state[i].data.slug == params.slug) {
        return { post: _state[i].data }
    }

    let a = await parent();
    let resp = await fetch(`${import.meta.env.VITE_BACKEND}/post/${params.slug}`, {
        method: 'get',
        headers: {
            'Content-Type': 'application/json',
            Authorization: a.locals.token
        },
    });
    resp = await resp.json();

    if (resp.status == 200) {
        return { ...resp }
    } else {
        throw error(404, "page not found")
    }
}