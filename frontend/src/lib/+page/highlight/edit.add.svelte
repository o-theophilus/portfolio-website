<script>
	import { app, loading, notify, module } from '$lib/store.svelte.js';

	import { Button } from '$lib/button';
	import { IG } from '$lib/input';

	let slug = $state();
	let error = $state({});
	let { ondone } = $props();

	const validate = () => {
		error = {};
		if (!slug) {
			error.slug = 'This field is required';
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
			app.highlight = resp.items;
			module.value.reset_index();

			let is_added = false;
			for (const x of app.highlight) {
				if (x.slug == slug) {
					is_added = true;
					break;
				}
			}

			notify.open(`Highlight ${is_added ? 'Added' : 'Removed'}`);

			slug = null;
			ondone();
		} else {
			error = resp;
		}
	};
</script>

<IG name="URL Path" type="text" bind:value={slug} error={error.error} placeholder="Post url path" />

<Button icon="plus" onclick={validate} disabled={!slug}>Add</Button>
