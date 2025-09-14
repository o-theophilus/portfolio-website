<script>
	import { loading, app, notify } from '$lib/store.svelte.js';
	import { Toggle } from '$lib/button';
	import { onMount } from 'svelte';
	let { item } = $props();

	let is_highlighted = $derived.by(() => {
		if (app.highlight) {
			for (const x of app.highlight) {
				if (x.key == item.key) return true;
			}
		}
		return false;
	});

	onMount(async () => {
		if (!app.highlight) {
			let resp = await fetch(`${import.meta.env.VITE_BACKEND}/highlights`);
			resp = await resp.json();

			if (resp.status == 200) {
				app.highlight = resp.items;
			}
		}
	});

	const submit = async () => {
		loading.open('Adding Highlight . . .');

		if (is_highlighted) {
			app.highlight = app.highlight.filter((x) => x.key != item.key);
		} else {
			app.highlight.push(item);
		}

		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/highlight`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: app.token
			},
			body: JSON.stringify({ key: item.key })
		});
		resp = await resp.json();
		loading.close();

		if (resp.status == 200) {
			app.highlight = resp.items;
			notify.open(`${is_highlighted ? 'Added' : 'Removed'} as Highlight`);
		} else {
			notify.open(resp.error, 400);
		}
	};
</script>

{#if app.user.access.includes('post:edit_highlight') && item.status == 'active'}
	<Toggle state_2="highlight" active={is_highlighted} onclick={submit} />
{/if}
