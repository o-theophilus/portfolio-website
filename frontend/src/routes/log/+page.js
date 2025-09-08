import { page_state, loading } from "$lib/store.svelte.js"
import { error } from "@sveltejs/kit";

export const load = async ({ fetch, url, parent, depends }) => {
	let a = await parent();
	if (!a.locals.login || !a.locals.user.access.includes('log:view')) {
		throw error(400, "Unauthorized access")
	}

	depends(true)

	let page_name = "logs"
	if (!page_state.state[page_name]) {
		let sp = {}
		for (let [key, value] of url.searchParams) {
			sp[key] = value
		}
		page_state.state[page_name] = {
			searchParams: sp,
			data: [],
			loaded: false
		}
	} else if (page_state.state[page_name].loaded) {
		return page_state.state[page_name].data
	}

	let backend = new URL(`${import.meta.env.VITE_BACKEND}/log`)
	backend.search = new URLSearchParams(page_state.state[page_name].searchParams);
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
		page_state.state[page_name].data = resp
		page_state.state[page_name].loaded = true

		return resp
	} else {
		throw error(resp.status, resp.error)
	}
}