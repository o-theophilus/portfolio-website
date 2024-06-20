<script>
	import { module, loading, settings } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Button from '$lib/button/button.svelte';
	import Dialogue from '$lib/dialogue.svelte';

	export let post;
	let is_highlight = false;

	const highlight = () => {
		is_highlight = false;
		for (const x of $settings.highlight) {
			if (x.key == post.key) {
				is_highlight = true;
				break;
			}
		}
	};

	highlight();

	const submit = async () => {
		$loading = 'Adding Highlight . . .';
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/highlight/${post.key}`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			}
		});
		resp = await resp.json();
		$loading = false;

		if (resp.status == 200) {
			$settings.highlight = resp.posts;
			highlight();

			$module = {
				module: Dialogue,
				message: `${is_highlight ? 'Added' : 'Removed'} as Highlight`,
				buttons: [
					{
						name: 'OK',
						icon: 'check',
						fn: () => {
							$module = null;
						}
					}
				]
			};
		} else {
			$module = {
				module: Dialogue,
				title: 'Error',
				message: resp.error,
				status: 400,
				buttons: [
					{
						name: 'OK',
						icon: 'check',
						fn: () => {
							$module = null;
						}
					}
				]
			};
		}
	};
</script>

<Button size="small" on:click={submit}>
	Highlight:
	{#if is_highlight}
		ON
	{:else}
		Off
	{/if}
</Button>

<style>
</style>
