<script>
	import { onMount } from 'svelte';
	import { module, loading, notify, app } from '$lib/store.svelte.js';

	import { IG } from '$lib/input';
	import { Button, Tag } from '$lib/button';
	import { Form } from '$lib/layout';

	let error = $state({});
	let init = module.value.tags;
	let tags_string = $state(init.join(', '));
	let tags = $derived(
		tags_string
			.replace(/\r?\n/g, ',')
			.replace(/\s+/g, ' ')
			.toLowerCase()
			.split(',')
			.map((i) => i.trim())
			.filter(Boolean)
			.filter((v, i, arr) => arr.indexOf(v) === i)
	);
	let unused_tags = $derived.by(() => {
		if (!app.tags) return [];
		return app.tags.filter((i) => !tags.includes(i));
	});

	const validate = () => {
		error = {};

		if (JSON.stringify(tags.sort()) === JSON.stringify(init.sort())) {
			error.tags = 'No changes were made';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		error = {};

		loading.open('Saving Post . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/post/${module.value.key}`, {
			method: 'put',
			headers: {
				'Content-Type': 'application/json',
				Authorization: app.token
			},
			body: JSON.stringify({ tags })
		});
		resp = await resp.json();
		loading.close();

		if (resp.status == 200) {
			module.value.update(resp.item);
			module.close();
			notify.open(`Tag${resp.item.tags.length > 1 ? 's' : ''} Saved`);
		} else {
			error = resp;
		}
	};

	const clean_value = (tag = '') => {
		tags_string += `, ${tag}`;
		tags_string = tags.join(', ');
	};

	let _loading = true;
	onMount(async () => {
		if (tags_string == '') {
			tags_string = module.value.title.split(' ').join(', ');
		}

		if (!app.tags) {
			let resp = await fetch(`${import.meta.env.VITE_BACKEND}/tags`);
			resp = await resp.json();

			if (resp.status == 200) {
				app.tags = resp.tags;
			}
		}
		_loading = false;
	});
</script>

<Form title="Edit Tags" error={error.error}>
	<IG
		name="Tags"
		bind:value={tags_string}
		error={error.tags}
		type="textarea"
		placeholder="Tags here"
		onblur={clean_value}
	/>

	<div class="line">
		{#each unused_tags as x}
			<Tag
				onclick={() => {
					clean_value(x);
				}}>{x}</Tag
			>
		{/each}
	</div>

	<Button icon2="send-horizontal" onclick={validate}>Submit</Button>
</Form>

<style>
	.line {
		margin: 16px 0;
		gap: 4px;
	}
</style>
