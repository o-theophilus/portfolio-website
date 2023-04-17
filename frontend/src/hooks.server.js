import { api_url } from '$lib/store.js';

export async function handle({ event, resolve }) {

    // const resp = await fetch(`${api_url}/init`, {
    //     method: 'post',
    //     headers: {
    //         'Content-Type': 'application/json',
    //         Authorization: event.cookies.get("token")
    //     }
    // });

    // if (resp.ok) {
    //     let data = await resp.json();

    //     if (data.status == 200) {
    //         // event.cookies.set("session", data.data.token)
    //         event.locals = data.data;
    //     }
    //     return await resolve(event);
    // }

    // throw new Error(404, `Error status: ${resp.status}`)
    event.locals = {};
    return await resolve(event);
}







