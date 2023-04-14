<script>
	import { goto } from '$app/navigation';
	import { api_url, module } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Button from '$lib/comp/button.svelte';
	import Info from '$lib/module/info.svelte';

	export let post;

	let error = '';

	const submit = async () => {
		const resp = await fetch(`${api_url}/${post.type}/${post.slug}`, {
			method: 'delete',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			}
		});

		if (resp.ok) {
			const data = await resp.json();

			if (data.status == 200) {
				$module = {
					module: Info,
					title: 'Done',
					status: 'good',
					message: `${post.type} Deleted`,
					button: [
						{
							name: 'Ok',
							fn: () => {
								$module = '';
							}
						}
					]
				};
				goto(`/${post.type}/`);
			} else {
				error = data.message;
			}
		}
	};
</script>

<form on:submit|preventDefault novalidate autocomplete="off">
	<strong class="big error">Delete</strong>
	<div class="error">Are you sure you want to delete</div>
	{#if error}
		<span class="error">
			{error}
		</span>
	{/if}

	<div class="h">
		<Button
			on:click={() => {
				submit();
			}}
		>
			Yes
		</Button>
		<Button
			on:click={() => {
				$module = '';
			}}
		>
			No
		</Button>
	</div>
</form>

<style>
	form {
		padding: var(--gap3);
	}
</style>
