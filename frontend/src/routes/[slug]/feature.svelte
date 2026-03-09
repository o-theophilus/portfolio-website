<script>
	import { Switch } from '$lib/button';
	import { app, loading, notify } from '$lib/store.svelte.js';
	let { post, update } = $props();

	const submit = async () => {
		loading.open('Updating feature . . .');

		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/posts/${post.key}/feature`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: app.token
			}
		});
		resp = await resp.json();
		loading.close();

		if (resp.status == 200) {
			update(resp.post);
			let msg = 'Added post to featured';
			if (post.featured == 0) {
				msg = 'Removed post from featured';
			}
			notify.open(msg);
		} else {
			notify.open(resp.error, 400);
		}
	};
</script>

{#if app.user.access.includes('post:edit_featured') && post.status == 'active'}
	<Switch
		--toggle-height="21px"
		--toggle-font-size="0.8rem"
		--toggle-padding-x="8px"
		list={['', 'feature']}
		value={post.featured == 0 ? '' : 'feature'}
		onclick={submit}
	/>
{/if}
