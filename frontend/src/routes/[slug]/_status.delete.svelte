<script>
	import { goto } from '$app/navigation';
	import { module, loading } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Button from '$lib/button/button.svelte';
	import Dialogue from '$lib/dialogue.svelte';
	import Icon from '$lib/icon.svelte';

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
				module: Dialogue,
				message: 'Post Deleted',
				buttons: [
					{
						name: 'Ok',
						icon: 'check',
						fn: () => {
							$module = null;
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
	<strong class="ititle">Delete</strong>
	<div class="error">Are you sure you want to delete this post</div>
	{#if error.error}
		<div class="error">
			{error.error}
		</div>
	{/if}

	<br />
	<div class="line">
		<Button extra="hover_red" on:click={submit}>
			<Icon icon="delete" />
			Yes
		</Button>
		<Button
			on:click={() => {
				$module = null;
			}}
		>
			<Icon icon="close" />
			No
		</Button>
	</div>
</form>

<style>
	form {
		padding: var(--sp3);
	}

	.line {
		display: flex;
		gap: var(--sp1);
	}

	.error {
		margin: var(--sp2) 0;
	}
</style>
