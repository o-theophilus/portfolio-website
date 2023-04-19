import { api_url } from '$lib/store.js';

export async function handle({ event, resolve }) {

    const resp = await fetch(`${api_url}/init`, {
        method: 'post',
        headers: {
            'Content-Type': 'application/json',
            Authorization: event.cookies.get("token")
        }
    });

    if (resp.ok) {
        let data = await resp.json();

        if (data.status == 200) {
            // event.cookies.set("session", data.data.token)
            event.locals = data.data;
        }
        return await resolve(event);
    }

    throw new Error(404, `Error status: ${resp.status}`)
    // event.locals = {
    //     "token": "IjFkYjk0ZDhjMDA0NjRhNWY5OWFkMTdlZDNhOTJhNTk4Ig.ZEBIgA.s-Z2erT0a9yHfcEhECesdVJ5CpQ",
    //     "user": {
    //         "email": "f2855b041579480a957cf2ba645ed413",
    //         "key": "1db94d8c00464a5f99ad17ed3a92a598",
    //         "login": false,
    //         "name": "f2855b041579480a957cf2ba645ed413",
    //         "roles": [],
    //         "setting": {
    //             "theme": "dark"
    //         },
    //         "status": "anonymous"
    //     },
    // };
    // return await resolve(event);
}







