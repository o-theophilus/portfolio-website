

export const load = async ({ fetch, parent }) => {
    const { data } = await parent()

    let resp = await fetch(`${import.meta.env.VITE_BACKEND}/tags`, {
        method: 'get',
        headers: {
            'Content-Type': 'application/json',
            Authorization: data.locals.token
        },
    });
    resp = await resp.json();

    if (resp.status == 200) {
        return {
            tags: resp.tags,
        }
    }

}