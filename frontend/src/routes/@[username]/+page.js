import { error } from '@sveltejs/kit';
import { loading } from "$lib/store.svelte.js"

export const load = async ({ parent, fetch, params }) => {
	let a = await parent();
	if (a.locals.user.key == params.username) {
		return { user: a.locals.user }
	}

	let resp = await fetch(`${import.meta.env.VITE_BACKEND}/user/${params.username}`, {
		method: 'get',
		headers: {
			'Content-Type': 'application/json',
			Authorization: a.locals.token
		}
	});
	resp = await resp.json();
	if (resp.status == 200) {
		return resp
	} else {
		throw error(resp.status, resp.error)
	}
}
