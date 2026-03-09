import { app } from "$lib/store.svelte.js";
import { error } from '@sveltejs/kit';

export const load = async ({ fetch, params, parent }) => {
    if (app.post.slug == params.slug) return { post: app.post }

    let a = await parent();
    let resp = await fetch(`${import.meta.env.VITE_BACKEND}/posts/${params.slug}`, {
        headers: {
            'Content-Type': 'application/json',
            Authorization: a.locals.token
        },
    });
    resp = await resp.json();

    if (resp.status == 200) {
        return resp
    } else {
        throw error(resp.status, resp.error)
    }
}