<script>
	import { module } from '$lib/store.svelte.js';
	import { Button } from '$lib/button';
	import { Form } from '$lib/layout';
	import { Note } from '$lib/info';
	import Confirm from './confirm.svelte';
</script>

<Form title="Delete Account">
	<Note note="Warning" status="400">
		Deleting your account irreversible and will permanently erase all associated data.
		<br />
		This action cannot be undone.
		<br />
		<br />
		Are you sure you want to continue?
	</Note>

	<Button
		icon="trash-2"
		onclick={() => {
			module.open(Confirm);
		}}
	>
		Continue
	</Button>
</Form>
