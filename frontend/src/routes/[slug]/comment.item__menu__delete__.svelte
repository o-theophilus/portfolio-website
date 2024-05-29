<script>
	import { module, loading, portal } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Button from '$lib/button.svelte';
	import Info from '$lib/info.svelte';

	export let comment_key;

	let error = {};

	const submit = async () => {
		error = {};

		$loading = `Deleting comment . . .`;
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/comment/${comment_key}`, {
			method: 'delete',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			}
		});
		$loading = false;

		resp = await resp.json();

		if (resp.status == 200) {
			$portal = {
				for: 'comment',
				data: resp.comments
			};

			$module = {
				module: Info,
				message: 'Comment Deleted',
				buttons: [
					{
						name: 'Ok',
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
