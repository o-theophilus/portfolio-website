export const load = async ({ fetch, params, parent }) => {
    const { data } = await parent()

    let resp = await fetch(`${import.meta.env.VITE_BACKEND}/post/${params.slug}`, {
        method: 'get',
        headers: {
            'Content-Type': 'application/json',
            Authorization: data.locals.token
        },
    });
    resp = await resp.json();

    if (resp.status == 200) {
        return {
            post: resp.post,
            tags: resp.tags,
            comments: resp.comments,
            ratings: resp.ratings
        }
    }
}