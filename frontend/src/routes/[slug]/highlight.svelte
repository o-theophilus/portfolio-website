<script>
	import { loading, app, notify } from '$lib/store.svelte.js';

	import { Toggle } from '$lib/button';

	let { post_key } = $props();
	let is_highlight = $state(false);

	const highlight = () => {
		is_highlight = false;
		for (const x of app.settings.highlight) {
			if (x.key == post_key) {
				is_highlight = true;
				break;
			}
		}
	};

	highlight();

	const submit = async () => {
		loading.open('Adding Highlight . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/highlight`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: app.token
			},
			body: JSON.stringify({ key: post_key })
		});
		resp = await resp.json();
		loading.close();

		if (resp.status == 200) {
			app.settings.highlight = resp.posts;
			notify.open(`${is_highlight ? 'Added' : 'Removed'} as Highlight`);
		} else {
			notify.open(resp.error, 400);
		}
		highlight();
	};
</script>

<Toggle
	state_2="highlight"
	active={is_highlight}
	onclick={() => {
		is_highlight = !is_highlight;
		submit();
	}}
/>
