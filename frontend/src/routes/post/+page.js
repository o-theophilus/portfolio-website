import { get } from 'svelte/store';
import { state, loading } from "$lib/store.js"


export const load = async ({ fetch, url, parent, depends }) => {
	let page_name = "post"
	let _state = get(state)
	let i = _state.findIndex(x => x.name == page_name);

	if (i == -1) {
		_state.push({
			name: page_name,
			search: url.search,
			data: [],
			loaded: false
		})
		state.set(_state)
		i = _state.findIndex(x => x.name == page_name);
	} else if (_state[i].loaded) {
		depends(_state[i].search)
		return _state[i].data
	}

	// loading.set(true)
	let backend = new URL(`${import.meta.env.VITE_BACKEND}/post`)
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

		_state[i].data = resp
		_state[i].loaded = true
		state.set(_state)

		return resp
	}
}
