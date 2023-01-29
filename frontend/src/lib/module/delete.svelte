<script>
	import { goto } from '$app/navigation';
	import { api_url, module } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Button from '$lib/comp/button.svelte';
	import Info from '$lib/module/info.svelte';

	export let data;
	let { post } = data;
	let { post_type } = data;

	let error = '';

	const submit = async () => {
		const resp = await fetch(`${api_url}/${post_type}/${post.slug}`, {
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
					data: {
						title: "Done",
						status: 'good',
						message: `${post_type} Deleted`,
						button: [
							{
								name: 'Ok',
								href: ''
							}
						]
					}
				};
				goto(`/${post_type}/`);
			} else {
				error = data.message;
			}
		}
	};
</script>

<section>
	<strong class="big">Delete</strong>
	<form on:submit|preventDefault novalidate autocomplete="off">
		<div>Are you sure you want to delete</div>
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
</section>

<style>
	section {
		display: flex;
		flex-direction: column;

		width: 100%;
	}
	strong,
	form {
		padding: var(--gap3);
	}
	strong {
		background-color: var(--color2);
	}
</style>
