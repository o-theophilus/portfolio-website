<script>
	import { createEventDispatcher } from 'svelte';
	import { app, loading, notify, module } from '$lib/store.svelte.js';

	import { Button } from '$lib/button';
	import { IG } from '$lib/input';

	let emit = createEventDispatcher();

	let slug = $state();
	let error = $state({});

	const validate = () => {
		error = {};
		if (!slug) {
			error.slug = 'cannot be empty';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		loading.open('Adding Highlight . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/highlight`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: app.token
			},
			body: JSON.stringify({ key: slug })
		});
		resp = await resp.json();
		loading.close();

		if (resp.status == 200) {
			app.highlight = resp.posts;
			module.value.update();

			let is_highlight = false;
			for (const x of app.highlight) {
				if (x.slug == slug) {
					is_highlight = true;
					break;
				}
			}

			notify.open(`Highlight ${is_highlight ? 'Added' : 'Removed'}`);

			slug = null;
			emit('ok');
		} else {
			error = resp;
		}
	};
</script>

<IG name="URL Path" type="text" bind:value={slug} error={error.error} placeholder="Post url path" />

<Button icon="plus" onclick={validate} disabled={!slug}>Add</Button>
