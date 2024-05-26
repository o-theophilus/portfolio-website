import { redirect } from '@sveltejs/kit';


export const load = async ({ parent, fetch }) => {

    await fetch(`${import.meta.env.VITE_BACKEND}/admin/init`);
    
    let a = await parent();
    if (!a.locals.user.login || a.locals.user.permissions.length == 0) {
        const url = new URL("https://a");
        url.searchParams.append("module", "info");
        url.searchParams.append("title", "Warning");
        url.searchParams.append("status", "warning");
        url.searchParams.append("message", "Unauthorised Access");
        throw redirect(307, `/${url.search}`);
    }
}