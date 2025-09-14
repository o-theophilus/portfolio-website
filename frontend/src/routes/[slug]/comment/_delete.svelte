<script>
	import { module, loading, notify, app } from '$lib/store.svelte.js';

	import { Button } from '$lib/button';
	import { Form } from '$lib/layout';
	import { Note } from '$lib/info';
	import Item from './item.svelte';

	let item = { ...module.value.item };
	let error = $state({});

	const submit = async () => {
		error = {};

		loading.open(`Deleting comment . . .`);

		let resp = await fetch(
			`${import.meta.env.VITE_BACKEND}/comment/${item.key}?${new URLSearchParams(
				module.value.search
			).toString()}`,
			{
				method: 'delete',
				headers: {
					'Content-Type': 'application/json',
					Authorization: app.token
				}
			}
		);
		loading.close();
		resp = await resp.json();

		if (resp.status == 200) {
			module.value.update(resp.items);
			module.close();
			notify.open('Comment Deleted');
		} else {
			error = resp;
		}
	};
</script>

<Form title="Delete Comment" error={error.error}>
	<Item {item}></Item>

	<Note --note-margin-top="16px" status="400" note="Are you sure you want to delete this comment"
	></Note>

	<div class="line">
		<Button icon="x" onclick={() => module.close()}>Close</Button>
		<Button icon="trash-2" --button-background-color-hover="red" onclick={submit}>Delete</Button>
	</div>
</Form>

<style>
	.line {
		display: flex;
		gap: var(--sp1);
	}
</style>
