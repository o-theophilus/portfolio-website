<script>
	import { loading, settings, notify } from '$lib/store_old.js';
	import { token } from '$lib/cookie.js';

	import Toggle from '$lib/toggle.svelte';

	export let post_key;
	let is_highlight = false;

	const highlight = () => {
		is_highlight = false;
		for (const x of $settings.highlight) {
			if (x.key == post_key) {
				is_highlight = true;
				break;
			}
		}
	};

	highlight();

	const submit = async () => {
		$loading = 'Adding Highlight . . .';
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/highlight`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify({ key: post_key })
		});
		resp = await resp.json();
		$loading = false;

		if (resp.status == 200) {
			$settings.highlight = resp.posts;
			$notify.add(`${is_highlight ? 'Added' : 'Removed'} as Highlight`);
		} else {
			$notify.add(resp.error, 400);
		}
		highlight();
	};
</script>

<Toggle
	state_2="highlight"
	active={is_highlight}
	on:click={() => {
		is_highlight = !is_highlight;
		submit();
	}}
/>

<style>
</style>
