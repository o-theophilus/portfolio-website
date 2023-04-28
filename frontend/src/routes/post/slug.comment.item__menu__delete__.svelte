<script>
	import { goto } from '$app/navigation';
	import { api_url, module, loading, portal } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Button from '$lib/button.svelte';
	import Info from '$lib/__info__.svelte';

	export let comment_key;

	let error = '';

	const submit = async () => {
		error = '';

		$loading = `Deleting comment . . .`;
		const resp = await fetch(`${api_url}/comment/${comment_key}`, {
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
				portal({
					for: 'comment',
					data: data.data.comments
				});

				$module = {
					module: Info,
					title: 'Done',
					status: 'good',
					message: 'Comment Deleted',
					button: [
						{
							name: 'Ok',
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
