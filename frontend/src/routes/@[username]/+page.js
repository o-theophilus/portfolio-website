import { error } from '@sveltejs/kit';
// import { get } from 'svelte/store';
import { memory, loading } from "$lib/store.svelte.js"

export const load = async ({ parent, fetch, url, params }) => {
	// console.log(params)
	let a = await parent();
	// if (!a.locals.user.login && !url.searchParams.has('search')) {
	// 	throw redirect(307, `/?module=login&return_url=${url.pathname}`);
	// }

	// let page_name = "profile"
	// let _state = get(memory)
	// let i = _state.findIndex(x => x.name == page_name);

	// if (i == -1) {
	// 	_state.push({
	// 		name: page_name
	// 	})
	// 	memory.set(_state)
	// }

	let backend = new URL(`${import.meta.env.VITE_BACKEND}/user/${params.username}`)
	// if (url.search) {
	// 	backend.search = url.search
	// } else {
	// 	loading.close()
	// 	return {
	// 		page_name,
	// 		user: a.locals.user
	// 	}
	// }

	let resp = await fetch(`${import.meta.env.VITE_BACKEND}/user/${params.username}`, {
		method: 'get',
		headers: {
			'Content-Type': 'application/json',
			Authorization: a.locals.token
		}
	});
	resp = await resp.json();
	// loading.close()
	// resp.page_name = page_name
	if (resp.status == 200) {
		return resp
	} else {
		throw error(404, resp.error)
	}
}
