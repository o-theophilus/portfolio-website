<script>
	import { loading, settings, notification } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Button from '$lib/button/button.svelte';
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
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/highlight/${post_key}`, {
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
			$notification = {
				message: `${is_highlight ? 'Added' : 'Removed'} as Highlight`
			};
		} else {
			$notification = {
				status: 400,
				message: resp.error
			};
		}
		highlight();
	};
</script>

<Toggle
	state_1="off"
	state_2="highlight"
	active={is_highlight}
	on:click={() => {
		is_highlight = !is_highlight;
		submit();
	}}
/>

<style>
</style>
