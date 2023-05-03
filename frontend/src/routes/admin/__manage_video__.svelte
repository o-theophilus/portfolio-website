<script>
	import { api_url, module, portal, loading } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Input from '$lib/input_group.svelte';
	import Button from '$lib/button.svelte';
	import Info from '$lib/__info__.svelte';

	export let setting;

	let featured_posts = [...setting.featured_posts];
	let error = '';

	const submit = async () => {
		error = '';

		$loading = `Saving . . .`;
		const resp = await fetch(`${api_url}/featured_post`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify({ featured_posts })
		});
		$loading = false;

		if (resp.ok) {
			const data = await resp.json();
			if (data.status == 200) {
				portal({
					for: 'setting',
					data: data.data.setting
				});

				$module = {
					module: Info,
					title: 'Done',
					status: 'good',
					message: `Featured Posts Saved`,
					button: [
						{
							name: 'OK',
							fn: () => {
								$module = '';
							}
						}
					]
				};
			} else {
				error = data.message;
			}
		}
	};

	const get_slugs = async () => {
		const resp = await fetch(`${api_url}/slug`, {
			method: 'get',
			headers: {
				'Content-Type': 'application/json'
			}
		});
		return await resp.json();
	};
	console.log(get_slugs());
</script>

<form on:submit|preventDefault novalidate autocomplete="off">
	<strong class="big"> Featured Posts </strong>
	{#if error}
		<span class="error">
			{error}
		</span>
	{/if}
	<Input name="post slug{featured_posts.length > 1 ? 's' : ''}">
		{#each Array(5) as _, i}
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
		padding: var(--gap3);
	}
</style>
