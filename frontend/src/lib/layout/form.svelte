<script>
	import { Note } from '$lib/info';
	let { title, error, children } = $props();
</script>

<form onsubmit={(e) => e.preventDefault()} novalidate autocomplete="off">
	<strong class="ititle"> {title} </strong>
	<Note note={error} status="400" --note-margin-top="16px"></Note>
	{@render children()}
</form>

<style>
	form {
		padding: var(--form-padding, 24px);
	}
</style>
