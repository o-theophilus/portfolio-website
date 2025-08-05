import { error } from '@sveltejs/kit';
import { get } from 'svelte/store';
import { memory, loading } from "$lib/store.svelte.js"

export const load = async ({ fetch, url, parent }) => {
	let a = await parent();
	if (!a.locals.user.access.includes("user:view")) {
		throw error(400, "unauthorized access")
	}

	let page_name = "users"
	let _state = get(memory)
	let i = _state.findIndex(x => x.name == page_name);

	if (i == -1) {
		_state.push({
			name: page_name,
			search: url.search
		})
		memory.set(_state)
		i = _state.findIndex(x => x.name == page_name);
	}

	let backend = new URL(`${import.meta.env.VITE_BACKEND}/users`)
	backend.search = _state[i].search
	let resp = await fetch(backend.href, {
		method: 'get',
		headers: {
			'Content-Type': 'application/json',
			Authorization: a.locals.token
		}
	});
	resp = await resp.json();
	loading.close()

	if (resp.status == 200) {
		resp.page_name = page_name
		return resp
	}
}