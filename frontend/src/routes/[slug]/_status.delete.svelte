<script>
	import { goto } from '$app/navigation';
	import { module, loading } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Button from '$lib/button.svelte';
	import Info from '$lib/info.svelte';

	let error = {};

	const submit = async () => {
		error = {};

		$loading = 'Deleting Post . . .';
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/post/${$module.post.key}`, {
			method: 'delete',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			}
		});
		$loading = false;
		resp = await resp.json();

		if (resp.status == 200) {
			$module = {
				module: Info,
				message: 'Post Deleted',
				buttons: [
					{
						name: 'Ok',
						fn: () => {
							$module = '';
						}
					}
				]
			};
			goto('/post');
		} else {
			error = resp;
		}
	};
</script>

<form on:submit|preventDefault novalidate autocomplete="off">
	<strong class="big error">Delete</strong>
	<div class="error">Are you sure you want to delete</div>
	{#if error.error}
		<span class="error">
			{error.error}
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
		padding: var(--sp3);
	}
</style>
