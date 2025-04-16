import { redirect } from '@sveltejs/kit';
import { get } from 'svelte/store';
import { state, loading } from "$lib/store.js"

export const load = async ({ parent, fetch, url }) => {
	let a = await parent();
	if (!a.locals.user.login && !url.searchParams.has('search')) {
		throw redirect(307, `/?module=login&return_url=${url.pathname}`);
	}

	let page_name = "profile"
	let _state = get(state)
	let i = _state.findIndex(x => x.name == page_name);

	if (i == -1) {
		_state.push({
			name: page_name
		})
		state.set(_state)
	}

	let backend = new URL(`${import.meta.env.VITE_BACKEND}/user`)
	if (url.search) {
		backend.search = url.search
	} else {
		loading.set(false)
		return {
			page_name,
			user: a.locals.user
		}
	}

	let resp = await fetch(backend.href, {
		method: 'get',
		headers: {
			'Content-Type': 'application/json',
			Authorization: a.locals.token
		}
	});
	resp = await resp.json();
	loading.set(false)
	resp.page_name = page_name
	return resp
}
