<script>
	import { goto } from '$app/navigation';
	import { module, loading, notify, app } from '$lib/store.svelte.js';

	import { Button } from '$lib/button';
	import { Form } from '$lib/layout';
	import { Icon } from '$lib/macro';

	let error = $state({});

	const submit = async () => {
		error = {};

		loading.open('Deleting Post . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/post/${module.value.post.key}`, {
			method: 'delete',
			headers: {
				'Content-Type': 'application/json',
				Authorization: app.token
			}
		});
		loading.close();
		resp = await resp.json();

		if (resp.status == 200) {
			module.close();
			notify.open('Post Deleted');
			goto('/post');
		} else {
			error = resp;
		}
	};
</script>

<Form title="Delete" error={error.error}>
	<div class="error">Are you sure you want to delete this post</div>

	<br />
	<div class="line">
		<Button extra="hover_red" onclick={submit}>
			<Icon icon="delete" />
			Yes
		</Button>
		<Button
			onclick={() => {
				module.close();
			}}
		>
			<Icon icon="close" />
			No
		</Button>
	</div>
</Form>

<style>
	.line {
		display: flex;
		gap: var(--sp1);
	}

	.error {
		margin: var(--sp2) 0;
	}
</style>
