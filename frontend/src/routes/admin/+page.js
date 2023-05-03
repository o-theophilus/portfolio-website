import { redirect } from '@sveltejs/kit';
import { api_url } from '$lib/store.js';

export const load = async ({ parent }) => {
    const { data } = await parent()
    
    // if(!data.locals.user.login || !data.locals.user.roles.includes("admin")){
    //     throw redirect(307, '/?module=info&title=Warning&status=warning&message=Unauthorised%20Access');
    // }    

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
    // throw redirect(307, '/?module=info&title=Unauthorised%20Access&status=warning&message=Unauthorised%20Access');
}