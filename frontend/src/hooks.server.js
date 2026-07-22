export async function handle({ event, resolve }) {
    let response = await fetch(`${import.meta.env.VITE_BACKEND}/init`, {
        method: 'post',
        headers: {
            'Content-Type': 'application/json',
            Authorization: event.cookies.get("token")
        }
    });
    let result = await response.json();

    if (response.status == 200) {
        event.locals = result;
        return await resolve(event);
    }

    throw new Error(404, `Error status: ${result.status}`)

}