<script>
	import { createEventDispatcher } from 'svelte';
	import { loading, settings, notification, module } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Button from '$lib/button/button.svelte';
	import Icon from '$lib/icon.svelte';
	import IG from '$lib/input_group.svelte';

	let emit = createEventDispatcher();

	let slug;
	let error = {};

	const validate = () => {
		error = {};
		if (!slug) {
			error.slug = 'cannot be empty';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		$loading = 'Adding Highlight . . .';
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/highlight`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify({ key: slug })
		});
		resp = await resp.json();
		$loading = false;

		if (resp.status == 200) {
			$settings.highlight = resp.posts;
			$module.update();

			let is_highlight = false;
			for (const x of $settings.highlight) {
				if (x.slug == slug) {
					is_highlight = true;
					break;
				}
			}

			$notification = {
				message: `Highlight ${is_highlight ? 'Added' : 'Removed'}`
			};

			slug = null;
			emit('ok');
		} else {
			error = resp;
		}
	};
</script>

<IG name="URL Path" type="text" bind:value={slug} error={error.error} placeholder="Post url path" />

<Button on:click={validate} disabled={!slug}>
	<Icon icon="add" />
	Add
</Button>
