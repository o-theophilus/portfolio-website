import { redirect } from '@sveltejs/kit';
import { api_url } from '$lib/store.js';

export const load = async ({ parent }) => {
    const { data } = await parent()
    
    const url = new URL("https://a");
    url.searchParams.append("module", "info");
    url.searchParams.append("title", "Warning");
    url.searchParams.append("status", "warning");
    url.searchParams.append("message", "Unauthorised Access");

    if(!data.locals.user.login || !data.locals.user.roles.includes("admin")){
        throw redirect(307, `/${url.search}`);
    }    
        
        const resp = await fetch(`${api_url}/admin`, {
        method: 'get',
        headers: {
            'Content-Type': 'application/json',
            Authorization: data.locals.token
        },
    });

    if (resp.ok) {
        const data = await resp.json();

        if (data.status == 200) {
            return {
                setting: data.data.setting,
            }
        }
    }
    throw redirect(307, `/${url.search}`);
}