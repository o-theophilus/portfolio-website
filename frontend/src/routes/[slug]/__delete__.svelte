<script>
	import { goto } from '$app/navigation';
	import { api_url, module, loading } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Button from '$lib/button.svelte';
	import Info from '$lib/__info__.svelte';

	export let post;

	let error = '';

	const submit = async () => {
		error = '';

		$loading = "Deleting Post . . .";
		const resp = await fetch(`${api_url}/post/${post.key}`, {
			method: 'delete',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			}
		});
		$loading = false;

		if (resp.ok) {
			const data = await resp.json();

			if (data.status == 200) {
				$module = {
					module: Info,
					title: 'Done',
					status: 'good',
					message: "Post Deleted",
					button: [
						{
							name: 'Ok',
							fn: () => {
								$module = '';
							}
						}
					]
				};
				goto("/post");
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
