import { error } from '@sveltejs/kit';

export const load = async ({ parent, fetch }) => {
	let a = await parent();
	if (!a.locals.user.access.includes("admin:manage_files")) {
		throw error(404, "Unauthorized access")
	}

	let resp = await fetch(`${import.meta.env.VITE_BACKEND}/file_error`, {
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
