import { error } from '@sveltejs/kit';

export const load = async ({ parent, fetch }) => {
	let a = await parent();
	if (!a.locals.user.permissions.includes("admin:manage_photo")) {
		throw error(400, "unauthorized access")
	}

	let resp = await fetch(`${import.meta.env.VITE_BACKEND}/photo/error`, {
		method: 'get',
		headers: {
			'Content-Type': 'application/json',
			Authorization: a.locals.token
		}
	});
	resp = await resp.json();

	if (resp.status == 200) {
		return resp
	}
}
