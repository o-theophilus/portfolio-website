export const load = async ({ fetch }) => {
    let resp = await fetch(`${import.meta.env.VITE_BACKEND}/featured_post`);
    resp = await resp.json();

    if (resp.status == 200) {
        return resp
    }
}