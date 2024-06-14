import { get } from 'svelte/store';
import { state, loading } from "$lib/store.js"

export const load = async ({ fetch, url, parent }) => {

	let page_name = "logs"
	let _state = get(state)
	let i = _state.findIndex(x => x.name == page_name);

	if (i == -1) {
		_state.push({
			name: page_name,
			search: url.search
		})
		state.set(_state)
		i = _state.findIndex(x => x.name == page_name);
	}

	let backend = new URL(`${import.meta.env.VITE_BACKEND}/log`)
	backend.search = _state[i].search
	let a = await parent();
	let resp = await fetch(backend.href, {
		method: 'get',
		headers: {
			'Content-Type': 'application/json',
			Authorization: a.locals.token
		}
	});
	resp = await resp.json();
	loading.set(false)

	if (resp.status == 200) {
		resp.page_name = page_name
		return resp
	}
}