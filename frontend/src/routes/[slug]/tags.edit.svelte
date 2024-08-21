<script>
	import { onMount } from 'svelte';
	import { module, loading, state, notification } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import IG from '$lib/input_group.svelte';
	import Button from '$lib/button/button.svelte';
	import Tag from '$lib/button/tag.svelte';
	import Icon from '$lib/icon.svelte';

	let post = { ...$module.post };
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

		$loading = 'Saving Post . . .';
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/post/${$module.post.key}`, {
			method: 'put',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify({ tags: tags.split(', ').filter(Boolean) })
		});
		resp = await resp.json();
		$loading = false;

		if (resp.status == 200) {
			$module.update(resp.post);
			$module = null;
			$notification = {
				message: `Tag${resp.post.tags.length > 1 ? 's' : ''} Saved`
			};
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
		let i = $state.findIndex((x) => x.name == pn);
		if (i == -1) {
			let resp = await fetch(`${import.meta.env.VITE_BACKEND}/tag`);
			resp = await resp.json();

			if (resp.status == 200) {
				all_tags = resp.tags;
				$state.push({
					name: pn,
					data: resp.tags
				});
			}
		} else {
			all_tags = $state[i].data;
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
	<div class="line">
		{#each unused_tags as tag}
			<Tag
				on:click={() => {
					clean_value(tag);
				}}
			>
				{tag}
			</Tag>
		{/each}
	</div>

	<br />

	<Button
		on:click={validate}
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

	.line {
		display: flex;
		flex-wrap: wrap;
		gap: var(--sp1);
	}

	.error {
		margin: var(--sp2) 0;
	}
</style>
