import { error } from '@sveltejs/kit';


export const load = async ({ parent, fetch }) => {
    await fetch(`${import.meta.env.VITE_BACKEND}/admin/default`);

    let a = await parent();
    if (!a.locals.login || a.locals.user.access.length == 0) {
        throw error(404, "Unauthorized access")
    }
}