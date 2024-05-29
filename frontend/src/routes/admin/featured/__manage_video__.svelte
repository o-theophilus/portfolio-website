<script>
	import { module, portal, loading } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Input from '$lib/input_group.svelte';
	import Button from '$lib/button.svelte';
	import Info from '$lib/info.svelte';

	export let setting;

	let featured_posts = [...setting.featured_posts];
	let error = {};

	const submit = async () => {
		error = {};

		$loading = `Saving . . .`;
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/featured_post`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify({ featured_posts })
		});
		resp = await resp.json();
		$loading = false;

		if (resp.status == 200) {
			$portal = {
				for: 'setting',
				data: resp.setting
			};

			$module = {
				module: Info,
				message: `Featured Posts Saved`,
				buttons: [
					{
						name: 'OK',
						fn: () => {
							$module = '';
						}
					}
				]
			};
		} else {
			error = resp;
		}
	};

	const get_slugs = async () => {
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/slug`, {
			method: 'get',
			headers: {
				'Content-Type': 'application/json'
			}
		});
		return await resp.json();
	};
</script>

<form on:submit|preventDefault novalidate autocomplete="off">
	<strong class="big"> Featured Posts </strong>
	{#if error.error}
		<span class="error">
			{error.error}
		</span>
	{/if}
	<Input name="post slug{featured_posts.length > 1 ? 's' : ''}">
		{#each Array(10) as _, i}
			<input placeholder="post slug {i + 1} here " type="text" bind:value={featured_posts[i]} />
		{/each}
	</Input>

	<Button
		on:click={() => {
			submit();
		}}
	>
		Submit
	</Button>

	{#await get_slugs()}
		Loaging Slugs . . .
	{:then data}
		{#each data.data.slugs as slug}
			{slug}
			<br />
		{/each}
	{/await}
</form>

<style>
	form {
		padding: var(--sp3);
	}
</style>
