export const load = async ({ fetch, parent }) => {
    const a = await parent()

    let resp = await fetch(`${import.meta.env.VITE_BACKEND}/post`, {
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