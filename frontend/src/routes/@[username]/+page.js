import { error } from '@sveltejs/kit';

export const load = async ({ parent, fetch, params }) => {
	let a = await parent();
	if (a.locals.user.key == params.username) {
		return { user: a.locals.user }
	}

	let response = await fetch(`${import.meta.env.VITE_BACKEND}/users/${params.username}`, {
		method: 'get',
		headers: {
			'Content-Type': 'application/json',
			Authorization: a.locals.token
		}
	});
	let result = await response.json();
	if (response.status == 200) {
		return result
	} else {
		throw error(result.status, result.error)
	}
}
