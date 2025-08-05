<script>
	import { onMount } from 'svelte';
	import { module, loading, notify, memory, app } from '$lib/store.svelte.js';

	import { IG } from '$lib/input';
	import { Button } from '$lib/button';
	import { Tags } from '$lib/layout';
	import { Icon } from '$lib/macro';

	let post = { ...module.value.post };
	let tags = post.tags.join(', ');
	let all_tags = [];
	let unused_tags = [];
	let error = {};

	const validate = () => {
		error = {};

		if (tags.split(', ').filter(Boolean).sort().join(', ') == post.tags.slice().sort().join(', ')) {
			error.tags = 'no change';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		error = {};

		loading.open('Saving Post . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/post/${module.value.post.key}`, {
			method: 'put',
			headers: {
				'Content-Type': 'application/json',
				Authorization: app.token
			},
			body: JSON.stringify({ tags: tags.split(', ').filter(Boolean) })
		});
		resp = await resp.json();
		loading.close();

		if (resp.status == 200) {
			module.value.update(resp.post);
			module.close();
			notify.open(`Tag${resp.post.tags.length > 1 ? 's' : ''} Saved`);
		} else {
			error = resp;
		}
	};

	const clean_value = (tag = '') => {
		tags = `${tags}, ${tag}`;
		tags = tags.replace(/\r?\n/g, ',');
		tags = tags.replace(/\s+/g, ' ');
		tags = tags.toLowerCase();
		tags = tags.split(',');
		tags = tags.map((i) => i.trim());
		tags = tags.filter(Boolean);
		tags = tags.filter((v, i, l) => l.indexOf(v) === i);
		tags = tags.join(', ');

		unused_tags = all_tags.filter((i) => !tags.split(', ').includes(i));
	};

	let loading_tags = true;
	onMount(async () => {
		if (tags == '') {
			tags = post.title.split(' ').join(', ');
		}

		let pn = 'tags';
		let i = $memory.findIndex((x) => x.name == pn);
		if (i == -1) {
			let resp = await fetch(`${import.meta.env.VITE_BACKEND}/tag`);
			resp = await resp.json();

			if (resp.status == 200) {
				all_tags = resp.tags;
				$memory.push({
					name: pn,
					data: resp.tags
				});
			}
		} else {
			all_tags = $memory[i].data;
		}
		loading_tags = false;

		clean_value();
	});
</script>

<form on:submit|preventDefault novalidate autocomplete="off">
	<strong class="ititle"> Edit tags </strong>
	{#if error.error}
		<div class="error">
			{error.error}
		</div>
	{/if}

	<IG
		name="Tags"
		bind:value={tags}
		error={error.tags}
		type="textarea"
		placeholder="Tags here"
		on:blur={() => {
			clean_value();
		}}
	/>

	<Tags
		tags={unused_tags}
		onclick={(e) => {
			clean_value(e.detail);
		}}
	/>

	<Button
		onclick={validate}
		disabled={tags.split(', ').filter(Boolean).sort().join(', ') ==
			post.tags.slice().sort().join(', ')}
	>
		Submit
		<Icon icon="send" />
	</Button>
</form>

<style>
	form {
		padding: var(--sp3);
	}

	.error {
		margin: var(--sp2) 0;
	}
</style>
