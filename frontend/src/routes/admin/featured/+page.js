import { redirect } from '@sveltejs/kit';


export const load = async ({ parent, fetch }) => {

    await fetch(`${import.meta.env.VITE_BACKEND}/admin/init`);

    let a = await parent();
    if (!a.locals.user.login || a.locals.user.permissions.length == 0) {
        throw redirect(307, `/?${new URLSearchParams({
            "module": "info",
            "title": "Warning",
            "status": 201,
            "message": "Unauthorized Access",
        })}`);
    }

    let resp = await fetch(`${import.meta.env.VITE_BACKEND}/featured`, {
        method: 'get',
        headers: {
            'Content-Type': 'application/json',
            Authorization: a.locals.token
        },
    });
    resp = await resp.json();

    if (resp.status == 200) {
        return { ...resp }
    }
}